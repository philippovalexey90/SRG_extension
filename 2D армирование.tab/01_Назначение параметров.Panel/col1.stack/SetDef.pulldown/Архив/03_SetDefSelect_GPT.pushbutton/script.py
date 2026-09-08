# -*- coding: utf-8 -*-

# Imports
import clr
from pyrevit import forms, script

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

    def save_button_clicked(sender, event):
        # Получите значения из текстовых полей
        sec_mrk = tb_sec_mrk.Text
        struct_mrk = tb_struct_mrk.Text
        struct_cnt = tb_struct_cnt.Text
        set_mrk = tb_set_mrk.Text
        set_cnt = tb_set_cnt.Text

        # Здесь вы можете добавить логику для сохранения данных
        # Например, сохранить в файл или выполнить другие действия

        with open("output.txt", "w") as f:
            f.write("Марка раздела: {}\n".format(sec_mrk))
            f.write("Марка конструкции: {}\n".format(struct_mrk))
            f.write("Количество конструкций: {}\n".format(struct_cnt))
            f.write("Марка сборки: {}\n".format(set_mrk))
            f.write("Количество сборок: {}\n".format(set_cnt))

        # Вывод сообщения о завершении
        forms.alert("Данные успешно сохранены!")


# Привязка обработчика к кнопке
# form.SaveButton.Click += save_button_clicked
MyCustomWindow().ShowDialog()
MyCustomWindow.save_button_clicked(sender,e)

