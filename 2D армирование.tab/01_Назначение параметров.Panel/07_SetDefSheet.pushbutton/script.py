# -*- coding: utf-8 -*-
__title__   = "Лист"
__doc__ = """Version = 1.0
Date    = 12.04.2025
_____________________________________________________________________
Отработано:
Отработано на версии 2020
Фильтр для элементов армирования
Наданный момент работает назначение 
Марки раздела
Марки конструкции
_____________________________________________________________________
Необходимо отработать:
Необходимо проверить код на версии 2022
_____________________________________________________________________
Задачи в планах:
- объеденить выбор рамкой и всех элементов на листе
- добавить предварительную проверку марки раздела листа
- добавить предварительный выбор марки раздела
- сделать отдельный скрипт назначения марки конструкции и марки раздела для всех видов армирования
- сделать отдельный скрипт парамтров для SHP
- сделать отдельный скрипт парамтров для SUM
_____________________________________________________________________
Автор: Филиппов Алексей"""


# Imports
import clr
from pyrevit import forms, script, revit, DB, UI
from Autodesk.Revit.DB import *
import wpf
from System import Windows


# CustomImports
from Snippets._set_param        import SetSec_mrkToReinf, SetStruct_mrkToReinf, SetStruct_cntToReinf, SetSet_mrkToReinf, SetSet_cntToReinf, SetSetChBox_cntToReinf
from Snippets._selection        import FEC_AllReinf_in_view, FEC_AllReinf_in_view_SHP, get_all_views_on_active_sheet, filter_specific_views
from Snippets._prep             import is_user_on_sheet
from Snippets._work_with_reinf  import print_nested_list

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# Variables

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = revit.get_selection()
reinf_id = selection.element_ids
active_view = doc.ActiveView

reinf = []
reinf_SHP = []

# Prepare

# Если функция проверки вернула False (пользователь не на листе) — сразу выходим
if not is_user_on_sheet():
    import sys; sys.exit() # Или просто return, если код внутри функции main()

# Если код пошел дальше — значит, пользователь точно на листе
views = filter_specific_views(get_all_views_on_active_sheet())

for view in views:
    reinf.extend(FEC_AllReinf_in_view(doc, view))
    reinf_SHP.extend(FEC_AllReinf_in_view_SHP(doc, view))

print_nested_list(reinf)


# Selection

# for i in reinf_id: reinf.append(doc.GetElement(i))
# all_detail_in_view = FilteredElementCollector(doc, active_view.Id)\
#     .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()
#
# for i in all_detail_in_view: reinf.append(i)

# reinf = FEC_AllReinf_in_view(doc, active_view)
# reinf_SHP = FEC_AllReinf_in_view_SHP(doc, active_view)


# Xamlfile

xamlfile = script.get_bundle_file('ui.xaml')

# Class

class MyCustomWindow(Windows.Window):
    def __init__(self):
        # Загружаем интерфейс из XAML
        wpf.LoadComponent(self, xamlfile)
        # --- УСТАНОВКА ЗНАЧЕНИЙ ПО УМОЛЧАНИЮ ---
        self.ChBox_1.IsChecked = True
        self.tb_struct_cnt.Text = "1"
        self.tb_set_cnt.Text = "1"
        # ----------------------------------------

        # Подписка на события
        self.SaveButton.Click += self.save_button_clicked
        self.ChBox_1.Checked += self.chBox_Checked
        self.ChBox_1.Unchecked += self.chBox_Unchecked

    def save_button_clicked(self, sender, event):
        try:
            sec_mrk = self.tb_sec_mrk.Text
            struct_mrk = self.tb_struct_mrk.Text
            struct_cnt = self.tb_struct_cnt.Text

            set_cnt = self.tb_set_cnt.Text
            set_chBox = self.ChBox_1.IsChecked

            # print("Марка раздела: {}\n".format(sec_mrk))
            # print("Марка конструкции: {}\n".format(struct_mrk))
            # print("Количество конструкций: {}\n".format(struct_cnt))
            # print("Марка сборки: {}\n".format(set_mrk))
            # print("Количество сборок: {}\n".format(set_cnt))
            # print("Чекбокс: {}\n".format(self.ChBox_1.IsChecked))

            SetSec_mrkToReinf(sec_mrk, reinf)
            SetStruct_mrkToReinf(struct_mrk, reinf)
            SetStruct_cntToReinf(struct_cnt, reinf_SHP)
            # SetSet_mrkToReinf(set_mrk, reinf)
            SetSet_cntToReinf(set_cnt, reinf_SHP)
            # SetSetChBox_cntToReinf(set_chBox, reinf)

            # Закрыть окно после обработки
            self.Close()

        except Exception as e:
            print("Ошибка в save_button_clicked:", e)

    def chBox_Checked(self, sender, args):
        self.ChBox.IsChecked = True
        # try:
        #     print("CheckBox установлен: ", self.ChBox.IsChecked)
        # except Exception as e:
        #     print("Ошибка в chBox_Checked:", e)

    def chBox_Unchecked(self, sender, args):
        self.ChBox.IsChecked = False
        # try:
        #     print("CheckBox сброшен: ", self.ChBox.IsChecked)
        # except Exception as e:
        #     print("Ошибка в chBox_Unchecked:", e)






# Main



window = MyCustomWindow()
window.ShowDialog()


