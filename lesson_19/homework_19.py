"""Check heartbeat intervals for one feed in a newest-first log."""

import logging
from datetime import datetime
from pathlib import Path


KEY = "Key TSTFEED0300|7E3E|0400"
TIMESTAMP = "Timestamp "


def analyze_heartbeats(
    input_path=Path(__file__).with_name("hblog.txt"),
    output_path=Path(__file__).with_name("hb_test.log"),
):
    """Write intervals above 31 seconds to a log and return its path."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    logger = logging.Logger("heartbeat_analysis", level=logging.WARNING)
    handler = logging.FileHandler(output_path, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(handler)

    try:
        newer = None
        with input_path.open(encoding="utf-8-sig") as source:
            for line_number, line in enumerate(source, start=1):
                if KEY not in line:
                    continue
                position = line.find(TIMESTAMP)
                if position == -1:
                    raise ValueError(f"Missing Timestamp on line {line_number}")
                time_text = line[position + len(TIMESTAMP):][:8]
                timestamp = datetime.strptime(time_text, "%H:%M:%S")

                if newer is not None:
                    newer_text, newer_timestamp, newer_line = newer
                    seconds = int((newer_timestamp - timestamp).total_seconds()) % 86400
                    message = (
                        "Timestamp %s | heartbeat %d seconds since %s "
                        "(source line %d)"
                    )
                    if seconds >= 33:
                        logger.error(message, newer_text, seconds, time_text, newer_line)
                    elif seconds > 31:
                        logger.warning(message, newer_text, seconds, time_text, newer_line)
                newer = (time_text, timestamp, line_number)
    finally:
        logger.removeHandler(handler)
        handler.close()

    return output_path


if __name__ == "__main__":
    print(f"Heartbeat analysis saved to {analyze_heartbeats()}")