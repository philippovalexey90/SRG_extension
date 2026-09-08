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
from Snippets._selection import find_views_by_detail_type_name


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Xamlfile

xamlfile = script.get_bundle_file('ui.xaml')


# Class

class MyCustomWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)


        self.SaveButton.Click += self.save_button_clicked


    def save_button_clicked(self, sender, event):
        try:
            type_name = self.tb_type_name.Text
            views_list = find_views_by_detail_type_name(doc, type_name)
            print("Тип '{}' найден на следующих видах:".format(type_name))
            for view_name in views_list:
                print("- {}".format(view_name))

            # Закрыть окно после обработки
            self.Close()

        except Exception as e:
            print("Ошибка в save_button_clicked:", e)






# Main

window = MyCustomWindow()
window.ShowDialog()