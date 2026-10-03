# -*- coding: utf-8 -*-

# Imports
import clr
# clr.AddReference('System')

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Viewport, ViewType
from pyrevit import revit, forms


def is_user_on_sheet():
    """
    Проверяет, открыт ли у пользователя в данный момент лист (Sheet).
    Если да — возвращает True. Если нет — выводит предупреждение и возвращает False.
    """
    # Получаем активный вид в текущем документе
    active_view = revit.doc.ActiveView

    # Проверяем, равен ли тип вида чертежному листу (DrawingSheet)
    if active_view.ViewType == ViewType.DrawingSheet:
        return True
    else:
        # Выводим красивое окно с предупреждением pyRevit
        forms.alert(
            "Для работы скрипта необходимо перейти на лист!",
            title="Неверный тип вида",
            warn_icon=True
        )
        return False

