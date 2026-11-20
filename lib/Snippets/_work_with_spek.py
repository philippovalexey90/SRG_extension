# -*- coding: utf-8 -*-

# Imports
import clr
import System
clr.AddReference('System')
from System.Collections.Generic import List as NetList



from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
from Autodesk.Revit.UI import *
from pyrevit import revit, DB, UI, forms, script

# CustomImports
from Snippets._selection import universalLookupParameter

# Инициализируем логгер pyRevit для вывода ошибок
logger = script.get_logger()
output = script.get_output()

# Variables

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# Functions

def get_master_schedule(sheet_schedule_instance):
    """
    Принимает ScheduleSheetInstance (спецификацию на листе)
    и возвращает основной объект спецификации (ViewSchedule).
    """
    # Получаем документ, в котором находится элемент
    doc = sheet_schedule_instance.Document

    # Получаем ID мастер-спецификации
    master_schedule_id = sheet_schedule_instance.ScheduleId

    # Возвращаем сам объект спецификации
    return doc.GetElement(master_schedule_id)

def getElementsFromSchedule(master_schedule):
    """
    Принимает на вход объект спецификации (ViewSchedule).
    Возвращает список элементов (Element), отображаемых в этой спецификации.
    """
    # Получаем текущий документ из глобального контекста
    doc = __revit__.ActiveUIDocument.Document

    # 1. Проверяем, что переданный объект — это спецификация
    # В Revit API спецификации имеют тип класса ViewSchedule
    if not isinstance(master_schedule, DB.ViewSchedule):
        forms.alert(
            "Переданный объект не является спецификацией Revit!",
            title="Ошибка типа данных"
        )
        return []

    try:
        # 2. Собираем элементы, проходящие через фильтр данной спецификации
        elements_in_schedule = DB.FilteredElementCollector(doc, master_schedule.Id) \
            .WhereElementIsNotElementType() \
            .ToElements()

        # Превращаем коллекцию .NET в обычный плоский список Python
        return list(elements_in_schedule)

    except Exception as ex:
        logger.error("Ошибка при сборе элементов из спецификации '{}': {}".format(master_schedule.Name, str(ex)))
        return []

def scheduleParameters(elem):
    """
    Генерирует список имен параметров для спецификации арматуры
    по шаблону: "D{Диаметр}-N{Класс_стали}"

    :return: Список строк (массив имен параметров)
    """
    # Исходные списки значений согласно вашему сортаменту

    diameter = universalLookupParameter(elem, "• Диаметр")
    steel_class = universalLookupParameter(elem, "• Номер класса стали")
    mass = elem.LookupParameter("• Масса")

    # print("• Диаметр: {}, • Номер класса стали: {} ".format(diameter, steel_class))

    if diameter and steel_class:
        # Получаем значения как текст без лишних единиц измерения проекта
        # Например, AsValueString() вернет "8" или "8 мм", убираем " мм" если нужно
        d_val = diameter.AsValueString().replace(" мм", "").strip()

        # Для целых чисел (класс стали) можно использовать AsInteger() или AsValueString()
        c_val = steel_class.AsValueString().strip()

        # Собираем и возвращаем одну строку
        name = "D{}-N{}".format(d_val, c_val)
        return name, mass

    return None

def generateScheduleParameterNames():
    """
    Генерирует полный список имен всех параметров для проверки ведомости.
    Включает параметры арматуры (D-N), поля V101-V180 и все итоговые/сводные поля.
    """

    # 1. Генерация стандартных полей сортамента (18 диаметров * 4 класса = 72 параметра)
    diameters = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40]
    steel_classes = [1, 2, 3, 4]

    all_parameters = ["D{}-N{}".format(d, c) for d in diameters for c in steel_classes]

    # 2. Генерация полей "V101" ... "V180" (всего 80 полей)
    v_parameters = ["V{}".format(i) for i in range(101, 181)]
    all_parameters.extend(v_parameters)

    # 3. Добавление итоговых и сводных полей ведомости
    total_fields = [
        "#V - Итого N1",
        "#V - Итого N2",
        "#V - Итого N3",
        "#V - Итого N4",
        "#V - Всего N1-N4",
        "#V - Итого - V101-V120",
        "#V - Итого - V121-V140",
        "#V - Итого - V141-V160",
        "#V - Итого - V161-V180",
        "#V - Всего - V101-V180"
    ]
    all_parameters.extend(total_fields)

    return all_parameters

