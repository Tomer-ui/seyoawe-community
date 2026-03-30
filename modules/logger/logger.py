import logging

logger = logging.getLogger(__name__)


class Logger:
    """Simple logging module — writes messages to the workflow log."""

    def log(self, input_data, context, **kwargs):
        message = input_data.get("message", "")
        level = input_data.get("level", "info").lower()

        log_fn = {
            "info": logger.info,
            "warning": logger.warning,
            "error": logger.error,
        }.get(level, logger.info)

        log_fn(message)
        return {"status": "ok", "message": message, "level": level}
