# -*- coding: utf-8 -*-

# Imports
import clr
# clr.AddReference('System')

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Viewport, ViewType
from pyrevit import revit, forms


def is_user_on_sheet(silent=0):
    """
    Проверяет, открыт ли у пользователя в данный момент лист (Sheet).
    Если да — возвращает True.
    Если нет — выводит предупреждение (если silent == 0) и возвращает False.

    :param silent: Флаг тихого режима (0 - показывать окно, 1 - скрыть окно)
    """
    active_view = revit.doc.ActiveView

    if active_view.ViewType == ViewType.DrawingSheet:
        return True
    else:
        # Выводим окно только если флаг не равен 1
        if not silent:
            forms.alert(
                "Для работы скрипта необходимо перейти на лист!",
                title="Неверный тип вида",
                warn_icon=True
            )
        return False


def get_view_drawing_set(view):
    """
    Ищет параметр 'Орг.КомплектЧертежей' в свойствах переданного вида
    и возвращает его текстовое значение (или None, если параметр не найден/пуст).

    :param view: Объект вида Revit (View)
    :return: Строковое значение параметра или None
    """
    if not view:
        return None

    param = view.LookupParameter('Орг.КомплектЧертежей')

    if param and param.HasValue:
        val = param.AsString()
        if val and val.strip():
            return val.strip()

    return None