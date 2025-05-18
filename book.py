# book.py
# Импортируем необходимые модули
from abc import ABC, abstractmethod
from decorators import check_conditions, PreConditionError, PostConditionError

# Абстрактный класс Product - базовый класс для всех продуктов в магазине
class Product(ABC):
    @abstractmethod
    def __init__(self, title, author, price, genre):
        # Инициализация базовых атрибутов продукта
        self.title = title
        self.author = author
        self.price = price
        self.genre = genre

    @abstractmethod
    def __str__(self):
        # Абстрактный метод для строкового представления продукта
        pass

    @property
    @abstractmethod
    def price(self):
        # Абстрактный геттер для цены
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        # Абстрактный сеттер для цены
        pass


# Функция-предусловие для проверки корректности названия
def is_valid_title(self, title, author, price, genre, article=None):
    # Проверяем, что название является строкой и не пустое
    return isinstance(title, str) and len(title) > 0

# Функция-постусловие для проверки корректности установки цены
def price_was_set(result, self, title, author, price, genre, article=None):
    # Проверяем, что цена установлена правильно
    return self.price == price

# Класс Book, наследующийся от Product - представляет книгу в магазине
class Book(Product):
    # Декоратор для проверки условий при создании книги
    @check_conditions(pre_conditions=[is_valid_title], post_conditions=[price_was_set])
    def __init__(self, title, author, price, genre, article=None):
        # Вызываем конструктор родительского класса
        super().__init__(title, author, price, genre)
        # Устанавливаем цену
        self._price = price
        # Артикул (двузначный, до 50)
        self.article = article or 0

    def __str__(self):
        # Возвращаем строковое представление книги с артикулом
        return f'[{self.article:02d}] {self.title} | Автор: {self.author} | Цена: {self._price} руб. | Жанр: {self.genre}'

    @property
    def price(self):
        # Геттер для получения цены
        return self._price

    @price.setter
    def price(self, value):
        # Сеттер для установки цены с проверками
        if not isinstance(value, (int, float)):
            raise ValueError("Цена должна быть числом")
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = value

class Magazine(Product):
    def __init__(self, title, author, price, genre, article=None):
        super().__init__(title, author, price, genre)
        self._price = price
        # Артикул (двузначный, больше 50)
        self.article = article or 50

    def __str__(self):
        return f'[{self.article:02d}] {self.title} | Цена: {self._price} руб. | Жанр: {self.genre}'
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        # Сеттер для установки цены с проверками
        if not isinstance(value, (int, float)):
            raise ValueError("Цена должна быть числом")
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = value 

class Newspaper(Product):
    def __init__(self, title, publisher, price, date_published, article=None):
        self.title = title
        self.publisher = publisher
        self.price = price
        self.date_published = date_published
        self.genre = "Газета"
        # Артикул (двузначный, больше 80)
        self.article = article or 80

    def __str__(self):
        return f'[{self.article:02d}] {self.title} | Издатель: {self.publisher} | Дата: {self.date_published} | Цена: {self._price} руб.'
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Цена должна быть числом")
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = value 