def isParameterValueZeroForElements(parameter_mass):
    """
    Числовой триггер: возвращает False (НЕ скрывать), если масса строго больше нуля.
    Работает через получение системного числа (AsDouble), полностью игнорируя текст.
    """
    if not parameter_mass:
        return True

    # 1. Считываем точное число из базы данных Revit (внутренние единицы)
    val_double = parameter_mass.AsDouble()

    if val_double is not None:
        # В Revit API масса 0.000000... может иметь микропогрешность,
        # поэтому проверяем, что число строго больше очень маленького порога (1e-6)
        if val_double > 1e-6:
            # Нашли реальный вес! Сразу возвращаем False (столбец НЕ скрывать)
            return False

    # 2. Резервный вариант (на случай, если параметр в семействе заведен как текст Text)
    else:
        val_string = parameter_mass.AsString()
        if val_string and val_string.strip() != "":
            # Очищаем строку от пробелов и проверяем, что это не просто "0" или "0.00"
            clean_str = val_string.replace(",", ".").replace(" кг", "").strip()
            try:
                if float(clean_str) > 1e-6:
                    return False
            except ValueError:
                # Если там написан чистый текст (не число), оставляем столбец видимым
                return False

    # Если значение равно нулю или пусто
    return True

def getScheduleColumnsStatus(elements_in_schedule):
    """
    Анализирует группу элементов спецификации и формирует финальный статус для каждого столбца,
    включая автоматическое отображение итоговых и сводных полей.

    :param elements_in_schedule: Список элементов, полученных из спецификации
    :return: Словарь columns_status {Имя_Параметра: Скрывать_Ли (True/False)}
    """
    # 1. Генерируем полный список из всех 162 возможных параметров
    target_parameters = generateScheduleParameterNames()

    # Инициализируем словарь: по умолчанию все столбцы скрыты (True)
    columns_status = {param_name: True for param_name in target_parameters}

    if not elements_in_schedule:
        return columns_status

    # 2. Основной цикл анализа элементов модели
    for elem in elements_in_schedule:
        # Получаем параметры конкретного элемента
        parameter_name, parameter_mass = scheduleParameters(elem)

        if parameter_name and parameter_mass:
            # Проверяем текущий элемент на ноль числовой функцией AsDouble
            is_empty = isParameterValueZeroForElements(parameter_mass)

            # Если мы нашли НЕ пустой элемент (is_empty == False)
            if not is_empty:
                # Столбец самого диаметра навсегда оставляем видимым
                columns_status[parameter_name] = False

                # --- ДОПОЛНИТЕЛЬНАЯ ЛОГИКА ДЛЯ ИТОГОВЫХ ПОЛЕЙ ---
                # Извлекаем номер класса стали из имени параметра (например, из "D12-N3" заберем "3")
                try:
                    if "-N" in parameter_name:
                        steel_class_num = parameter_name.split("-N")[1].strip()

                        # Собираем точное имя итогового параметра для этого класса
                        total_param_name = "#V - Итого N{}".format(steel_class_num)

                        # Оставляем этот итог и общий сводный столбец видимыми
                        if total_param_name in columns_status:
                            columns_status[total_param_name] = False

                        columns_status["#V - Всего N1-N4"] = False
                except Exception:
                    # Защита на случай, если имя параметра имеет нестандартный формат
                    pass
            else:
                # Если параметр пустой у текущего элемента, проверяем,
                # не был ли он уже открыт (False) каким-то из предыдущих элементов
                if columns_status.get(parameter_name) != False:
                    columns_status[parameter_name] = True

    return columns_status

def updateFieldVisibility(master_schedule, parameter_name, should_hide):
    """
    Находит столбец в спецификации и переключает его видимость.
    Возвращает True, если состояние столбца было реально изменено.
    """
    definition = master_schedule.Definition
    count_fields = definition.GetFieldCount()

    for i in range(count_fields):
        field = definition.GetField(i)

        # Проверяем совпадение по имени заголовка
        if field.GetName() == parameter_name:
            # Если нужно скрыть, и он еще не скрыт
            if should_hide and not field.IsHidden:
                field.IsHidden = True
                return True
            # Если нужно показать, и он сейчас скрыт
            elif not should_hide and field.IsHidden:
                field.IsHidden = False
                return True
            break
    return False


