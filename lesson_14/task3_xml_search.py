"""
Завдання 3:
Для файла ideas_for_test/work_with_xml/groups.xml створіть функцію пошуку по group/number
і повернення значення timingExbytes/incoming результат виведіть у консоль через логер
на рівні інфо.
"""
import logging
import os
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XML_FILE = os.path.join(BASE_DIR, "groups.xml")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("xml_search")


def find_incoming_by_group_number(group_number):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    for group in root.findall("group"):
        number = group.find("number")
        if number is not None and number.text == str(group_number):
            incoming = group.find("timingExbytes/incoming")
            return incoming.text if incoming is not None else None
    return None


tree = ET.parse(XML_FILE)
root = tree.getroot()
for group in root.findall("group"):
    group_number = group.findtext("number")
    incoming_value = find_incoming_by_group_number(group_number)
    logger.info(f"Group {group_number}: timingExbytes/incoming = {incoming_value}")
