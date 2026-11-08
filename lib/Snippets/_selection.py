# -*- coding: utf-8 -*-

# Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List as NetList



from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
from Autodesk.Revit.UI import *
from pyrevit import revit, DB, UI


# Variables

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# Functions

def get_selected_elements(uidoc):
    """ Function to get selected elements in Revit UI"""
    doc = uidoc.Document
    print(doc.Title)
    selected_elements = []

    for e_id in uidoc.Selection.GetElementsIds():
        element = doc.GetElement(e_id)
        selected_elements.append(element)
    return selected_elements

def get_selected_elements_short(uidoc):
    """ Function to get selected elements in Revit UI"""
    doc = uidoc.Document
    print(doc.Title)
    return [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementsIds()]

def get_selected_elements_simple(uidoc):
    """ Function to get selected elements in Revit UI
    Возвращает коллекцию (список) элементов, а не один объект"""
    selected_elements = revit.get_selection()
    return selected_elements

def FEC_AllDetail_in_view(doc, active_view):
    """ Function select detail components in Revit UI"""
    detail = []
    all_detail_in_view = FilteredElementCollector(doc, active_view.Id) \
        .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()
    for family_instance in all_detail_in_view: detail.append(family_instance)
    return detail

# def FEC_AllReinf_in_view_study(doc, active_view):
#     """ Function select Reinf components in Revit UI"""
#     reinf = []
#     reinffam_R_SHP ='R-SHP'
#     reinffam_R_SUM = 'R-SUM'
#
#     all_detail_in_view = FilteredElementCollector(doc, active_view.Id) \
#         .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()
#     for family_instance in all_detail_in_view:
#         if reinffam_R_SHP in family_instance.Symbol.Family.Name or reinffam_R_SUM in family_instance.Symbol.Family.Name:
#             reinf.append(family_instance)
#     return reinf

# def FEC_AllReinf_in_view_study1(doc, active_view):
#     """Function select Reinf components in Revit UI"""
#     reinffam_R_SHP = 'R-SHP'
#     reinffam_R_SUM = 'R-SUM'
#     reinffam_DRF = 'DRF'
#     reinffam_DRS = 'DRS'
#
#
#     all_detail_in_view = FilteredElementCollector(doc, active_view.Id) \
#         .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()
#
#     reinf = [family_instance for family_instance in all_detail_in_view
#               if hasattr(family_instance, 'Symbol') and
#                  (reinffam_R_SHP in family_instance.Symbol.Family.Name or
#                   reinffam_R_SUM in family_instance.Symbol.Family.Name or
#                   reinffam_DRF in family_instance.Symbol.Family.Name or
#                   reinffam_DRS in family_instance.Symbol.Family.Name)]
#
#
#     return reinf

def FEC_AllReinf_in_view(doc, active_view):
    """Function select Reinf components in Revit UI"""
    reinffam_R_SHP = 'R-SHP'
    reinffam_R_SUM = 'R-SUM'
    reinffam_DRF = 'DRF'
    reinffam_DRS = 'DRS'

    # Словарь с семействами, которые мы хотим проверить
    valid_families = {
        reinffam_R_SHP: True,
        reinffam_R_SUM: True,
        reinffam_DRF: True,
        reinffam_DRS: True
    }

    all_detail_in_view = FilteredElementCollector(doc, active_view.Id) \
        .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()

    reinf = [
        family_instance for family_instance in all_detail_in_view
        if hasattr(family_instance, 'Symbol') and
           any(part in family_instance.Symbol.Family.Name for part in valid_families)
    ]

    # Проверка: Проходим по всем экземплярам и выводим имя семейства
    # for family_instance in reinf:
    #     family = family_instance.Symbol.Family  # Получаем семейство
    #     family_name = family.Name  # Получаем имя семейства
    #     print("Экземпляр: {}, Имя семейства: {}".format(family_instance.Id, family_name))

    return reinf

