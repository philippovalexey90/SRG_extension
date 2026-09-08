# -*- coding: utf-8 -*-

# Imports
import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from pyrevit import forms
from pyrevit import UI
from pyrevit import script
import wpf
from System import Windows


# find the path of ui.xaml
xamlfile = script.get_bundle_file('ui.xaml')


class MyCustomWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)



MyCustomWindow().ShowDialog()

