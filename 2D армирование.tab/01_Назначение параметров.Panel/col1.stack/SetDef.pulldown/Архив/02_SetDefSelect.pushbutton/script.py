# -*- coding: utf-8 -*-

import clr
from pyrevit import forms, script
import wpf
from System import Windows

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

xamlfile = script.get_bundle_file('ui.xaml')

class MyCustomWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)
        self.ChBox.IsChecked = False

        self.SaveButton.Click += self.save_button_clicked
        self.ChBox.Checked += self.chBox_Checked
        self.ChBox.Unchecked += self.chBox_Unchecked

    def save_button_clicked(self, sender, event):
        try:
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

            # Закрыть окно после обработки
            self.Close()

        except Exception as e:
            print("Ошибка в save_button_clicked:", e)

    def chBox_Checked(self, sender, args):
        self.ChBox.IsChecked = True
        # try:
        #     print("CheckBox установлен: ", self.ChBox.IsChecked)
        # except Exception as e:
        #     print("Ошибка в chBox_Checked:", e)

    def chBox_Unchecked(self, sender, args):
        self.ChBox.IsChecked = False
        # try:
        #     print("CheckBox сброшен: ", self.ChBox.IsChecked)
        # except Exception as e:
        #     print("Ошибка в chBox_Unchecked:", e)

window = MyCustomWindow()
window.ShowDialog()


