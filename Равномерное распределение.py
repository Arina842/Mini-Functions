def distribute_values(min_depth=0, max_depth=21, min_value=81, max_value=94, step=0.5):
    """
    Равномерно распределяет значения из диапазона [min_value, max_value]
    по диапазону глубин [min_depth, max_depth] с шагом step.

    Args:
        min_depth: Минимальная глубина.
        max_depth: Максимальная глубина.
        min_value: Минимальное значение.
        max_value: Максимальное значение.
        step: Шаг глубины.

    Returns:
        Список значений, соответствующих глубинам.
    """

    depth_range = [depth for depth in frange(min_depth, max_depth + step, step)]
    num_values = len(depth_range)
    value_range = [min_value + (max_value - min_value) * i / (num_values - 1) for i in range(num_values)]
    for i in range(len(value_range)):
        print(depth_range[i],'-',value_range[i])

    return depth_range,value_range

# Функция frange для работы с float в range (необходима, так как range работает только с int)
def frange(start, stop, step):
  i = start
  while i < stop:
    yield i
    i += step

# Вызываем функцию и печатаем результат.
num_values,distribution = distribute_values()
print(num_values)
print(distribution)
