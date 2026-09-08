# -*- coding: utf-8 -*-

# Imports
import clr
# clr.AddReference('System')



from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
from Autodesk.Revit.UI import *
from pyrevit import revit, DB, UI

# Variables

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

from Autodesk.Revit.DB import Transaction


def write_total_cnt_to_revit(updated_SHP, doc):
    """
    Открывает одну общую транзакцию, проходит по словарю со вложенными списками
    и записывает '• Расчетное число' в каждый элемент Revit.
    """
    # Создаем и стартуем транзакцию
    t = Transaction(doc, "Запись расчетного числа")
    t.Start()

    try:
        counter = 0
        for key, value_list in updated_SHP.items():
            for inner_item in value_list:
                # Распаковываем [элемент, total_cnt]
                elem, cnt = inner_item

                # Ищем параметр у элемента Revit и устанавливаем значение
                # (Предполагаем, что параметр текстовый или числовой.
                # Для целых чисел используется Set(), для вещественных - Set(), для текста - Set())
                param = elem.LookupParameter('• Количество')
                if param and not param.IsReadOnly:
                    param.Set(cnt)
                    counter += 1
                else:
                    print("Предупреждение: Параметр не найден или доступен только для чтения у ID: {}".format(elem.Id))

        # Если всё прошло успешно, фиксируем изменения
        t.Commit()
        print("Транзакция успешно завершена. Обновлено элементов: {}".format(counter))

    except Exception as e:
        # Если произошла любая ошибка, откатываем изменения, чтобы не испортить модель
        t.RollBack()
        print("Ошибка внутри транзакции! Изменения отменены. Ошибка: {}".format(str(e)))
