"""
Ваша команда та ви розробляєте систему входу для веб-додатка,
і вам потрібно реалізувати тести на функцію для логування подій в системі входу.
Дано функцію, напишіть набір тестів для неї.
"""
import logging
import unittest


def log_event(username: str, status: str):
    """
    Логує подію входу в систему.

    username: Ім'я користувача, яке входить в систему.

    status: Статус події входу:

    * success - успішний, логується на рівні інфо
    * expired - пароль застаріває і його слід замінити, логується на рівні warning
    * failed  - пароль невірний, логується на рівні error
    """
    log_message = f"Login event - Username: {username}, Status: {status}"

    # Створення та налаштування логера
    logging.basicConfig(
        filename='login_system.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
        )
    logger = logging.getLogger("log_event")

    # Логування події
    if status == "success":
        logger.info(log_message)
    elif status == "expired":
        logger.warning(log_message)
    else:
        logger.error(log_message)


class TestLogEvent(unittest.TestCase):

    def test_sainz_podium_logs_info(self):
        sainz_driver = "carlos_sainz_underrated"

        with self.assertLogs("log_event", level="INFO") as race_telemetry:
            log_event(sainz_driver, "success")

        self.assertEqual(len(race_telemetry.records), 1)
        checkered_flag_record = race_telemetry.records[0]
        self.assertEqual(checkered_flag_record.levelno, logging.INFO)
        self.assertIn(f"Username: {sainz_driver}", checkered_flag_record.message)
        self.assertIn("Status: success", checkered_flag_record.message)

    def test_stroll_Q1_logs_warning(self):
        stroll_notA_driver = "stroll_crushes"

        with self.assertLogs("log_event", level="WARNING") as race_telemetry:
            log_event(stroll_notA_driver, "expired")

        self.assertEqual(len(race_telemetry.records), 1)
        pit_wall_warning = race_telemetry.records[0]
        self.assertEqual(pit_wall_warning.levelno, logging.WARNING)
        self.assertIn(f"Username: {stroll_notA_driver}", pit_wall_warning.message)
        self.assertIn("Status: expired", pit_wall_warning.message)

    def test_mazepin_into_the_wall_logs_error(self):
        mazepin_shit_driver = "rusnya_mazepin"

        with self.assertLogs("log_event", level="ERROR") as race_telemetry:
            log_event(mazepin_shit_driver, "failed")

        self.assertEqual(len(race_telemetry.records), 1)
        crash_report = race_telemetry.records[0]
        self.assertEqual(crash_report.levelno, logging.ERROR)
        self.assertIn(f"Username: {mazepin_shit_driver}", crash_report.message)
        self.assertIn("Status: failed", crash_report.message)


    def test_unknown_flag_falls_back_to_error(self):
        safety_car_driver = "rain_tires"

        with self.assertLogs("log_event", level="ERROR") as race_telemetry:
            log_event(safety_car_driver, "champion")

        self.assertEqual(race_telemetry.records[0].levelno, logging.ERROR)

    def test_race_report_message_format(self):
        verstappen_driver = "max_verstappen"

        with self.assertLogs("log_event", level="INFO") as race_telemetry:
            log_event(verstappen_driver, "success")

        self.assertEqual(
            race_telemetry.records[0].message,
            f"Login event - Username: {verstappen_driver}, Status: success",
        )


if __name__ == "__main__":
    unittest.main()
