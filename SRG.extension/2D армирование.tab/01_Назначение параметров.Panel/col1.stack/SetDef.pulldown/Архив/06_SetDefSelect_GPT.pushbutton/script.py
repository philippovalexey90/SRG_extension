# -*- coding: utf-8 -*-

# Imports
import clr
from pyrevit import forms, script
import wpf
from System import Windows

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# find the path of ui.xaml
xamlfile = script.get_bundle_file('ui.xaml')


class MyCustomWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

        # Привязка обработчика к кнопке
        self.SaveButton.Click += self.save_button_clicked

        # Чек бокс
        self.ChBox.IsChecked = False  # Изначально значение False

        # Привязка обработчиков событий
        self.ChBox.Checked += self.chBox_Checked
        self.ChBox.Unchecked += self.chBox_Unchecked

    def save_button_clicked(self, sender, event):
        # Получите значения из текстовых полей
        sec_mrk = self.tb_sec_mrk.Text
        struct_mrk = self.tb_struct_mrk.Text
        struct_cnt = self.tb_struct_cnt.Text
        set_mrk = self.tb_set_mrk.Text
        set_cnt = self.tb_set_cnt.Text



        print("Марка раздела: {}\n".format(sec_mrk))
        print("Марка конструкции: {}\n".format(struct_mrk))
        print("Количество конструкций: {}\n".format(struct_cnt))
        print("Марка сборки: {}\n".format(set_mrk))
        print("Количество сборок: {}\n".format(set_cnt))
        print("Чекбокс: {}\n".format(self.ChBox.IsChecked))

        # Вывод сообщения о завершении

        # forms.alert("Данные успешно сохранены!")


    def chBox_Checked(self, sender, args):
        self.ChBox.IsChecked = True
        print("CheckBox установлен: ", self.ChBox.IsChecked)


    def chBox_Unchecked(self, sender, args):
        self.ChBox.IsChecked = False
        print("CheckBox сброшен: ", self.ChBox.IsChecked)

# Запуск окна
MyCustomWindow().ShowDialog()
print("CheckBox: ", self.ChBox.IsChecked)