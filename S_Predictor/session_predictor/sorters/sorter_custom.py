from .abstract_sorter import AbstractSorter
import xml.etree.ElementTree as ET
from django.conf import settings

class SorterCustom(AbstractSorter):
    def SorterInit(self):
        tree = ET.parse(f"{settings.SORTERS_DATA}/SortersData.xml")
        root = tree.getroot()
        result = root.find(f"{self.field}").text
        if (result == None):
            return ""
        return result

    def SorterApply(self):
        tree = ET.parse(f"{settings.SORTERS_DATA}/SortersData.xml")
        root = tree.getroot()
        node = root.find(f"{self.field}")
        if ((node.text == None) or (node.text == "")):
            node.text = "⭣"
            return tree.write(f"{settings.SORTERS_DATA}/SortersData.xml")
        if(node.text == "⭣"):
            node.text = "⭡"
            return tree.write(f"{settings.SORTERS_DATA}/SortersData.xml")
        if(node.text == "⭡"):
            node.text = ""
            return tree.write(f"{settings.SORTERS_DATA}/SortersData.xml")
