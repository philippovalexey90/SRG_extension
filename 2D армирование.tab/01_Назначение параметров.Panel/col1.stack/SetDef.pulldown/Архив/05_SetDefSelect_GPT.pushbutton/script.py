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
        self.ChBox = False  # Изначально значение False
        # Привязка обработчиков событий
        self.ChBox.Checked += self.ChBox_Checked
        self.ChBox.Unchecked += self.ChBox_Unchecked

    def save_button_clicked(self, sender, event):
        # Получите значения из текстовых полей
        sec_mrk = self.tb_sec_mrk.Text
        struct_mrk = self.tb_struct_mrk.Text
        struct_cnt = self.tb_struct_cnt.Text
        set_mrk = self.tb_set_mrk.Text
        set_cnt = self.tb_set_cnt.Text

        def ChBox_Checked(self, sender, args):
            self.ChBox = True
            print("CheckBox установлен: ", self.ChBox)

        def ChBox_Unchecked(self, sender, args):
            self.ChBox = False
            print("CheckBox сброшен: ", self.ChBox)

        # Здесь вы можете добавить логику для сохранения данных
        try:
            with open('output.txt', 'w', encoding='utf-8') as f:
                f.write("Марка раздела: {}\n".format(sec_mrk))
                f.write("Марка конструкции: {}\n".format(struct_mrk))
                f.write("Количество конструкций: {}\n".format(struct_cnt))
                f.write("Марка сборки: {}\n".format(set_mrk))
                f.write("Количество сборок: {}\n".format(set_cnt))
                print('Данные успешно сохранены!')
        except:
            print('Ошибка записи')

        print("Марка раздела: {}\n".format(sec_mrk))
        print("Марка конструкции: {}\n".format(struct_mrk))
        print("Количество конструкций: {}\n".format(struct_cnt))
        print("Марка сборки: {}\n".format(set_mrk))
        print("Количество сборок: {}\n".format(set_cnt))

        # Вывод сообщения о завершении

        # forms.alert("Данные успешно сохранены!")


# Запуск окна
MyCustomWindow().ShowDialog()
