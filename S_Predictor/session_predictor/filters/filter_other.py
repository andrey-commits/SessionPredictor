from .abstract_filter import AbstractFilter
import xml.etree.ElementTree as ET
from django.conf import settings



class FilterOther(AbstractFilter):
    def FilterInit(self, storage ="FiltersData.xml"):
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(f"{settings.FILTERS_DATA}/{storage}",parser=parser)
        root = tree.getroot()
        result = root.find(f"{self.field}").text
        if(result == None):
            return ""
        return result

    def FilterApply(self, value, storage = "FiltersData.xml"):
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(f"{settings.FILTERS_DATA}/{storage}",parser=parser)
        root = tree.getroot()
        node = root.find(f"{self.field}")
        if (node.text != value):
            node.text = value
            tree.write(f"{settings.FILTERS_DATA}/{storage}",encoding="utf-8")