def FEC_AllReinf_in_view_SHP(doc, active_view):
    """Function select Reinf components in Revit UI"""
    reinffam_R_SHP = 'R-SHP'
    reinffam_R_SUM = 'R-SUM'
    reinffam_DRF = 'DRF'
    reinffam_DRS = 'DRS'

    # Словарь с семействами, которые мы хотим проверить
    valid_families = {
        reinffam_R_SHP: True,
        reinffam_DRF: True,

    }

    all_detail_in_view = FilteredElementCollector(doc, active_view.Id) \
        .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()

    reinf = [
        family_instance for family_instance in all_detail_in_view
        if hasattr(family_instance, 'Symbol') and
           any(part in family_instance.Symbol.Family.Name for part in valid_families)
    ]

    # Проверка: Проходим по всем экземплярам и выводим имя семейства
    # for family_instance in reinf:
    #     family = family_instance.Symbol.Family  # Получаем семейство
    #     family_name = family.Name  # Получаем имя семейства
    #     print("Экземпляр: {}, Имя семейства: {}".format(family_instance.Id, family_name))

    return reinf

# Work with DOC

def FEC_AllReinf_in_doc(doc):
    """Function select Reinf components in Revit DOC"""

    reinffam_R_SHP = 'R-SHP'
    reinffam_R_SUM = 'R-SUM'
    reinffam_DRF = 'DRF'
    reinffam_DRS = 'DRS'

    # Словарь с семействами, которые мы хотим проверить
    valid_families = {
        reinffam_R_SHP: True,
        reinffam_R_SUM: True,
        reinffam_DRF: True,
        reinffam_DRS: True
    }

    all_detail_in_view = FilteredElementCollector(doc) \
        .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()

    reinf = [
        family_instance for family_instance in all_detail_in_view
        if hasattr(family_instance, 'Symbol') and
           any(part in family_instance.Symbol.Family.Name for part in valid_families)
    ]

    # Проверка: Проходим по всем экземплярам и выводим имя семейства
    # for family_instance in reinf:
    #     family = family_instance.Symbol.Family  # Получаем семейство
    #     family_name = family.Name  # Получаем имя семейства
    #     print("Экземпляр: {}, Имя семейства: {}".format(family_instance.Id, family_name))

    return reinf

def FEC_AllStructBuiltInCat_in_doc(doc):
    """Function select Structural Builtin components in Revit DOC"""

    # 1. Создаем список категорий в формате .NET (требование Revit API)
    categories = NetList[BuiltInCategory]()

    categories.Add(BuiltInCategory.OST_Walls)
    categories.Add(BuiltInCategory.OST_StructuralFoundation)
    categories.Add(BuiltInCategory.OST_Floors)
    categories.Add(BuiltInCategory.OST_StructuralFraming)
    categories.Add(BuiltInCategory.OST_StructuralColumns)

    # 2. Создаем мульти-категорийный фильтр
    multi_filter = ElementMulticategoryFilter(categories)

    # 3. Собираем ВСЕ элементы этих категорий за ОДИН запрос
    all_elements = FilteredElementCollector(doc) \
        .WherePasses(multi_filter) \
        .WhereElementIsNotElementType() \
        .ToElements()

    # 4. Быстро распределяем элементы по спискам с помощью генераторов Python
    walls = [e for e in all_elements if e.Category.Id.IntegerValue == int(BuiltInCategory.OST_Walls)]
    foundations = [e for e in all_elements if
                   e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFoundation)]
    floors = [e for e in all_elements if e.Category.Id.IntegerValue == int(BuiltInCategory.OST_Floors)]
    framing = [e for e in all_elements if e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFraming)]
    columns = [e for e in all_elements if e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralColumns)]

    return walls, foundations, floors, framing, columns

