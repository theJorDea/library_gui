# decorators.py
# Импортируем модуль time для измерения времени выполнения функций
import time

# Декоратор для логирования выполнения сценариев
# Принимает название сценария и создает декоратор для функции
def log_scenario(scenario_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Засекаем время начала выполнения
            start_time = time.time()
            # Выводим сообщение о начале сценария
            print(f"Начало сценария: '{scenario_name}' - Функция: '{func.__name__}'")
            # Выполняем саму функцию
            result = func(*args, **kwargs)
            # Засекаем время окончания
            end_time = time.time()
            # Вычисляем длительность выполнения
            duration = end_time - start_time
            # Выводим сообщение о завершении сценария
            print(f"Окончание сценария: '{scenario_name}' - Функция: '{func.__name__}'. Длительность: {duration:.4f} сек.")
            return result
        return wrapper
    return decorator


# Декоратор для проверки предусловий и постусловий функции
def check_conditions(pre_conditions=None, post_conditions=None):
    # Инициализируем пустые списки, если условия не переданы
    if pre_conditions is None:
        pre_conditions = []
    if post_conditions is None:
        post_conditions = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Проверяем все предусловия перед выполнением функции
            for condition in pre_conditions:
                if not condition(*args, **kwargs):
                    # Если предусловие не выполнено, вызываем исключение
                    raise PreConditionError(f"Предусловие не выполнено для функции '{func.__name__}': {condition.__name__ if hasattr(condition, '__name__') else condition}")
            
            # Выполняем основную функцию
            result = func(*args, **kwargs)
            
            # Проверяем все постусловия после выполнения функции
            for condition in post_conditions:
                if not condition(result, *args, **kwargs):
                    # Если постусловие не выполнено, вызываем исключение
                    raise PostConditionError(f"Постусловие не выполнено для функции '{func.__name__}': {condition.__name__ if hasattr(condition, '__name__') else condition}")
            return result
        return wrapper
    return decorator

# Пользовательское исключение для ошибок предусловий
class PreConditionError(Exception):
    pass

# Пользовательское исключение для ошибок постусловий
class PostConditionError(Exception):
    pass