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
    try:
        s = 1 if not s.isdigit() else s
        # get shared parameter
        reinf_shared=[]

        for i in reinf:
            reinf_shared.append(i.LookupParameter('• Количество конструкций')) # get shared parameter

        # Transaction module

        t = Transaction(doc, "changes")
        t.Start()                           #Start Transaction
        for i in reinf_shared:
            i.Set(int(s))


        t.Commit()                          #End Transaction
        pass
    except:
        pass

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
    try:
        s = 1 if not s.isdigit() else s
        # get shared parameter
        reinf_shared=[]

        for i in reinf:
            reinf_shared.append(i.LookupParameter('• Количество сборок')) # get shared parameter

        # Transaction module

        t = Transaction(doc, "changes")
        t.Start()                           #Start Transaction
        for i in reinf_shared:
            i.Set(int(s))


        t.Commit()                          #End Transaction
        pass
    except:
        pass

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