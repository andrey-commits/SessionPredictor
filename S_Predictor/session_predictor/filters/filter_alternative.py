from .abstract_filter import AbstractFilter
import xml.etree.ElementTree as ET
from django.conf import settings
import datetime



class FilterAlternativeNumber(AbstractFilter):
    def FilterInit(self):
        tree = ET.parse(f"{settings.FILTERS_DATA}/FiltersData.xml")
        root = tree.getroot()
        try:
            result = int(root.find(f"{self.field}").text)
        except:
            return ""
        return result

    def FilterApply(self, value):
        tree = ET.parse(f"{settings.FILTERS_DATA}/FiltersData.xml")
        root = tree.getroot()
        node = root.find(f"{self.field}")
        try:
            value = str(value)
        except:
            return
        if (node.text != value):
            node.text = value
            tree.write(f"{settings.FILTERS_DATA}/FiltersData.xml")

class FilterAlternativeDate(AbstractFilter):
    def FilterInit(self):
        tree = ET.parse(f"{settings.FILTERS_DATA}/FiltersData.xml")
        root = tree.getroot()
        try:
            result = datetime.datetime.strptime(root.find(f"{self.field}").text, '%Y-%m-%d').date()
        except:
            return ""
        return str(result)

    def FilterApply(self, value):
        tree = ET.parse(f"{settings.FILTERS_DATA}/FiltersData.xml")
        root = tree.getroot()
        node = root.find(f"{self.field}")
        try:
            value = str(value)
        except:
            return
        if (node.text != value):
            node.text = value
            tree.write(f"{settings.FILTERS_DATA}/FiltersData.xml")