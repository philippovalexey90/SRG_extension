# -*- coding: utf-8 -*-
__title__   = "3_Назначение параметров только элементам SHP на виде"
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
from Snippets._set_param import SetSec_mrkToReinf, SetStruct_mrkToReinf, SetStruct_cntToReinf, SetSet_mrkToReinf, SetSet_cntToReinf, SetSetChBox_cntToReinf
from Snippets._selection import FEC_AllReinf_in_view_SHP

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# Variables

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = revit.get_selection()
reinf_id = selection.element_ids
active_view = doc.ActiveView

# reinf=[]

# Selection

# for i in reinf_id: reinf.append(doc.GetElement(i))
# all_detail_in_view = FilteredElementCollector(doc, active_view.Id)\
#     .OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()
#
# for i in all_detail_in_view: reinf.append(i)

reinf = FEC_AllReinf_in_view_SHP(doc, active_view)



# Xamlfile

xamlfile = script.get_bundle_file('ui.xaml')

# Class

class MyCustomWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)
        self.ChBox.IsChecked = False

        self.SaveButton.Click += self.save_button_clicked
        self.ChBox.Checked += self.chBox_Checked
        self.ChBox.Unchecked += self.chBox_Unchecked

    def save_button_clicked(self, sender, event):
        try:
            sec_mrk = self.tb_sec_mrk.Text
            struct_mrk = self.tb_struct_mrk.Text
            struct_cnt = self.tb_struct_cnt.Text
            set_mrk = self.tb_set_mrk.Text
            set_cnt = self.tb_set_cnt.Text
            set_chBox = self.ChBox.IsChecked

            # print("Марка раздела: {}\n".format(sec_mrk))
            # print("Марка конструкции: {}\n".format(struct_mrk))
            # print("Количество конструкций: {}\n".format(struct_cnt))
            # print("Марка сборки: {}\n".format(set_mrk))
            # print("Количество сборок: {}\n".format(set_cnt))
            # print("Чекбокс: {}\n".format(self.ChBox.IsChecked))

            SetSec_mrkToReinf(sec_mrk, reinf)
            SetStruct_mrkToReinf(struct_mrk, reinf)
            SetStruct_cntToReinf(struct_cnt, reinf)
            SetSet_mrkToReinf(set_mrk, reinf)
            SetSet_cntToReinf(set_cnt, reinf)
            SetSetChBox_cntToReinf(set_chBox, reinf)

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


