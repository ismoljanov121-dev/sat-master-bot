"""
Import Batches 6, 7, and 8 into Question Vault and Sync sat_question_bank.json.
"""

import os
import sys
import json

BASE_DIR = r"D:\AntigravityWorkspace\projects\sat_ai_bot"
sys.path.insert(0, BASE_DIR)

from services.question_repository import vault
from services.question_validator import validate_question

def main():
    batches = [
        ("Batch 6 (Math)", os.path.join(BASE_DIR, "data", "batch6_math.json")),
        ("Batch 7 (Reading)", os.path.join(BASE_DIR, "data", "batch7_reading.json")),
        ("Batch 8 (Writing)", os.path.join(BASE_DIR, "data", "batch8_writing.json"))
    ]

    total_imported = 0
    for name, file_path in batches:
        if not os.path.exists(file_path):
            print(f"ERROR: File {file_path} does not exist!")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        print(f"Processing {name} ({len(items)} questions)...")
        batch_success = 0
        batch_fail = 0
        for q in items:
            valid, errs = validate_question(q)
            if not valid:
                print(f"Validation failure on {q.get('id')}: {errs}")
                batch_fail += 1
                continue

            ok, msg = vault.upsert_question(q, status="published")
            if ok:
                batch_success += 1
            else:
                print(f"Upsert failure on {q.get('id')}: {msg}")
                batch_fail += 1

        print(f"{name} completed: {batch_success} succeeded, {batch_fail} failed.")
        total_imported += batch_success

    sync_count = vault.sync_to_json()
    print("\n--- VAULT SUMMARY ---")
    print(f"Total published questions synced: {sync_count}")
    print("Counts by status:", vault.get_counts_by_status())
    print("Published by section:", vault.get_published_counts_by_section())
    print("Breakdown by difficulty:", vault.get_breakdown_by_difficulty())

if __name__ == "__main__":
    main()
