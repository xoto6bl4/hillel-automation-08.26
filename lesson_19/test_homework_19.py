"""Regression tests for heartbeat interval analysis."""

import tempfile
import unittest
from pathlib import Path

from homework_19 import KEY, analyze_heartbeats


class HeartbeatAnalysisTests(unittest.TestCase):
    def test_thresholds_filtering_midnight_and_repeat_run(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "hblog.txt"
            output = Path(folder) / "hb_test.log"
            source.write_text(
                "".join(
                    f"Timestamp {time} {key}\n"
                    for time, key in [
                        ("00:02:13", KEY),
                        ("00:02:12", "Key different"),
                        ("00:01:38", KEY),  # 35: ERROR
                        ("00:01:05", KEY),  # 33: ERROR
                        ("00:00:33", KEY),  # 32: WARNING
                        ("00:00:02", KEY),  # 31: normal
                        ("23:59:32", KEY),  # 30 across midnight: normal
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(analyze_heartbeats(source, output), output)
            expected = [
                "ERROR Timestamp 00:02:13 | heartbeat 35 seconds since 00:01:38 (source line 1)",
                "ERROR Timestamp 00:01:38 | heartbeat 33 seconds since 00:01:05 (source line 3)",
                "WARNING Timestamp 00:01:05 | heartbeat 32 seconds since 00:00:33 (source line 4)",
            ]
            self.assertEqual(output.read_text(encoding="utf-8").splitlines(), expected)
            analyze_heartbeats(source, output)
            self.assertEqual(output.read_text(encoding="utf-8").splitlines(), expected)


if __name__ == "__main__":
    unittest.main()