# -*- coding: utf-8 -*-

__title__ = "Удалить спецификацию из проекта"
__doc__ = """Version = 1.0
Date    = 19.09.2026
_____________________________________________________________________
Отработано:
Отработано на версии 2022
"""

# Imports
import clr
from pyrevit import forms, script, revit, DB, UI
from Autodesk.Revit.DB import *
import wpf
from System import Windows

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# CustomImports
from Snippets._transactions import delete_selected_schedule


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection_ids = uidoc.Selection.GetElementIds()

for element_id in selection_ids:
    delete_selected_schedule(doc, element_id)