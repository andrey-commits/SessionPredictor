from .abstract_filter import AbstractFilter
import xml.etree.ElementTree as ET
from django.conf import settings



class FilterFeature(AbstractFilter):
    def FilterInit(self):
        tree = ET.parse(f"{settings.FILTERS_DATA}/FiltersData.xml")
        root = tree.getroot()
        result = root.find(f"{self.field}").text
        if(result == None):
            return ""
        return result

    def FilterApply(self, value):
        tree = ET.parse(f"{settings.FILTERS_DATA}/FiltersData.xml")
        root = tree.getroot()
        node = root.find(f"{self.field}")
        if (node.text != value):
            node.text = value
            tree.write(f"{settings.FILTERS_DATA}/FiltersData.xml")
