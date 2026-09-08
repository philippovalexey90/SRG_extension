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


# Functions

def SHP_sep_to_list (family_instance):

    reinffam_R_SHP = 'R-SHP'
    reinffam_R_SUM = 'R-SUM'
    reinffam_DRF = 'DRF'
    reinffam_DRS = 'DRS'

    # Словарь с семействами, которые мы хотим проверить
    valid_families = {
        reinffam_R_SHP: True,
        reinffam_DRF: True
    }

    reinf = [
        reinf_instance for reinf_instance in family_instance
        if hasattr(reinf_instance, 'Symbol') and
           any(part in reinf_instance.Symbol.Family.Name for part in valid_families)
    ]
    # for reinf_instance in reinf:
    #     print("reinf: {}".format(reinf_instance))

    reinf_SHP_summ = []
    for reinf_instance in reinf:
        try:

            instance = get_reinf_SHP_to_summ(reinf_instance)
            if instance is None:
                continue
            else: reinf_SHP_summ.append(instance)
        except:
            continue

    # Проверка: Проходим по всем экземплярам и выводим имя семейства
    # for family_instance in reinf_SHP_summ:
    #     # print("reinf_SHP_to_summ: {}".format(family_instance))
    #     family = family_instance.Symbol.Family  # Получаем семейство
    #     family_name = family.Name  # Получаем имя семейства
    #     spek = family_instance.LookupParameter('• Учет в спецификации')
    #     cnt = family_instance.LookupParameter('• Рассчитать количество')
    #
    #     try:
    #         print("Экземпляр: {}, Имя семейства: {}, • Учет в спецификации: {}, • Рассчитать количество: {}".format(
    #             family_instance.Id, family_name, get_param_value(spek), get_param_value(cnt)))
    #
    #     except:
    #         pass
    return reinf_SHP_summ

def SUM_sep_to_list (family_instance):

    reinffam_R_SHP = 'R-SHP'
    reinffam_R_SUM = 'R-SUM'
    reinffam_DRF = 'DRF'
    reinffam_DRS = 'DRS'

    # Словарь с семействами, которые мы хотим проверить
    valid_families = {
        reinffam_R_SUM: True,
        reinffam_DRS: True
    }

    reinf = [
        reinf_instance for reinf_instance in family_instance
        if hasattr(reinf_instance, 'Symbol') and
           any(part in reinf_instance.Symbol.Family.Name for part in valid_families)
    ]
    # for reinf_instance in reinf:
    #     print("reinf: {}".format(reinf_instance))

    reinf_SUM_summ = []
    for reinf_instance in reinf:
        try:

            instance = get_reinf_SUM_to_summ(reinf_instance)
            if instance is None:
                continue
            else: reinf_SUM_summ.append(instance)
        except:
            continue

        # Проверка: Проходим по всем экземплярам и выводим имя семейства
    # for family_instance in reinf_SUM_summ:
    #     # print("reinf_SUM_summ: {}".format(family_instance))
    #     family = family_instance.Symbol.Family  # Получаем семейство
    #     family_name = family.Name  # Получаем имя семейства
    #     spek = family_instance.LookupParameter('• Учет в спецификации')
    #     cnt = family_instance.LookupParameter('• Рассчитать количество')
    #
    #     try:
    #         print("Экземпляр: {}, Имя семейства: {}, • Учет в спецификации: {}, • Рассчитать количество: {}".format(
    #             family_instance.Id, family_name, get_param_value(spek), get_param_value(cnt)))
    #
    #     except:
    #         pass
    return reinf_SUM_summ

def List_reinf_SHP_summ_dct(reinf_SHP_summ):
    SHP_simple = {}
    SHP_simple_work = {}
    SHP_set_work = {}

    for family_instance in reinf_SHP_summ:
        # print(get_param_value(family_instance.LookupParameter('• Марка сборки')))
        if get_param_value(family_instance.LookupParameter('• Марка сборки')) =='':
            key_abc = get_family_instance_key_abc(family_instance)
            key_ab = get_family_instance_key_ab(family_instance)
            add_to_dict(SHP_simple_work, key_ab, family_instance)
            # SHP_simple_work[key_ab] = family_instance

            if key_abc in SHP_simple:
                print('Ошибка! Элементов армирования SHP c параметрами • Раздел, • Марка конструкции, • Марка элемента повторяются')
                for i in key_abc:
                    print(i)

                print("Name: {}".format(family_instance.Name))
                print("Name: {}".format(SHP_simple[key_abc].Name))
                print("Id: {}".format(family_instance.Id))
                print("Id: {}".format(SHP_simple[key_abc].Id))

                print('\n_______________\n')
                # for p in SHP_simple[key].Parameters:
                #     print("Name: {}".format(p.Definition.Name))
                #     print("Id: {}".format(p.Definition.Id))

            else:
                SHP_simple[key_abc] = family_instance


        else:
            key_abd = get_family_instance_key_abd(family_instance)
            add_to_dict(SHP_set_work, key_abd, family_instance)
            # print(key)
            # SHP_set[key_abd] = family_instance

    # print('SHP_simple_work')
    # print_dict_elements(SHP_simple_work)
    # print('SHP_simple')
    # print_dict_elements(SHP_simple)
    # print('SHP_set_work')
    # print_dict_elements(SHP_set_work)

    return SHP_simple_work, SHP_set_work

