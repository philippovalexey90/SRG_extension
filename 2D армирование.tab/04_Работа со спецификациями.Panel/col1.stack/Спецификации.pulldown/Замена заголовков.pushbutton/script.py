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




# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Transaction, TableSectionData, SectionType
from pyrevit import revit, forms

# Получаем текущий активный вид (это должна быть открытая спецификация)
view = revit.active_view

# Проверяем, что открыта именно спецификация
if hasattr(view, 'GetTableData'):
    # Получаем данные секции заголовка (Header) спецификации
    table_data = view.GetTableData()
    header_section = table_data.GetSectionData(SectionType.Header)

    # Определяем границы таблицы заголовков
    first_row = header_section.FirstRowNumber
    last_row = header_section.LastRowNumber
    first_col = header_section.FirstColumnNumber
    last_col = header_section.LastColumnNumber

    old_text = "ГОСТ 8509-93"
    new_text = "ГОСТ 12345-99"
    replaced = False

    # Открываем транзакцию для изменения модели
    t = Transaction(revit.doc, 'Переименование заголовка ВРС')
    t.Start()

    try:
        # Циклом обходим все ячейки в секции заголовка
        for row in range(first_row, last_row + 1):
            for col in range(first_col, last_col + 1):
                # Получаем текущий текст в ячейке
                cell_text = header_section.GetCellText(row, col)

                # Если нашли искомый ГОСТ, меняем его
                if old_text in cell_text:
                    header_section.SetCellText(row, col, new_text)
                    print("Успешно заменено в строке {}, столбце {}:".format(row, col))
                    print("Было: {} -> Стало: {}".format(cell_text, new_text))
                    replaced = True

        if not replaced:
            print("Текст '{}' в заголовках спецификации не найден.".format(old_text))
            t.RollBack()  # Отменяем транзакцию, если ничего не изменилось
        else:
            t.Commit()  # Применяем изменения

    except Exception as e:
        print("Ошибка при выполнении транзакции: {}".format(e))
        t.RollBack()
else:
    forms.alert("Пожалуйста, откройте нужную спецификацию на экране перед запуском скрипта!")
