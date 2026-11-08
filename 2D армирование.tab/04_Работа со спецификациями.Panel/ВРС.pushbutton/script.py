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
from Snippets._work_with_spek import getScheduleColumnsStatus, generateScheduleParameterNames, scheduleParameters, get_master_schedule, getElementsFromSchedule, isParameterValueZeroForElements, updateFieldVisibility

# Инициализируем логгер pyRevit для вывода ошибок
logger = script.get_logger()
output = script.get_output()

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = doc.ActiveView

# Local Functions


# -*- coding: utf-8 -*-

def print_columns_status(columns_status, target_n=None, target_d=None):
    """
    Выводит статус столбцов с фильтрацией по классу стали N и диаметру D.
    Сводный анализ в конце по-прежнему считается по всей спецификации.

    :param columns_status: Словарь состояния полей {Имя_Параметра: Скрывать_Ли}
    :param target_n: Номер класса стали (например: 2, "2", "N2" или None для всех)
    :param target_d: Диаметр арматуры (например: 8, "8", "D8" или None для всех)
    """
    if not columns_status:
        print("Словарь columns_status пуст.")
        return

    # --- Подготовка фильтра N ---
    str_target_n = None
    if target_n is not None:
        str_target_n = "N{}".format(str(target_n).strip().upper().replace("N", ""))

    # --- Подготовка фильтра D ---
    str_target_d = None
    if target_d is not None:
        str_target_d = "D{}".format(str(target_d).strip().upper().replace("D", ""))

    # Красивый заголовок фильтров
    f_n_text = str_target_n if str_target_n else "Все"
    f_d_text = str_target_d if str_target_d else "Все"

    print("\n" + "=" * 60)
    print(" 🔎 СТАТУС СТОЛБЦОВ С ФИЛЬТРАЦИЕЙ | Класс (N): {} | Диаметр (D): {}".format(f_n_text, f_d_text))
    print("=" * 60)

    # Надежная сортировка ключей по числовому значению диаметра
    try:
        sorted_keys = sorted(
            columns_status.keys(),
            key=lambda x: int(x.split('-')[0].replace('D', ''))
        )
    except Exception:
        sorted_keys = sorted(columns_status.keys())

    # Сбор глобальной аналитики
    active_d = set()
    active_n = set()
    hidden_params = []
    shown_params = []

    printed_count = 0

    for param_name in sorted_keys:
        should_hide = columns_status[param_name]

        # Разбираем имя (например, "D12-N3" -> ["D12", "N3"])
        parts = param_name.split('-')
        d_part = parts[0]
        id_d = int(d_part.replace('D', ''))
        n_part = parts[1]

        # Накапливаем общую аналитику для финала
        if should_hide:
            hidden_params.append(param_name)
        else:
            shown_params.append(param_name)
            active_d.add(id_d)
            active_n.add(n_part)

        # ПРОВЕРКА ФИЛЬТРОВ (Логика совпадения условий)
        match_n = (str_target_n is None) or (n_part == str_target_n)
        match_d = (str_target_d is None) or (d_part == str_target_d)

        if match_n and match_d:
            status_text = "❌ СКРЫТЬ (нули)" if should_hide else "✅ ОСТАВИТЬ (есть данные)"
            print("  {:<12} -> {}".format(param_name, status_text))
            printed_count += 1

    if printed_count == 0:
        print("  [Нет параметров, соответствующих заданным фильтрам D и N]")

    # ========================================================
    #  БЛОК СВОДНОЙ АНАЛИТИКИ (РАСЧЕТ ПО ВСЕМ 56 СТОЛБЦАМ)
    # ========================================================
    print("\n" + "=" * 60)
    print(" СВОДНЫЙ АНАЛИЗ ВСЕЙ ВЕДОМОСТИ (ПО ВСЕМ КЛАССАМ И ДИАМЕТРАМ)")
    print("=" * 60)

    # 1. Анализ диаметров (D)
    print("📊 АКТИВНЫЕ ДИАМЕТРЫ (D):")
    if active_d:
        sorted_active_d = sorted(list(active_d))
        str_active_d = ", ".join(["Ø{}".format(d) for d in sorted_active_d])
        print("  • Есть данные в проекте: [{}]".format(str_active_d))
    else:
        print("  • Есть данные в проекте: [Все диаметры пустые]")

    # 2. Анализ классов стали (N)
    print("\n🏗️ АКТИВНЫЕ КЛАССЫ СТАЛИ (N):")
    if active_n:
        sorted_active_n = sorted(list(active_n))
        str_active_n = ", ".join(sorted_active_n)
        print("  • Есть данные в проекте: [{}]".format(str_active_n))
    else:
        print("  • Есть данные в проекте: [Нет активных классов стали]")

    # 3. Итоговый баланс
    print("\n⚖️ ОБЩИЙ БАЛАНС СТОЛБЦОВ В ТАБЛИЦЕ:")
    print("  • Будет выведено на лист (с данными) : {} столбцов".format(len(shown_params)))
    print("  • Будет свернуто/скрыто (все нули) : {} столбцов".format(len(hidden_params)))
    print("=" * 60 + "\n")


# Main

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
        # target_parameters = generateScheduleParameterNames()
        hidden_count = 0
        shown_count = 0
        # 💥 СЛОВАРЬ ДЛЯ ТРИГГЕРОВ: Имя_Параметра -> Скрывать_Ли (по умолчанию True - скрыть)
        # Мы будем менять True на False, если найдем хоть один элемент с весом > 0
        # Если элементов какого-то диаметра вообще нет в модели, этот столбец гарантированно закроется.
        target_parameters = generateScheduleParameterNames()
        columns_status = {param_name: True for param_name in target_parameters}
        # print_columns_status(columns_status)

        try:
            # 🚀 ШАГ 1: Получаем финальный статус столбцов через новую функцию (чистое чтение)
            columns_status = getScheduleColumnsStatus(elements_in_schedule)


            # ШАГ 2: Управление видимостью полей на основе собранного словаря
            # Открываем транзакцию строго под запись изменений
            with revit.Transaction("pyRevit: Оптимизация видимости столбцов"):
                # Перебираем все найденные столбцы и их финальные вердикты
                for param_name, should_hide in columns_status.items():
                    is_changed = updateFieldVisibility(master_schedule, param_name, should_hide=should_hide)
                    if is_changed:
                        if should_hide:
                            hidden_count += 1
                        else:
                            shown_count += 1

                # Отображаем результаты работы (вынесено за пределы циклов!)
                output.print_md("## 🎉 Оптимизация спецификации завершена!")
                print("Спецификация: '{}'".format(master_schedule.Name))
                print("-" * 50)
                print("Автоматически скрыто пустых столбцов (ноль): {}".format(hidden_count))
                print("Автоматически отображено столбцов с данными: {}".format(shown_count))
                print("-" * 50)

        except Exception as ex:
            logger.error("Критический сбой оптимизации: {}".format(str(ex)))
    else:
        print("Проверка НЕ пройдена для имени: " + str(schedule.Name))