def List_reinf_SUM_summ_dct(reinf_SUM_summ):

    SUM_simple_work = {}
    SUM_set_work = {}

    for family_instance in reinf_SUM_summ:
        # print(get_param_value(family_instance.LookupParameter('• Марка сборки')))
        if get_param_value(family_instance.LookupParameter('• Марка сборки')) =='':

            key_ab = get_family_instance_key_ab(family_instance)
            add_to_dict(SUM_simple_work, key_ab, family_instance)


        else:
            key_abd = get_family_instance_key_abd(family_instance)
            add_to_dict(SUM_set_work, key_abd, family_instance)
            # print(key)
            # SHP_set[key_abd] = family_instance

    # print('SUM_simple_work')
    # print_dict_elements(SUM_simple_work)
    # print('SUM_set_work')
    # print_dict_elements(SUM_set_work)

    return SUM_simple_work, SUM_set_work

# def calculate_a_summ(SHP_simple, SUM_simple):
#     for idx, (key, value) in enumerate(SHP_simple.items(), 1):
#         print('{}, Ключ: {}'.format(idx, tuple_to_string(key)))
#         # Если значение список или кортеж
#         if isinstance(value, (list, tuple)):
#             print('Количество элементов: {}'.format(len(value)))
#             for i, elem in enumerate(value, 1):
#                 if hasattr(elem, 'Id') and hasattr(elem, 'Name'):
#                     print('{}, Id: {}, Имя: {}'.format(i, elem.Id, elem.Name))
#                 else:
#                     print('{}, {}'.format(i, elem))
#     # for key in SHP_simple:
#     for key, SHP_list in SHP_simple.items():
#         # print('SHP_simple key: {}'.format(tuple_to_string(key)))
#         # SHP_list = SHP_simple[key]
#         SUM_list = SUM_simple.get(key)
#         if not SUM_list:
#             continue
#         for i in SHP_list:
#             cnt = 0
#             # print('='*60)
#             i_mrk = get_element_param_value(i, '• Марка элемента')
#             # print('{}-{}'.format(i.Id, i_mrk))
#             for j in SUM_list:
#                 j_mrk = get_element_param_value(j, '• Марка элемента')
#                 if i_mrk == j_mrk:
#                     cnt += get_element_param_value(j, '• Расчетное число')
#                     # print('----- {}-{}, • Расчетное число {}'.format(j.Id, j_mrk, cnt))
#                     add_to_dict(SHP_simple, key, cnt)
#                     print('• Марка элемента {}, Количество {}'. format(i_mrk, cnt))
#
#
#
#
#
#         # try:
#         #     SUM_list = SUM_simple[key]
#         #     # print('SUM_list: {}'.format(SUM_simple[key]))
#         #
#         #     for i in SHP_list:
#         #         cnt = 0
#         #         # print('='*60)
#         #         i_mrk = get_element_param_value(i, '• Марка элемента')
#         #         # print('{}-{}'.format(i.Id, i_mrk))
#         #         for j in SUM_list:
#         #             j_mrk = get_element_param_value(j, '• Марка элемента')
#         #             if i_mrk == j_mrk:
#         #                 cnt += get_element_param_value(j, '• Расчетное число')
#         #                 # print('----- {}-{}, • Расчетное число {}'.format(j.Id, j_mrk, cnt))
#         #                 add_to_dict(SHP_simple, key, cnt)
#         #                 print(SHP_simple[key])
#         #
#         # except:
#         #     continue
#
#     return SHP_simple

def calculate_a_summ_GPT(SHP_simple, SUM_simple):
    updated_SHP = {}

    for key, SHP_list in SHP_simple.items():
        # Безопасно получаем список из SUM_simple. Если ключа нет — используем пустой список
        SUM_list = SUM_simple.get(key, [])
        # print('Ключ: {}'.format(tuple_to_string(key)))
        new_list_for_key = []

        for i in SHP_list:
            # Считаем сумму "Расчетного числа" индивидуально для текущего элемента `i`
            element_total_cnt = 0
            i_mrk = get_element_param_value(i, '• Марка элемента')

            for j in SUM_list:
                j_mrk = get_element_param_value(j, '• Марка элемента')
                if i_mrk == j_mrk:
                    element_total_cnt += get_element_param_value(j, '• Расчетное число')
            # Вместо добавления в конец исходного списка,
            # упаковываем элемент и его сумму во вложенный список [элемент, сумма]
            new_list_for_key.append([i, element_total_cnt])

        # Записываем обновленный вложенный список в новый словарь
        updated_SHP[key] = new_list_for_key

    # print('----------Проверка print_dict_elements----------')
    # print_dict_with_nested_elements(updated_SHP)
    return updated_SHP





