# -*- coding: utf-8 -*-
__title__   = "Версия v 0.2"
__doc__ = """Version = 0.2
Date    = 23.10.2026
IronPython 2.7
logger = script.get_logger()
Занесение параметра Орг.КомплектЧертежей в Раздел
Занесение параметра Мрк.МаркаКонструкции в Марка конструкции
_____________________________________________________________________
Автор: Филиппов Алексей"""



doc = __revit__.ActiveUIDocument.Document

# CustomImports
from Snippets._selection import print_structural_elements_report, FEC_AllStructBuiltInCat_in_doc
from Snippets._transactions import CopyStructuralParameters


CopyStructuralParameters(doc, *FEC_AllStructBuiltInCat_in_doc(doc))