# def toggle_schedule_fields_visibility_1(schedule_element):
#     """
#     Принимает либо ViewSchedule, либо ScheduleSheetInstance.
#     Автоматически находит мастер-спецификацию и управляет видимостью полей:
#     скрывает полностью пустые столбцы и открывает заполненные.
#     """
#     # 1. ПРОВЕРКА ТИПА: Если это спецификация на листе, получаем мастер-спецификацию
#     if isinstance(schedule_element, DB.ScheduleSheetInstance):
#         master_schedule = get_master_schedule(schedule_element)
#     else:
#         master_schedule = schedule_element
#
#     # 2. Валидация: проверяем, что в итоге мы работаем с объектом ViewSchedule
#     if not master_schedule or not isinstance(master_schedule, DB.ViewSchedule):
#         print("Ошибка: Переданный объект не является спецификацией или ее экземпляром на листе.")
#         return False
#
#     doc = master_schedule.Document
#
#     # 3. Собираем элементы, отображаемые в спецификации
#     elements_in_schedule = DB.FilteredElementCollector(doc, master_schedule.Id) \
#         .WhereElementIsNotElementType() \
#         .ToElements()
#
#     schedule_definition = master_schedule.Definition
#     field_count = schedule_definition.GetFieldCount()
#
#     # 4. Открываем транзакцию для изменения свойств полей
#     with revit.Transaction("Оптимизация видимости полей спецификации"):
#
#         for i in range(field_count):
#             field = schedule_definition.GetField(i)
#
#             # Пропускаем скрытые по умолчанию технические поля при пустой спецификации
#             if field.IsHidden and not elements_in_schedule:
#                 continue
#
#             param_id = field.ParameterId
#             has_value = False
#
#             # Проверяем заполненность ячеек у элементов
#             for elem in elements_in_schedule:
#                 # УНИВЕРСАЛЬНЫЙ СПОСОБ: работает и в старых, и в новых версиях Revit
#                 if hasattr(elem, "GetParameterWithId"):
#                     param = elem.GetParameterWithId(param_id)
#                 else:
#                     param = elem.get_Parameter(param_id)  # Для Revit 2023 и ниже
#
#                 if param and param.HasValue:
#                     # Дополнительная проверка текстовых параметров на пустые строки
#                     if param.StorageType == DB.StorageType.String:
#                         if param.AsString() and param.AsString().strip():
#                             has_value = True
#                             break
#                     else:
#                         has_value = True
#                         break
#
#             # Меняем видимость столбца
#             if has_value:
#                 if field.IsHidden:
#                     field.IsHidden = False
#             else:
#                 if not field.IsHidden:
#                     field.IsHidden = True
#
#     return True
#
#
# def toggle_schedule_fields_visibility(schedule_element):
#     """
#     Принимает либо ViewSchedule, либо ScheduleSheetInstance.
#     Автоматически находит мастер-спецификацию и скрывает полностью пустые столбцы.
#     Совместима со ВСЕМИ версиями Revit (включая Revit 2019-2023).
#     """
#     # 1. Проверка типа объекта
#     if isinstance(schedule_element, DB.ScheduleSheetInstance):
#         master_schedule = get_master_schedule(schedule_element)
#     else:
#         master_schedule = schedule_element
#
#     if not master_schedule or not isinstance(master_schedule, DB.ViewSchedule):
#         print("Ошибка: Переданный объект не является спецификацией.")
#         return False
#
#     doc = master_schedule.Document
#
#     # 2. Собираем элементы в спецификации
#     elements_in_schedule = getElementsFromSchedule(master_schedule)
#
#     schedule_definition = master_schedule.Definition
#     field_count = schedule_definition.GetFieldCount()
#
#     # 3. Модификация полей в транзакции
#     with revit.Transaction("Оптимизация видимости полей спецификации"):
#
#         for i in range(field_count):
#             field = schedule_definition.GetField(i)
#
#             if field.IsHidden and not elements_in_schedule:
#                 continue
#
#             param_id = field.ParameterId  # Это ElementId
#             has_value = False
#
#             # Подготовка для Revit 2023 и ниже: определяем тип параметра
#             is_builtin = param_id.IntegerValue < 0
#             bip = System.Enum.ToObject(DB.BuiltInParameter, param_id.IntegerValue) if is_builtin else None
#
#             # Если параметр пользовательский (Shared), пытаемся получить его GUID для старых Revit
#             param_guid = None
#             if not is_builtin and not hasattr(DB.Element, "GetParameterWithId"):
#                 shared_param_element = doc.GetElement(param_id)
#                 if shared_param_element and hasattr(shared_param_element, "GuidValue"):
#                     param_guid = shared_param_element.GuidValue
#
#             # Проверяем заполненность ячеек у элементов
#             for elem in elements_in_schedule:
#                 param = None
#
#                 # Способ для Revit 2024+
#                 if hasattr(elem, "GetParameterWithId"):
#                     param = elem.GetParameterWithId(param_id)
#
#                 # Способ для Revit 2023 и ниже
#                 else:
#                     if is_builtin:
#                         param = elem.get_Parameter(bip)
#                     elif param_guid:
#                         param = elem.get_Parameter(param_guid)
#                     else:
#                         # Финальный шанс: ищем параметр по имени поля
#                         param = elem.LookupParameter(field.ColumnHeading)
#
#                 # Проверяем значение найденного параметра
#                 if param and param.HasValue:
#                     if param.StorageType == DB.StorageType.String:
#                         if param.AsString() and param.AsString().strip():
#                             has_value = True
#                             break
#                     else:
#                         has_value = True
#                         break
#
#             # Меняем видимость столбца
#             if has_value:
#                 if field.IsHidden:
#                     field.IsHidden = False
#             else:
#                 if not field.IsHidden:
#                     field.IsHidden = True
#
#     return True


