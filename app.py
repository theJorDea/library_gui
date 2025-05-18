import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from book import Book, Magazine
from library import Store
from decorators import log_scenario, check_conditions, PreConditionError, PostConditionError

# Основной класс приложения
class BookStoreApp(App):
    def build(self):
        # Инициализируем магазин
        self.store = Store()

        # Создаем основной layout
        self.layout = BoxLayout(orientation='vertical')

        # Создаем элементы интерфейса для отображения списков
        self.book_list = Label(size_hint_y=None, height=200)
        self.cart_list = Label(size_hint_y=None, height=200)

        # Добавляем кнопки для категорий
        self.show_books_button = Button(text='Показать книги')
        self.show_magazines_button = Button(text='Показать журналы')
        self.show_newspapers_button = Button(text='Показать газеты')
        
        self.show_books_button.bind(on_press=lambda x: self.show_category_wrapper(x, 'books'))
        self.show_magazines_button.bind(on_press=lambda x: self.show_category_wrapper(x, 'magazines'))
        self.show_newspapers_button.bind(on_press=lambda x: self.show_category_wrapper(x, 'newspapers'))

        # Поле ввода и кнопка для добавления в корзину
        self.add_to_cart_input = TextInput(hint_text='Номер товара для добавления в корзину')
        self.add_to_cart_button = Button(text='Добавить в корзину')
        self.add_to_cart_button.bind(on_press=self.add_to_cart_wrapper)

        # Поле ввода и кнопка для удаления из корзины
        self.remove_from_cart_input = TextInput(hint_text='Номер товара для удаления из корзины')
        self.remove_from_cart_button = Button(text='Удалить из корзины')
        self.remove_from_cart_button.bind(on_press=self.remove_from_cart_wrapper)

        # Кнопка для отображения корзины
        self.show_cart_button = Button(text='Показать корзину')
        self.show_cart_button.bind(on_press=self.show_cart_wrapper)

        # Кнопка для сохранения заказа
        self.save_order_button = Button(text='Сохранить заказ')
        self.save_order_button.bind(on_press=self.save_order_wrapper)

        # Добавляем все элементы в layout
        self.layout.add_widget(self.show_books_button)
        self.layout.add_widget(self.show_magazines_button)
        self.layout.add_widget(self.show_newspapers_button)
        self.layout.add_widget(self.book_list)
        self.layout.add_widget(self.add_to_cart_input)
        self.layout.add_widget(self.add_to_cart_button)
        self.layout.add_widget(self.remove_from_cart_input)
        self.layout.add_widget(self.remove_from_cart_button)
        self.layout.add_widget(self.show_cart_button)
        self.layout.add_widget(self.save_order_button)
        self.layout.add_widget(self.cart_list)

        return self.layout

    # Обертки для методов с логированием
    def show_category_wrapper(self, instance, category):
        self.log_action(f"show_{category}")
        self.show_category(instance, category)

    def valid_cart_addition(self, instance, *args):
        # This is a simple pre-condition that always returns True
        # You can add actual validation logic here if needed
        return True

    # Define the post-condition function properly
    def cart_not_empty(result, self, instance, *args):
        # Check that the cart is not empty after adding an item
        return len(self.store.view_cart()) > 0
    
    @log_scenario("Добавление товара в корзину")
    @check_conditions(
        pre_conditions=[lambda self, instance, *args: True],
        post_conditions=[lambda result, self, instance, *args: len(self.store.view_cart()) > 0]
    )
    def add_to_cart(self, instance, *args):
        try:
            # Получаем артикул товара
            article = int(self.add_to_cart_input.text)
            
            # Добавляем товар в корзину по артикулу
            success = self.store.add_to_cart(article)
            
            if success:
                # Очищаем поле ввода
                self.add_to_cart_input.text = ''
                self.book_list.text += "\n\nТовар с артикулом " + str(article) + " добавлен в корзину!"
            else:
                self.book_list.text += "\n\nОшибка: Товар с артикулом " + str(article) + " не найден."
        except ValueError:
            self.book_list.text += "\n\nОшибка: Введите артикул товара (число)."
        except PostConditionError as e:
            print(f"Постусловие после добавления в корзину не выполнено: {e}")

    def remove_from_cart_wrapper(self, instance, *args):
        self.log_action("remove_from_cart")
        self.remove_from_cart(instance, *args)

    def show_cart_wrapper(self, instance, *args):
        self.log_action("show_cart")
        self.show_cart(instance, *args)

    def save_order_wrapper(self, instance, *args):
        self.log_action("save_order")
        self.save_order(instance, *args)

    # Основные методы работы с магазином
    @log_scenario("Отображение категории")
    def show_category(self, instance, category):
        # Сохраняем текущую категорию
        self.current_category = category
        products = self.store.list_products(category)
        category_names = {
            'books': 'Книги',
            'magazines': 'Журналы',
            'newspapers': 'Газеты'
        }
        product_list = []
        for product in products:
            product_list.append(f'{str(product)}')
        
        self.book_list.text = f"{category_names[category]}:\n" + "\n".join(product_list)

    @log_scenario("Удаление товара из корзины")
    def remove_from_cart(self, instance, *args):
        try:
            # Преобразуем введенный номер товара в индекс
            item_index = int(self.remove_from_cart_input.text) - 1
            # Удаляем товар из корзины
            self.store.remove_from_cart(item_index)
            # Очищаем поле ввода
            self.remove_from_cart_input.text = ''
        except ValueError:
            self.cart_list.text = "Ошибка: Введите номер товара для удаления."
        except IndexError:
            self.cart_list.text = "Ошибка: Товары с таким номером в корзине не существуют."

    @log_scenario("Отображение корзины")
    def show_cart(self, instance, *args):
        # Получаем содержимое корзины
        cart = self.store.view_cart()
        
        if cart:
            # Словарь для перевода категорий
            category_names = {
                'books': 'Книга',
                'magazines': 'Журнал',
                'newspapers': 'Газета'
            }
            
            # Если корзина не пуста, показываем её содержимое и общую стоимость
            cart_items = []
            for i, item in enumerate(cart):
                product = item['item']
                category = item['category']
                cart_items.append(f'{i + 1}. [{category_names.get(category, "Товар")}] {str(product)}')
                
            total = self.store.calculate_cart_total()
            self.cart_list.text = "Ваша корзина:\n" + "\n".join(cart_items) + f"\n\nОбщая стоимость: {total} руб."
        else:
            self.cart_list.text = "Ваша корзина пуста."

    @log_scenario("Сохранение заказа")
    def save_order(self, instance, *args):
        # Сохраняем заказ в базу данных
        self.store.save_order()
        self.cart_list.text = "Заказ сохранен в базе данных!"

    def add_to_cart_wrapper(self, instance, *args):
        self.log_action("add_to_cart")
        # Если текущая категория не задана, используем 'books' по умолчанию
        if not hasattr(self, 'current_category'):
            self.current_category = 'books'
        self.add_to_cart(instance, *args)

