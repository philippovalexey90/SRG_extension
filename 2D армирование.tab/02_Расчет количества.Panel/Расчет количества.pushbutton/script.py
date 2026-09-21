# -*- coding: utf-8 -*-

__title__ = "Просуммировать количество арматуры"
__doc__ = """Version = 1.0
Date    = 24.08.2026
_____________________________________________________________________
Отработано:
Отработано на версии 2020
Разработана функция def FEC_AllReinf_in_doc_SHP_sep_to_dct(doc)

Фильтр для элементов армирования
Найти все элементы SHP  соотвествующей марки констр. и раздела
Разделить элементы по наличию записи марки сборки
Выполнить проверку элементов SHP Элемент одной марки с параметрами Учет в спецификации = True и Рассчитать количество = True должен быть в единственном эксземпляре,
Просуммировать элементы
_____________________________________________________________________
Необходимо отработать:
Добавить логи
Для функции def FEC_AllReinf_in_doc_SHP_sep_to_dct(doc) необходимо создать фильтр
ParameterHasValueFilter для общего параметра • Учет в спецификации
Необходимо проверить код на версии 2022
_____________________________________________________________________

_____________________________________________________________________
Автор: Филиппов Алексей"""

# Imports
import clr
from pyrevit import forms, script, revit, DB, UI
from Autodesk.Revit.DB import *
import wpf
from System import Windows

# CustomImports
from Snippets._selection import FEC_AllReinf_in_doc
from Snippets._work_with_reinf import SHP_sep_to_list, List_reinf_SHP_summ_dct, SUM_sep_to_list, \
    List_reinf_SUM_summ_dct, calculate_a_summ_GPT, check_SUM_without_SHP, print_dict_elements
from Snippets._transactions import write_total_cnt_to_revit

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# Variables

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

all_reinf = FEC_AllReinf_in_doc(doc)
SHP_simple_work, SHP_set_work, SHP_simple = List_reinf_SHP_summ_dct(SHP_sep_to_list(all_reinf))
SUM_simple_work, SUM_set_work, SUM_simple = List_reinf_SUM_summ_dct(SUM_sep_to_list(all_reinf))
# получил 5 словаря SHP_simple_work, SHP_set, SUM_simple_work, SUM_set, SUM_simple
#  выполнить проверку, что для каждого SHP_work есть хотя бы 1 SUM_simple

check_SUM_without_SHP(SHP_simple, SUM_simple)

updated_SHP = calculate_a_summ_GPT(SHP_simple_work, SUM_simple_work)
# print_dict_elements(SHP_set_work)
# print_dict_elements(SUM_set_work)
updated_SHP_set = calculate_a_summ_GPT(SHP_set_work, SUM_set_work)

write_total_cnt_to_revit(updated_SHP, doc)
write_total_cnt_to_revit(updated_SHP_set, doc)

'''
Функция получает на вход 2 словаря
SHP_simple
SUM_simple

Проходит по ключам SHP_simple
Для каждого ключа из 
SHP_simple
SUM_simple
достаем список
далее работем со списком
для каждого элемента из списка SHP_simple находи марку элемента mrk (марки элементов не повтоляются)
в списке из SUM_simple находим все элементы соотв марки mrk
Находим расчетное количество элементов mrk (отдельная функция)
число элементов записываем в SHP_simple_fill для каждой mrk

на выходе получаем словарь SHP_simple_fill с заполненным количеством



Далее нужно написать функцию с транзакцией, для внесения изменения в объекты Revit

'''