def print_structural_elements_report(walls, foundations, floors, framing, columns):
        """
        Принимает списки конструктивных элементов Revit, группирует их
        и выводит структурированный отчет с ID и именами в консоль.
        """
        # Создаем структурированный словарь для красивой итерации
        structural_data = {
            "1. Стены (OST_Walls)": walls,
            "2. Фундаменты (OST_StructuralFoundation)": foundations,
            "3. Перекрытия (OST_Floors)": floors,
            "4. Несущий каркас (OST_StructuralFraming)": framing,
            "5. Несущие колонны (OST_StructuralColumns)": columns
        }

        # Наша шапка отчета
        print("=" * 60)
        print("ОТЧЕТ О СБОРЕ КОНСТРУКТИВНЫХ ЭЛЕМЕНТОВ В ПРОЕКТЕ")
        print("=" * 60)

        # Перебираем категории и печатаем элементы внутри них
        for category_name, elements_list in structural_data.items():
            print("\n{} (Всего элементов: {})".format(category_name, len(elements_list)))
            print("-" * 50)

            if not elements_list:
                print("  [Элементы данной категории в проекте отсутствуют]")
                continue

            for idx, elem in enumerate(elements_list, 1):
                # Безопасное чтение параметров элемента, чтобы скрипт никогда не падал
                try:
                    elem_name = elem.Name if hasattr(elem, 'Name') else "Без имени"
                    print("  {}. ID: {}, Имя: {}".format(idx, elem.Id, elem_name))
                except Exception as e:
                    print("  {}. ID: {}, [Ошибка чтения имени: {}]".format(idx, elem.Id, str(e)))

        print("\n" + "=" * 60)
        print("ПЕЧАТЬ ПОЛНОСТЬЮ ЗАВЕРШЕНА")
        print("=" * 60)


def universalLookupParameter(elem, parameter_name):
    """
    Ищет параметр у элемента Revit вне зависимости от того,
    задан ли он по типу (Type) или по экземпляру (Instance).

    :param elem: Объект элемента Revit (Element)
    :param parameter_name: Строковое имя параметра (например, "• Диаметр")
    :return: Объект параметра (Parameter) или None, если параметр не найден
    """
    if not elem:
        return None

    # Шаг 1: Пробуем найти параметр в свойствах ЭКЗЕМПЛЯРА
    param = elem.LookupParameter(parameter_name)
    if param:
        return param

    # Шаг 2: Если в экземпляре нет, пробуем найти в свойствах ТИПА
    # Используем глобальную переменную doc, которую вы объявили в блоке Variables
    type_id = elem.GetTypeId()

    # Проверяем, что у элемента есть ID типа (сравниваем напрямую с классом ElementId)
    if type_id and type_id != ElementId.InvalidElementId:
        elem_type = doc.GetElement(type_id)
        if elem_type:
            param = elem_type.LookupParameter(parameter_name)
            if param:
                return param

    # Если параметр не найден ни в типе, ни в экземпляре
    return None



def get_parameter_value(reinf, param_name):
    """
    Ищет параметр по названию сначала в экземпляре, а затем в типе элемента Revit.
    Возвращает значение или сообщение об отсутствии параметра.
    """
    # 1. ЧТЕНИЕ ПАРАМЕТРА ЭКЗЕМПЛЯРА
    try:
        reinf_shared = reinf.LookupParameter(param_name)
        if reinf_shared is not None:
            # Метод AsInteger() используется, так как в исходном коде был .AsInteger()
            print('{}: {}'.format(param_name, reinf_shared.AsInteger()))
            return reinf_shared.AsInteger()
        else:
            print('{}: Параметр отсутствует в экземпляре'.format(param_name))
    except Exception as e:
        print('Ошибка при чтении параметра экземпляра: {}'.format(e))

    # 2. ЧТЕНИЕ ПАРАМЕТРА ТИПА (FamilySymbol)
    try:
        type_id = reinf.GetTypeId()
        reinf_type = reinf.Document.GetElement(type_id)

        if reinf_type is not None:
            reinf_type_shared = reinf_type.LookupParameter(param_name)
            if reinf_type_shared is not None:
                print('{} (по типу): {}'.format(param_name, reinf_type_shared.AsInteger()))
                return reinf_type_shared.AsInteger()
            else:
                print('{} (по типу): Параметр отсутствует в типе'.format(param_name))
        else:
            print('{} (по типу): Не удалось получить объект типа'.format(param_name))
    except Exception as e:
        print('Ошибка при чтении параметра типа: {}'.format(e))

    return None

