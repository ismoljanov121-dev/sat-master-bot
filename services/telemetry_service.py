"""
EduTest Pro - Minimal Privacy-Preserving Telemetry Service
Tracks strictly necessary product engagement signals without collecting personal identifiable info (PII):
- starter_drill_started, starter_drill_completed
- day2_retention, day7_retention
- dropoff_step
- mistake_revisited
- question_reported
- pro_beta_feature_used
"""

from typing import Any
import logging

from database import db, get_utc_now_str

logger = logging.getLogger("TelemetryService")

ALLOWED_EVENTS = {
    "starter_drill_started",
    "starter_drill_completed",
    "day2_retention",
    "day7_retention",
    "dropoff_step",
    "mistake_revisited",
    "question_reported",
    "pro_beta_feature_used"
}


class TelemetryService:
    async def record_event(
        self,
        event_name: str,
        user_id: int | None = None,
        metadata: dict[str, Any] | None = None
    ) -> bool:
        """Records an anonymous product engagement event."""
        if event_name not in ALLOWED_EVENTS:
            logger.warning(f"Ignored unregistered telemetry event: {event_name}")
            return False

        # Sanitize metadata to avoid PII
        clean_meta = {}
        if metadata and isinstance(metadata, dict):
            for k, v in metadata.items():
                if k in ("step", "mode", "section", "skill", "duration_seconds", "question_id", "flag_reason"):
                    clean_meta[k] = v

        await db.log_telemetry_event(event_name, user_id=user_id, metadata=clean_meta)
        return True

    def get_summary(self) -> dict[str, int]:
        """Returns aggregate event counts."""
        return db.get_telemetry_summary()


telemetry = TelemetryService()
