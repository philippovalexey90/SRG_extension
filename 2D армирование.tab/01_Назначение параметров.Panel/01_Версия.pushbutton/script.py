# -*- coding: utf-8 -*-
__title__   = "Версия v 0.5"
__doc__ = """Version = 0.5
Date    = 23.10.2026
IronPython 2.7
logger = script.get_logger()
Занесение параметра Орг.КомплектЧертежей в Раздел
Занесение параметра Мрк.МаркаКонструкции в Марка конструкции
_____________________________________________________________________
Автор: Филиппов Алексей"""



doc = __revit__.ActiveUIDocument.Document

# CustomImports
from Snippets._selection import print_structural_elements_report, FEC_AllStructBuiltInCat_in_doc, FEC_ElementsByCategories
from Snippets._transactions import CopyStructuralParameters


target_cats = [
    "OST_Walls",
    "OST_StructuralFoundation",
    "OST_Floors",
    "OST_StructuralFraming",
    "OST_StructuralColumns"
    "OST_Rebar"
    "OST_GenericModel"
]

roof_cats = ["OST_Roofs"]
roof_dict = FEC_ElementsByCategories(doc, roof_cats)

# Извлекаем сам список элементов крыш по ключу словаря
roof_elements = roof_dict.get("OST_Roofs", [])

if roof_elements:
    print("В модели присутствует категория крыша (элементов: {}). Работа скрипта остановлена.".format(len(roof_elements)))
else:
    CopyStructuralParameters(doc, FEC_ElementsByCategories(doc, target_cats))

