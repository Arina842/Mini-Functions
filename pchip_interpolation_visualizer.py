"""
Скрипт для визуализации PCHIP-интерполяции из файлов данных
Автор: Арина
Дата: 27.03.2025
"""

# Импорт необходимых библиотек
import matplotlib.pyplot as plt  # Для построения графиков
import os  # Для работы с файловой системой
import numpy as np  # Для работы с массивами и математическими операциями
from pathlib import Path  # Для кросс-платформенной работы с путями

"""
ОБЩЕЕ ОПИСАНИЕ РАБОТЫ СКРИПТА:
1. Чтение данных: Скрипт ищет все файлы формата synthetic_interp_*.txt в указанной папке
2. Парсинг данных: Из каждого файла извлекаются узлы интерполяции (x) и коэффициенты кубических полиномов (c)
3. Восстановление кривых: Для каждого интервала между узлами рассчитываются 100 точек по формуле кубического полинома
4. Визуализация: Все кривые отображаются на одном графике с подписанными осями и легендой

КЛЮЧЕВЫЕ ОСОБЕННОСТИ:
- Обрабатывает несколько файлов данных одновременно
- Автоматически проверяет согласованность узлов и коэффициентов
- Генерирует плавные кривые между узлами интерполяции
- Выводит понятные сообщения об ошибках при проблемах с чтением файлов
"""


def read_interpolation_data():
    """
    Чтение и парсинг файлов с данными интерполяции

    Возвращает:
        dict: Словарь вида {filename: (x_nodes, coefficients), ...}

    Логика работы:
        1. Итерируется по всем файлам в целевой папке
        2. Для файлов, соответствующих шаблону synthetic_interp_*.txt:
           a. Парсит узлы интерполяции (секция "Узлы (x):")
           b. Парсит коэффициенты полиномов (секция "Коэффициенты (c):")
        3. Сохраняет данные в словарь
    """
    # Путь к папке с файлами данных (ЗАМЕНИТЕ НА СВОЙ)
    folder_path = r"C:\Users\Arina\PycharmProjects\PythonProject\interpolator_data"

    # Словарь для хранения данных {имя_файла: (узлы, коэффициенты)}
    interpolators_data = {}

    # Итерация по всем файлам в целевой папке
    for filename in os.listdir(folder_path):
        # Фильтрация по имени файла
        if filename.startswith("synthetic_interp_") and filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Чтение и разделение содержимого файла на строки
                    content = f.read().split("\n")

                # Парсинг узлов интерполяции (x)
                # Поиск начала и конца секции с узлами
                x_start = content.index("Узлы (x):") + 1
                x_end = content.index("", x_start)  # Пустая строка как разделитель
                # Преобразование строк в числа
                x_values = np.array([float(line.strip()) for line in content[x_start:x_end] if line.strip()])

                # Парсинг коэффициентов (c)
                c_start = content.index("Коэффициенты (c):") + 1
                # Чтение всех строк до конца файла и преобразование в числа
                c_values = np.array(
                    [list(map(float, line.strip().split())) for line in content[c_start:] if line.strip()]
                )

                # Сохранение в словарь
                interpolators_data[filename] = (x_values, c_values)

            except Exception as e:
                # Обработка ошибок с выводом сообщения
                print(f"Ошибка в файле {filename}: {e}")

    return interpolators_data


def restore_pchip(interpolators_data):
    """
    Восстановление и визуализация PCHIP-интерполяции

    Параметры:
        interpolators_data (dict): Словарь с данными из read_interpolation_data()

    Логика работы:
        1. Создает общее окно для графиков
        2. Для каждого файла данных:
           a. Проверяет согласованность узлов и коэффициентов
           b. Для каждого интервала рассчитывает 100 точек по формуле полинома
           c. Строит кривую на графике
        3. Настраивает и отображает график
    """
    # Создание фигуры для рисования (размер 12x6 дюймов)
    plt.figure(figsize=(12, 6))

    # Итерация по всем загруженным данным
    for filename, (x_nodes, coefficients) in interpolators_data.items():
        x_values = []  # Точки X для графика
        y_values = []  # Точки Y для графика

        # Проверка согласованности данных
        if len(x_nodes) - 1 != len(coefficients):
            print(f"Пропуск файла {filename}: несоответствие узлов и коэффициентов")
            continue  # Переход к следующему файлу

        # Обработка каждого интервала между узлами
        for i in range(len(x_nodes) - 1):
            # Границы интервала
            x_start = x_nodes[i]
            x_end = x_nodes[i + 1]

            # Коэффициенты кубического полинома: a, b, c, d
            a, b, c, d = coefficients[i]

            # Генерация 100 точек в текущем интервале
            x_interval = np.linspace(x_start, x_end, 100)

            # Расчет смещения относительно начала интервала
            t = x_interval - x_start

            # Расчет значений полинома: y = a*t³ + b*t² + c*t + d
            y_interval = a * t ** 3 + b * t ** 2 + c * t + d

            # Сохранение точек
            x_values.extend(x_interval)
            y_values.extend(y_interval)

        # Добавление кривой на график
        plt.plot(x_values, y_values, label=f"Интерполяция ({filename})")

    # Настройка внешнего вида графика
    plt.title("Интерполяционные кривые PCHIP")  # Заголовок
    plt.xlabel("X")  # Подпись оси X
    plt.ylabel("P(X)")  # Подпись оси Y
    plt.grid(True, linestyle='--', alpha=0.7)  # Сетка с пунктирными линиями
    plt.legend()  # Отображение легенды
    plt.tight_layout()  # Автоматическая настройка полей
    plt.show()  # Показ графика


# Основной блок выполнения
if __name__ == "__main__":
    # Загрузка данных
    interpolators_data = read_interpolation_data()

    if interpolators_data:
        # Построение графиков если данные есть
        restore_pchip(interpolators_data)
    else:
        # Сообщение если данных нет
        print("Нет данных для построения графиков. Проверьте:")
        print("1. Путь к папке с файлами")
        print("2. Формат файлов (должны быть synthetic_interp_*.txt)")
        print("3. Содержимое файлов (должны содержать узлы и коэффициенты)")
