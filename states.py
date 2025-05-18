from typing import List, Tuple


def knapsack(items: List[Tuple[int, int]], K: int) -> int:
    """
    Жадный алгоритм для задачи о рюкзаке с ограничением на количество шагов.

    Args:
    items (List[Tuple[int, int]]): Список предметов (вес, стоимость).
    K (int): Максимальное количество шагов.

    Returns:
    int: Максимальная ценность, которую можно украсть.
    """
    # Сортируем предметы по стоимости на единицу веса
    items.sort(key=lambda x: x[1] / x[0], reverse=True)

    total_value = 0  # Общая ценность
    steps = 0  # Счетчик шагов

    for weight, value in items:
        if steps >= K:  # Проверяем лимит шагов
            break
        total_value += value  # Добавляем ценность предмета
        steps += 1  # Увеличиваем счетчик шагов

    return total_value  # Возвращаем максимальную ценность


# Пример использования
items = [(5, 10), (4, 40), (6, 30), (3, 50)]
K = 2
max_value = knapsack(items, K)
print(f"Максимальная ценность украденного: {max_value}")


