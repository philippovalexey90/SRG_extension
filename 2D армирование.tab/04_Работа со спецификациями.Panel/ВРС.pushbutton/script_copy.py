# -*- coding: utf-8 -*-

# Imports
import clr
from pyrevit import forms, script, revit, DB, UI
from Autodesk.Revit.DB import *
import wpf
from System import Windows

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# CustomImports
from Snippets._selection import get_selected_elements_simple, get_selected_schedule, check_schedule_combination
from Snippets._work_with_spek import get_master_schedule, getElementsFromSchedule, generateScheduleParameterNames, isParameterValueZeroForElements, updateFieldVisibility

# Инициализируем логгер pyRevit для вывода ошибок
logger = script.get_logger()
output = script.get_output()

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = doc.ActiveView


# Получаем список элементов вашей функцией
selection = get_selected_elements_simple(uidoc)
# Передаем результат в новую функцию
schedule = get_selected_schedule(selection, active_view)


print(schedule)
print(schedule.Name)


if schedule:
    if check_schedule_combination(schedule.Name):
        if isinstance(schedule, DB.ScheduleSheetInstance):
            master_schedule = get_master_schedule(schedule)
        else:
            master_schedule = schedule

        elements_in_schedule = getElementsFromSchedule(master_schedule)
        # Генерируем массив параметров для проверки (56 штук)
        target_parameters = generateScheduleParameterNames()
        hidden_count = 0
        shown_count = 0
        # Открываем одну общую транзакцию для максимальной скорости работы
        with revit.Transaction("pyRevit: Оптимизация видимости столбцов"):
            try:

                for param_name in target_parameters:
                    # Проверяем, пустой ли столбец для всей группы элементов
                    is_empty = isParameterValueZeroForElements(elements_in_schedule, param_name)
                    # Обновляем видимость: скрываем, если пустой (is_empty == True)
                    is_changed = updateFieldVisibility(master_schedule, param_name, should_hide=is_empty)
                    if is_changed:
                        if is_empty:
                            hidden_count += 1
                        else:
                            shown_count += 1
                # Отображаем результаты работы
                output.print_md("## 🎉 Оптимизация спецификации завершена!")
                print("Спецификация: '{}'".format(active_view.Name))
                print("-" * 50)
                print("Автоматически скрыто пустых столбцов (ноль): {}".format(hidden_count))
                print("Автоматически отображено столбцов с данными: {}".format(shown_count))
                print("-" * 50)
            except Exception as ex:
                logger.error("Критический сбой оптимизации: {}".format(str(ex)))


    else:
        print("Проверка НЕ пройдена для имени: " + str(schedule.Name))


