# library.py
# Импортируем необходимые модули
import sqlite3
import time
from book import Book, Magazine, Newspaper
from decorators import log_scenario

# Миксин для логирования операций с базой данных
class DatabaseLoggingMixin:
    def log_db_action(self, action, table_name, data=None):
        # Формируем сообщение о действии с базой данных
        log_message = f"Database Action: {action} on table '{table_name}'"
        if data:
            log_message += f" with data: {data}"
        print(log_message)


# Основной класс магазина, включающий функционал логирования БД
class Store(DatabaseLoggingMixin):
    def __init__(self):
        self.products = {
            'books': [],
            'magazines': [],
            'newspapers': []
        }
        self.cart = []
        self.conn = sqlite3.connect('store.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.load_products()

    @log_scenario("Создание таблиц БД")
    def create_tables(self):
        # Логируем создание таблицы
        self.log_db_action("CREATE TABLE IF NOT EXISTS", "orders")
        # Создаем таблицу для заказов если она не существует
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title TEXT,
            author TEXT,
            price REAL,
            genre TEXT
        )''')
        self.conn.commit()

    def load_products(self):
        # Загружаем книги с артикулами до 50
        self.products['books'] = [
            Book('Война и мир', 'Лев Толстой', 500, 'Роман', 10),
            Book('Мастер и Маргарита', 'Михаил Булгаков', 400, 'Фантастика', 11),
            Book('Преступление и наказание', 'Федор Достоевский', 350, 'Классика', 12),
            Book('Анна Каренина', 'Лев Толстой', 450, 'Роман', 13),
            Book('Идиот', 'Федор Достоевский', 320, 'Классика', 14)
        ]
        
        # Загружаем журналы с артикулами больше 50
        self.products['magazines'] = [
            Magazine('Time', 'Time Inc.', 100, 'Политика', 51),
            Magazine('National Geographic', 'National Geographic Society', 200, 'Наука', 52),
            Magazine('Vogue', 'Condé Nast', 250, 'Мода', 53),
            Magazine('Forbes', 'Forbes Media', 180, 'Бизнес', 54),
            Magazine('Cosmopolitan', 'Hearst Communications', 150, 'Стиль жизни', 55)
        ]
        
        # Загружаем газеты с артикулами больше 80
        self.products['newspapers'] = [
            Newspaper('Ведомости', 'Business News Media', 50, '2024-03-20', 81),
            Newspaper('Коммерсантъ', 'Коммерсантъ', 60, '2024-03-20', 82),
            Newspaper('РБК', 'РБК Медиа', 55, '2024-03-20', 83)
        ]

    def list_products(self, category=None):
        if category:
            return self.products.get(category, [])
        return {cat: items for cat, items in self.products.items()}

    def add_to_cart(self, article, category=None):
        # Если категория не указана, ищем во всех категориях
        if category is None:
            for cat_name, products in self.products.items():
                for product in products:
                    if hasattr(product, 'article') and product.article == article:
                        self.cart.append({
                            'item': product,
                            'category': cat_name
                        })
                        return True
        else:
            # Если категория указана, ищем только в ней
            if category in self.products:
                for product in self.products[category]:
                    if hasattr(product, 'article') and product.article == article:
                        self.cart.append({
                            'item': product,
                            'category': category
                        })
                        return True
        
        # Если ничего не нашли, возвращаем False
        return False

    def view_cart(self):
        # Возвращаем содержимое корзины
        return self.cart

    def remove_from_cart(self, book_index):
        # Удаляем товар из корзины по индексу
        if 0 <= book_index < len(self.cart):
            del self.cart[book_index]
            return True
        return False

    @log_scenario("Сохранение заказа в БД")
    def save_order(self):
        # Сохраняем каждый товар из корзины в базу данных
        for item_data in self.cart:
            product = item_data['item']
            
            # Обрабатываем случай с газетами, у которых вместо author - publisher
            author = getattr(product, 'author', getattr(product, 'publisher', 'Неизвестно'))
            
            order_data = (product.title, author, product.price, product.genre)
            # Логируем операцию вставки
            self.log_db_action("INSERT", "orders", data=order_data)
            # Выполняем вставку данных
            self.cursor.execute('''INSERT INTO orders (product_title, author, price, genre) VALUES (?, ?, ?, ?)''',
                                order_data)
        # Сохраняем изменения и очищаем корзину
        self.conn.commit()
        self.cart.clear()

    def calculate_cart_total(self):
        # Вычисляем общую стоимость товаров в корзине
        return sum(item['item'].price for item in self.cart)