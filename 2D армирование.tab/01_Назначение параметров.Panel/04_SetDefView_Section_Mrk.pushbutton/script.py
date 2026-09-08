# -*- coding: utf-8 -*-
__title__   = "SetDefView_Section_Mrk"
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
from Snippets._selection import FEC_AllReinf_in_view

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

reinf = FEC_AllReinf_in_view(doc, active_view)



# Xamlfile

xamlfile = script.get_bundle_file('ui.xaml')

# Class

class MyCustomWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)


        self.SaveButton.Click += self.save_button_clicked


    def save_button_clicked(self, sender, event):
        try:
            sec_mrk = self.tb_sec_mrk.Text
            struct_mrk = self.tb_struct_mrk.Text




            SetSec_mrkToReinf(sec_mrk, reinf)
            SetStruct_mrkToReinf(struct_mrk, reinf)


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


