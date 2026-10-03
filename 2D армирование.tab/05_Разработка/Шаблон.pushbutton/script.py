# -*- coding: utf-8 -*-

"""Шаблон чистого скрипта для pyRevit с UI и логированием ошибок."""

__title__ = "Имя Кнопки"
__author__ = "Ваше Имя"
__doc__ = "Описание того, что делает ваш скрипт при наведении на кнопку"

# 1. Импорт библиотек Revit API
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# 2. Импорт библиотек pyRevit
from pyrevit import revit, forms, script

# Инициализируем логгер и вывод pyRevit
logger = script.get_logger()
output = script.get_output()

# Получаем текущий документ и интерфейс
doc = revit.doc
uidoc = revit.uidoc


def main():
    # ---- ШАГ 1: ВЫБОР ЭЛЕМЕНТОВ ЧЕРЕЗ UI ----
    # Вариант А: Быстрый сбор всех стен на активном виде (через API)
    all_walls = FilteredElementCollector(doc, doc.ActiveView.Id) \
        .OfCategory(BuiltInCategory.OST_Walls) \
        .WhereElementIsNotElementType() \
        .ToElements()

    if not all_walls:
        forms.alert("На активном виде не найдены элементы категории 'Стены'!", title="Внимание")
        return

    # Вариант Б: Выбор конкретных элементов пользователем через удобное окно pyRevit
    selected_walls = forms.SelectFromList.show(
        context=all_walls,
        title="Выберите стены для обработки",
        width=500,
        height=400,
        button_name="Запустить обработку",
        multiselect=True,
        # Лямбда-функция определяет, какой текст будет выведен в строке выбора
        name_attr="Name"
    )

    # Если пользователь закрыл окно или ничего не выбрал — выходим
    if not selected_walls:
        forms.alert("Операция отменена пользователем.", title="Отмена")
        return

    # Настраиваем прогресс-бар в нижнем углу Revit
    total_elements = len(selected_walls)

    # ---- ШАГ 2: БЕЗОПАСНАЯ ТРАНЗАКЦИЯ С ЛОГИРОВАНИЕМ ----
    # Используем контекстный менеджер pyRevit для транзакции
    with revit.Transaction("pyRevit: Обработка элементов"):
        try:
            success_count = 0

            for idx, element in enumerate(selected_walls, 1):
                # Обновляем прогресс-бар (шаг от 0 до 100)
                forms.ProgressBar.update_progress(idx, total_elements)

                # --- МЕСТО ДЛЯ ВАШЕЙ ЛОГИКИ ---
                # Пример: Меняем значение какого-нибудь параметра
                param = element.LookupParameter("Комментарии")
                if param and not param.IsReadOnly:
                    param.Set("Обработано через pyRevit")
                    success_count += 1
                else:
                    # Запись некритичной ошибки в консоль (скрипт не падает)
                    logger.warning(
                        "Элемент ID: {} доступен только для чтения или параметр не найден.".format(element.Id))
                # ------------------------------

            # Выводим красивый отчет пользователю при успешном завершении
            output.print_md("## 🎉 Скрипт успешно выполнен!")
            output.print_md("**Обработано элементов:** `{}` из `{}`".format(success_count, total_elements))

        except Exception as ex:
            # Если произошел критический сбой внутри транзакции:
            # pyRevit автоматически сделает RollBack (отменит изменения в модели)
            logger.error("Критическая ошибка при выполнении скрипта: {}".format(str(ex)))
            forms.alert("Произошла ошибка при выполнении. Изменения отменены. Подробности в консоли.", title="Ошибка")


if __name__ == "__main__":
    main()