# Миксин для логирования действий
class LoggingMixin:
    def log_action(self, action_name):
        # Логируем действие пользователя
        print(f"Действие пользователя: {action_name}")

# Метакласс для регистрации действий
# Метакласс - это класс, который создает другие классы
# Он позволяет автоматически регистрировать все методы, начинающиеся с 'action_'
class ActionRegistryMeta(type):
    def __new__(mcs, name, bases, attrs):
        # mcs - сам метакласс
        # name - имя создаваемого класса
        # bases - родительские классы
        # attrs - словарь атрибутов и методов класса

        # Создаем словарь для хранения действий
        actions = {}

        # Перебираем все атрибуты создаваемого класса
        for name_attr, value in attrs.items():
            # Проверяем, является ли атрибут методом, начинающимся с 'action_'
            if name_attr.startswith('action_') and callable(value):
                # Удаляем префикс 'action_' и добавляем метод в словарь действий
                # Например: 'action_test_action' станет 'test_action'
                actions[name_attr[7:]] = value

        # Добавляем словарь actions в атрибуты класса
        # Теперь к нему можно обращаться через self.actions
        attrs['actions'] = actions

        # Создаем класс с помощью родительского метакласса type
        return super().__new__(mcs, name, bases, attrs)

# Финальный класс приложения с логированием и метаклассом
# metaclass=ActionRegistryMeta указывает, что класс должен быть создан с помощью нашего метакласса
class LoggedBookStoreApp(BookStoreApp, LoggingMixin, metaclass=ActionRegistryMeta):
    # Тестовое действие (демонстрационное)
    def action_test_action(self, instance, *args):
        print("Выполнено тестовое действие через метакласс!")

    # Новое полезное действие - очистка корзины
    def action_clear_cart(self, instance, *args):
        self.store.cart.clear()
        self.cart_list.text = "Корзина очищена!"
        print("Корзина успешно очищена")

    # Обертки для действий с правильной передачей аргументов
    def test_action_wrapper(self, instance, *args):
        self.actions['test_action'](instance, *args)

    def clear_cart_wrapper(self, instance, *args):
        self.actions['clear_cart'](instance, *args)

    def build(self):
        layout = super().build()

        # Кнопка для тестового действия
        test_button = Button(text='Выполнить тестовое действие')
        test_button.bind(on_press=self.test_action_wrapper)

        # Кнопка для очистки корзины
        clear_cart_button = Button(text='Очистить корзину')
        clear_cart_button.bind(on_press=self.clear_cart_wrapper)

        # Добавляем кнопки в интерфейс
        layout.add_widget(test_button)
        layout.add_widget(clear_cart_button)
        return layout

# Пример использования:
# 1. При создании класса LoggedBookStoreApp метакласс находит метод action_test_action
# 2. Создает словарь actions = {'test_action': action_test_action}
# 3. При нажатии кнопки вызывается метод из словаря actions по ключу 'test_action'

if __name__ == '__main__':
    # Запускаем приложение
    LoggedBookStoreApp().run()