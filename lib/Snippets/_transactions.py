# -*- coding: utf-8 -*-

# Imports
import clr
# clr.AddReference('System')

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
from Autodesk.Revit.UI import *
from pyrevit import revit, DB, UI, script

# Variables
logger = script.get_logger()
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
        # print("Транзакция успешно завершена. Обновлено элементов: {}".format(counter))

    except Exception as e:
        # Если произошла любая ошибка, откатываем изменения, чтобы не испортить модель
        t.RollBack()
        print("Ошибка внутри транзакции! Изменения отменены. Ошибка: {}".format(str(e)))

def delete_selected_schedule(doc, element_id):
    """
    Удаляет выбранную спецификацию из проекта Revit
    вместе с её размещением на листе.
    """

    element = doc.GetElement(element_id)

    if not isinstance(element, ScheduleSheetInstance):
        print(
            'Ошибка: выбранный элемент не является спецификацией на листе'
        )
        return

    schedule_id = element.ScheduleId

    t = Transaction(doc, "Удалить спецификацию")

    try:
        t.Start()

        # Удаляем саму спецификацию из проекта.
        # Размещение на листе удаляется вместе с ней.
        doc.Delete(schedule_id)

        t.Commit()

    except Exception:
        t.RollBack()
        raise

def CopyStructuralParameters(doc, walls, foundations, floors, framing, columns):
    """
    Проходит по всем конструктивным элементам, считывает значения из исходных параметров
    и записывает их в целевые параметры в рамках одной транзакции.
    """
    # Объединяем все 5 списков в один плоский массив для итерации
    all_elements = []
    all_elements.extend(walls)
    all_elements.extend(foundations)
    all_elements.extend(floors)
    all_elements.extend(framing)
    all_elements.extend(columns)

    total_count = len(all_elements)
    if total_count == 0:
        print("Нет элементов для обработки.")
        return

    # Открываем одну общую транзакцию на всю операцию
    t = Transaction(doc, "Перенос параметров конструкций")
    t.Start()

    success_section = 0
    success_mark = 0

    try:
        for elem in all_elements:
            # --- 1. ПЕРЕНОС: Орг.КомплектЧертежей -> • Раздел ---
            p_source_section = elem.LookupParameter('Орг.КомплектЧертежей')
            p_target_section = elem.LookupParameter('• Раздел')

            if p_source_section and p_target_section and not p_target_section.IsReadOnly:
                # Получаем значение как текст (подходит для текстовых параметров)
                val_section = p_source_section.AsString()
                if val_section:
                    p_target_section.Set(val_section)
                    success_section += 1
            else:
                if not p_source_section:
                    logger.warning("У элемента ID: {} отсутствует параметр 'Орг.КомплектЧертежей'".format(elem.Id))
                elif p_target_section and p_target_section.IsReadOnly:
                    logger.warning("Параметр '• Раздел' у элемента ID: {} закрыт для записи".format(elem.Id))

            # --- 2. ПЕРЕНОС: Мрк.МаркаКонструкции -> • Марка конструкции ---
            p_source_mark = elem.LookupParameter('Мрк.МаркаКонструкции')
            p_target_mark = elem.LookupParameter('• Марка конструкции')

            if p_source_mark and p_target_mark and not p_target_mark.IsReadOnly:
                val_mark = p_source_mark.AsString()
                if val_mark:
                    p_target_mark.Set(val_mark)
                    success_mark += 1
            else:
                if not p_source_mark:
                    logger.warning("У элемента ID: {} отсутствует параметр 'Мрк.МаркаКонструкции'".format(elem.Id))
                elif p_target_mark and p_target_mark.IsReadOnly:
                    logger.warning("Параметр '• Марка конструкции' у элемента ID: {} закрыт для записи".format(elem.Id))

        # Фиксируем изменения в модели
        t.Commit()

        # Выводим красивый текстовый отчет в консоль
        print("\n" + "=" * 50)
        print("ОТЧЕТ О ПЕРЕНОСЕ ПАРАМЕТРОВ:")
        print("=" * 50)
        print("Всего обработано элементов: {}".format(total_count))
        print("Успешно заполнено параметров '• Раздел': {}".format(success_section))
        print("Успешно заполнено параметров '• Марка конструкции': {}".format(success_mark))
        print("=" * 50 + "\n")

    except Exception as ex:
        # Если внутри цикла произошел критический сбой, полностью откатываем транзакцию
        t.RollBack()
        logger.error("Критическая ошибка при переносе параметров: {}".format(str(ex)))