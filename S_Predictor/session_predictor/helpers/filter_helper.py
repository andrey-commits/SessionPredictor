import xml.etree.ElementTree as ET
from django.conf import settings

def FilterCleaner():
    tree = ET.parse(f"{settings.FILTERS_DATA}/FiltersData.xml")
    root = tree.getroot()
    for node in root.iter():
        node.text = ""
    tree.write(f"{settings.FILTERS_DATA}/FiltersData.xml")