# Вспомогательные функции

def get_reinf_SHP_to_summ(family_instance):

    spek_val = get_param_value(family_instance.LookupParameter('• Учет в спецификации'))
    cnt_val = get_param_value(family_instance.LookupParameter('• Рассчитать количество'))
    if spek_val == 1 and cnt_val == 1:
        return family_instance

def get_reinf_SUM_to_summ(family_instance):

    cnt_val = get_param_value(family_instance.LookupParameter('• Рассчитать количество'))
    if cnt_val == 1:
        return family_instance

def get_param_value(param):
    """Get a value from a Parameter based on its StorageType."""
    value = None
    if param.StorageType == StorageType.Double:
        value = param.AsDouble()
    elif param.StorageType == StorageType.ElementId:
        value = param.AsElementId()
    elif param.StorageType == StorageType.Integer:
        value = param.AsInteger()
    elif param.StorageType == StorageType.String:
        value = param.AsString()
    return value

# Работа со словарем

def print_dict_elements(dict):

    '''Выводит на печать все элементы словаря'''
    if not dict:
        print('Словарь пуст')
        return
    print('='*60)
    print('Всего ключей: {}'.format(len(dict)))
    print('='*60)

    for idx, (key, value) in enumerate(dict.items(),1):
        print('\n{}, Ключ: {}\n'.format(idx, tuple_to_string(key)))

        # Если значение список или кортеж
        if isinstance(value, (list, tuple)):
            print('Количество элементов: {}'.format(len(value)))

            for i, elem in enumerate(value, 1):

                if hasattr(elem, 'Id') and hasattr(elem, 'Name'):
                     print('{}, Id: {}, Имя: {}'.format(i, elem.Id, elem.Name))
                else:
                     print('{}, {}'.format(i, elem))
        else:
            if hasattr(value, 'Id') and hasattr(value, 'Name'):
                print('Id: {}, Имя: {}'.format(value.Id, value.Name))
            else:
                print('Значение {}'.format(value))

    print('='*60)

def print_dict_with_nested_elements(target_dict):
    """Выводит на печать элементы измененного словаря со вложенными списками"""
    if not target_dict:
        print('Словарь пуст')
        return
    print('=' * 60)
    print('Всего ключей: {}'.format(len(target_dict)))
    print('=' * 60)

    for idx, (key, value) in enumerate(target_dict.items(), 1):
        print('\n{}, Ключ: {}\n'.format(idx, tuple_to_string(key)))

        if isinstance(value, (list, tuple)):
            print('Количество элементов: {}'.format(len(value)))
            for i, inner_item in enumerate(value, 1):
                # Так как теперь у нас внутри списки вида [elem, cnt]
                if isinstance(inner_item, (list, tuple)) and len(inner_item) == 2:
                    elem, cnt = inner_item
                    if hasattr(elem, 'Id') and hasattr(elem, 'Name'):
                        print('{}, Id: {}, Имя: {}, Расчетное число: {}'.format(i, elem.Id, elem.Name, cnt))
                    else:
                        print('{}, {}, Расчетное число: {}'.format(i, elem, cnt))
                else:
                    # На случай, если какой-то элемент остался старого формата
                    print('{}, Старый формат: {}'.format(i, inner_item))
        else:
            print('Значение не является списком: {}'.format(value))

    print('=' * 60)

def tuple_to_string(tuple):
    '''Преобразует кортеж в строку, разделяя значения пробелом'''
    return ' '.join(str(item) for item in tuple)

def add_to_dict(dict, key, new_item):
    '''
    Добавляет элемент в словарь по ключу.
    Если улюч существует - добавляет в список.
    Если нет ключа - создает новый список.
    '''
    if key not in dict:
        dict[key] = [] #Создаем новый список
    dict[key].append(new_item)

# Ключи словаря

def get_family_instance_key_abc(family_instance):

    val_a = get_element_param_value(family_instance, '• Раздел')
    val_b = get_element_param_value(family_instance, '• Марка конструкции')
    val_c = get_element_param_value(family_instance, '• Марка элемента')
    val_d = get_element_param_value(family_instance, '• Марка сборки')

    return (val_a, val_b, val_c)

def get_family_instance_key_ab(family_instance):

    val_a = get_element_param_value(family_instance, '• Раздел')
    val_b = get_element_param_value(family_instance, '• Марка конструкции')
    val_c = get_element_param_value(family_instance, '• Марка элемента')
    val_d = get_element_param_value(family_instance, '• Марка сборки')

    return (val_a, val_b)

def get_family_instance_key_abd(family_instance):

    val_a = get_element_param_value(family_instance, '• Раздел')
    val_b = get_element_param_value(family_instance, '• Марка конструкции')
    val_c = get_element_param_value(family_instance, '• Марка элемента')
    val_d = get_element_param_value(family_instance, '• Марка сборки')

    return (val_a, val_b, val_d)

def get_element_param_value(element, param):
    val = get_param_value(element.LookupParameter(param))
    return val

