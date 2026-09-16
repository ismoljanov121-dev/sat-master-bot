"""
EduTest Pro - Question Batch Ingestion & Generation Engine
Handles candidate auditing, lifecycle transitions (published, rejected, pending_human_review),
atomic vault ingestion, and detailed batch reporting.
"""

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

from services.adversarial_audit import adversarial_audit_question
from services.question_repository import vault
from services.question_service import qs

logger = logging.getLogger("BatchGenerator")

REJECTED_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "rejected_questions.json")


def run_batch_audit_and_ingest(
    candidates: list[dict[str, Any]],
    batch_name: str,
    dry_run: bool = False
) -> dict[str, Any]:
    """
    Runs adversarial audit on a list of candidate questions and ingests approved ones into the vault.
    
    Returns comprehensive report:
      - batch_name: str
      - total_candidates: int
      - published_count: int
      - rejected_count: int
      - pending_count: int
      - by_section: dict[section, int]
      - by_domain: dict[domain, int]
      - by_difficulty: dict[difficulty, int]
      - published_ids: list[str]
      - rejected_details: list[dict]
      - pending_details: list[dict]
    """
    logger.info(f"Starting batch audit for '{batch_name}' with {len(candidates)} candidates.")
    
    # Load all existing published questions for duplicate & similarity cross-checking
    existing_published = vault.get_published_questions()
    
    published_ids: list[str] = []
    rejected_details: list[dict[str, Any]] = []
    pending_details: list[dict[str, Any]] = []
    
    by_section: dict[str, int] = {"math": 0, "reading": 0, "writing": 0}
    by_domain: dict[str, int] = {}
    by_difficulty: dict[str, int] = {"Easy": 0, "Medium": 0, "Hard": 0}
    
    for candidate in candidates:
        qid = str(candidate.get("id", "UNKNOWN")).strip()
        section = str(candidate.get("section", "unknown")).lower().strip()
        domain = str(candidate.get("domain", "Unknown")).strip()
        diff = str(candidate.get("difficulty", "Medium")).capitalize().strip()
        
        # Tag authoring metadata if not present
        candidate.setdefault("author", f"batch_generator:{batch_name}")
        candidate.setdefault("license", "proprietary_original")
        
        # Run 7-stage adversarial audit
        decision, errors, warnings, metadata = adversarial_audit_question(candidate, existing_published)
        
        if decision == "published":
            if not dry_run:
                ok, msg = vault.upsert_question(candidate, status="published")
                if ok:
                    published_ids.append(qid)
                    existing_published.append(candidate)  # update pool for intra-batch duplicate checks
                    by_section[section] = by_section.get(section, 0) + 1
                    by_domain[domain] = by_domain.get(domain, 0) + 1
                    by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
                else:
                    rejected_details.append({
                        "id": qid,
                        "section": section,
                        "reasons": [f"Vault upsert failed: {msg}"]
                    })
            else:
                published_ids.append(qid)
                existing_published.append(candidate)
                by_section[section] = by_section.get(section, 0) + 1
                by_domain[domain] = by_domain.get(domain, 0) + 1
                by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
                
        elif decision == "pending_human_review":
            if not dry_run:
                vault.upsert_question(candidate, status="pending_human_review")
            pending_details.append({
                "id": qid,
                "section": section,
                "domain": domain,
                "warnings": warnings,
                "metadata": metadata
            })
            
        else:  # rejected
            rejected_details.append({
                "id": qid,
                "section": section,
                "domain": domain,
                "errors": errors,
                "metadata": metadata
            })

    # Persist rejected items for audit tracking
    if rejected_details and not dry_run:
        _record_rejected_questions(batch_name, rejected_details)

    # Atomic sync to disk and reload question service
    if not dry_run and published_ids:
        vault.sync_to_json()
        qs.reload()

    report = {
        "batch_name": batch_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_candidates": len(candidates),
        "published_count": len(published_ids),
        "rejected_count": len(rejected_details),
        "pending_count": len(pending_details),
        "by_section": by_section,
        "by_domain": by_domain,
        "by_difficulty": by_difficulty,
        "published_ids": published_ids,
        "rejected_details": rejected_details,
        "pending_details": pending_details,
    }
    
    logger.info(
        f"Batch '{batch_name}' completed: {len(published_ids)} published, "
        f"{len(rejected_details)} rejected, {len(pending_details)} pending."
    )
    return report


def _record_rejected_questions(batch_name: str, rejected_list: list[dict[str, Any]]):
    """Appends rejected candidates with their failure causes to data/rejected_questions.json."""
    os.makedirs(os.path.dirname(REJECTED_PATH), exist_ok=True)
    existing_records: list[dict[str, Any]] = []
    if os.path.exists(REJECTED_PATH):
        try:
            with open(REJECTED_PATH, "r", encoding="utf-8") as f:
                existing_records = json.load(f)
        except Exception:
            existing_records = []

    record = {
        "batch_name": batch_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "count": len(rejected_list),
        "items": rejected_list
    }
    existing_records.append(record)

    with open(REJECTED_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_records, f, indent=2, ensure_ascii=False)
