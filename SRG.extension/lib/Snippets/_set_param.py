# -*- coding: utf-8 -*-

# Imports

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
from Autodesk.Revit.UI import *
from pyrevit import revit, DB, UI

# Variables

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# Functions

def SetSec_mrkToReinf (s, reinf):
    try:
        # get shared parameter
        reinf_shared=[]

        for i in reinf:
            reinf_shared.append(i.LookupParameter('• Раздел')) # get shared parameter



        # Transaction module



        t = Transaction(doc, "changes")
        t.Start()                           #Start Transaction
        for i in reinf_shared:
            i.Set(s)

        # reinf_shared.Set(s)               #Set Parameter Value
        t.Commit()                          #End Transaction
        pass
    except:
        pass

def SetStruct_mrkToReinf (s, reinf):
    try:
        # get shared parameter
        reinf_shared=[]

        for i in reinf:
            reinf_shared.append(i.LookupParameter('• Марка конструкции')) # get shared parameter

        # Transaction module
        t = Transaction(doc, "changes")
        t.Start()                           #Start Transaction
        for i in reinf_shared:
            i.Set(s)


        t.Commit()                          #End Transaction
        pass
    except:
        pass

def SetStruct_cntToReinf (s, reinf):
    """
    Записывает целое значение s в параметр '• Количество конструкций'
    для всех элементов списка reinf.
    """
    # приведём входное значение к int
    try:
        s = int(s)
    except (ValueError, TypeError):
        from Autodesk.Revit.UI import TaskDialog
        TaskDialog.Show('Ошибка', 'Введите целое число.')
        return
    # соберём параметры, которые действительно существуют

    params = []
    for elem in reinf:
        p = elem.LookupParameter('• Количество конструкций')
        if p and p.StorageType == StorageType.Integer:
            params.append(p)

    if not params:
        return

    # один транзакционный блок
    try:
        with Transaction(doc, 'Количество конструкций') as t:
            t.Start()
            for p in params:
                p.Set(s)
            t.Commit()
    except Exception as ex:
        TaskDialog.Show('Ошибка транзакции', str(ex))




def SetSet_mrkToReinf (s, reinf):
    try:
        # get shared parameter
        reinf_shared=[]

        for i in reinf:
            reinf_shared.append(i.LookupParameter('• Марка сборки')) # get shared parameter

        # Transaction module

        t = Transaction(doc, "changes")
        t.Start()                           #Start Transaction
        for i in reinf_shared:
            i.Set(s)


        t.Commit()                          #End Transaction
        pass
    except:
        pass






def SetSet_cntToReinf (s, reinf):
    """
        Записывает целое значение s в параметр '• Количество сборок'
        для всех элементов списка reinf.
        """
    # приведём входное значение к int
    try:
        s = int(s)
    except (ValueError, TypeError):
        from Autodesk.Revit.UI import TaskDialog
        TaskDialog.Show('Ошибка', 'Введите целое число.')
        return
    # соберём параметры, которые действительно существуют

    params = []
    for elem in reinf:
        p = elem.LookupParameter('• Количество сборок')
        if p and p.StorageType == StorageType.Integer:
            params.append(p)

    if not params:
        return

    # один транзакционный блок
    try:
        with Transaction(doc, 'Количество сборок') as t:
            t.Start()
            for p in params:
                p.Set(s)
            t.Commit()
    except Exception as ex:
        TaskDialog.Show('Ошибка транзакции', str(ex))










def SetSetChBox_cntToReinf(s, reinf):
    try:
        # get shared parameter
        reinf_shared = []

        for i in reinf:
            reinf_shared.append(i.LookupParameter('• Специфицировать сборку'))  # get shared parameter

        # Transaction module

        t = Transaction(doc, "changes")
        t.Start()  # Start Transaction
        for i in reinf_shared:
            i.Set(s)


        t.Commit()  # End Transaction
        pass
    except:
        pass