def find_views_by_detail_type_name(doc, type_name):
    """
    Находит все виды, на которых размещены экземпляры элементов узла
    заданного наименования типа.
    """
    # 1. Находим нужный тип семейства (FamilySymbol) по имени в категории "Элементы узлов"
    detail_type = None
    all_types = FilteredElementCollector(doc) \
        .OfCategory(BuiltInCategory.OST_DetailComponents) \
        .WhereElementIsElementType()

    for t in all_types:
        if t.Name == type_name:
            detail_type = t
            break

    if not detail_type:
        print("Тип с именем '{}' не найден в модели.".format(type_name))
        return []

    # 2. Собираем все экземпляры этого конкретного типа
    instances = FilteredElementCollector(doc) \
        .OfCategory(BuiltInCategory.OST_DetailComponents) \
        .WhereElementIsNotElementType()

    # Фильтруем элементы узла, проверяя соответствие ID их типа
    target_instances = [i for i in instances if i.GetTypeId() == detail_type.Id]

    if not target_instances:
        print("Экземпляры типа '{}' не найдены в модели.".format(type_name))
        return []

    # 3. Собираем уникальные ID видов, на которых лежат эти экземпляры
    view_ids = set()
    for inst in target_instances:
        # У 2D элементовOwnerViewId всегда указывает на родительский вид
        if inst.OwnerViewId and inst.OwnerViewId != ElementId.InvalidElementId:
            view_ids.add(inst.OwnerViewId)

    # 4. Получаем имена видов по их ID
    found_views = []
    for v_id in view_ids:
        view_el = doc.GetElement(v_id)
        if view_el:
            found_views.append(view_el.Name)

    return found_views

def find_views_by_family_name(doc, family_name):
    """
    Находит все виды, на которых размещены любые экземпляры
    заданного семейства элементов узла.
    """
    # 1. Находим семейство в категории "Элементы узлов" по имени
    target_family = None
    all_families = FilteredElementCollector(doc) \
        .OfClass(Family)

    for f in all_families:
        # Проверяем имя семейства и его категорию
        if f.Name == family_name and f.FamilyCategory.Id.IntegerValue == int(BuiltInCategory.OST_DetailComponents):
            target_family = f
            break

    if not target_family:
        print("Семейство с именем '{}' не найдено в модели.".format(family_name))
        return []

    # 2. Получаем ID всех типов (типоразмеров), принадлежащих этому семейству
    family_type_ids = target_family.GetFamilySymbolIds()

    if not family_type_ids:
        print("У семейства '{}' нет созданных типов.".format(family_name))
        return []

    # 3. Собираем все экземпляры элементов узлов в модели
    instances = FilteredElementCollector(doc) \
        .OfCategory(BuiltInCategory.OST_DetailComponents) \
        .WhereElementIsNotElementType()

    # Фильтруем экземпляры: оставляем только те, чей TypeId входит в наше семейство
    target_instances = [i for i in instances if i.GetTypeId() in family_type_ids]

    if not target_instances:
        print("Экземпляры семейства '{}' не найдены в модели.".format(family_name))
        return []

    # 4. Собираем уникальные ID видов, на которых размещены элементы
    view_ids = set()
    for inst in target_instances:
        if inst.OwnerViewId and inst.OwnerViewId != ElementId.InvalidElementId:
            view_ids.add(inst.OwnerViewId)

    # 5. Получаем имена видов по их ID
    found_views = []
    for v_id in view_ids:
        view_el = doc.GetElement(v_id)
        if view_el:
            found_views.append(view_el.Name)

    return found_views

# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---
# doc — это текущий документ Revit (в pyRevit/Shell он доступен по умолчанию)
# target_type_name = "Лист 20х220"  # Замените на нужное имя
# views_list = find_views_by_detail_type_name(doc, target_type_name)
#
# print("Тип '{}' найден на следующих видах:".format(target_type_name))
# for view_name in views_list:
#     print("- {}".format(view_name))

# Work with Views

def get_all_views_on_active_sheet():
    """
    Находит и возвращает список всех видов (View), размещенных на активном листе.
    """
    doc = revit.doc
    active_sheet = doc.ActiveView

    # 1. Проверяем, что мы действительно на листе
    if active_sheet.ViewType != ViewType.DrawingSheet:
        forms.alert("Активный вид не является листом!", title="Ошибка")
        return []

    # Идентификатор текущего листа
    current_sheet_id = active_sheet.Id
    views = []

    # 2. Собираем все видовые экраны в проекте
    viewports = FilteredElementCollector(doc) \
        .OfClass(Viewport) \
        .ToElements()

    # 3. Фильтруем видовые экраны: ищем те, которые лежат на нашем листе
    for vp in viewports:
        # Проверяем, совпадает ли ID листа видового экрана с нашим активным листом
        if vp.SheetId == current_sheet_id:
            # Извлекаем ID самого вида, привязанного к этому экрану
            view_id = vp.ViewId
            view_element = doc.GetElement(view_id)

            if view_element:
                views.append(view_element)

    return views


def filter_specific_views(all_views):
    """
    Фильтрует список видов и оставляет только:
    Планы несущих конструкций, Фасады, Разрезы, Чертежные виды и Узлы/Фрагменты.
    """
    # Создаем множество (set) из целевых типов видов для быстрой проверки
    target_types = {
        ViewType.EngineeringPlan,
        ViewType.Elevation,
        ViewType.Section,
        ViewType.DraftingView,
        ViewType.Detail
    }

    # Фильтруем виды с помощью генератора списков (List Comprehension)
    filtered_views = [v for v in all_views if v.ViewType in target_types]

    return filtered_views


def get_selected_schedule(selected_elements, active_view):
    """
    Функция проверяет выборку и возвращает имя спецификации.
    Если спецификация не выбрана на экране, проверяет активный вид.
    """
    # 1. Проверяем элементы, полученные из вашей функции
    if selected_elements:
        first_element = selected_elements[0]  # Берем первый элемент из списка
        return first_element

    # 2. Если на экране ничего не выбрано, проверяем текущий активный вид
    if isinstance(active_view, DB.ViewSchedule):
        return active_view

    # Если спецификация не найдена
    return None


def check_schedule_combination(schedule_name):
    """
    Проверяет, начинается ли имя спецификации с 6-го по счету символа
    на комбинацию 'E1' или 'E2' (с учетом английской/русской раскладки).
    """
    # Нам нужно как минимум 7 символов в имени, чтобы проверить 6-й и 7-й
    if not schedule_name or len(schedule_name) < 7:
        return False

    # Берем срез строки: 6-й и 7-й символы (индексы 5 и 6, индекс 7 не включается)
    combination = schedule_name[5:7]

    # Приводим к верхнему регистру для универсальности (e1 -> E1)
    combination_upper = combination.upper()

    # Список допустимых вариантов (английская E и русская Е)
    valid_combinations = [
        "E1", "E2",  # Английская E
        u"Е1", u"Е2"  # Русская Е (юникод для IronPython 2.7)
    ]

    # Проверяем, входит ли наша комбинация в список разрешенных
    if combination_upper in valid_combinations:
        return True

    return False


# Class

