import json
import os


class Book:
    """
    Класс для представления книги.

    Атрибуты:
    title (str): Название книги.
    author (str): Автор книги.
    year (int): Год издания книги.
    status (str): Статус книги. Может быть "в наличии" или "выдана".
    id (int): Уникальный идентификатор книги.
    """

    def __init__(self, title: str, author: str, year: int, status: str = "в наличии", id: int = None):
        """
        Инициализация объекта книги.

        Параметры:
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги, по умолчанию "в наличии".
        """
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.id = id  # Добавлено для поддержки аргумента id

    def __str__(self):
        """
        Возвращает строковое представление книги для удобного вывода.

        Возвращает:
        str: Строка, содержащая информацию о книге (ID, название, автор, год, статус).
        """
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"


class Library:
    """
    Класс для представления библиотеки.

    Атрибуты:
    filename (str): Имя файла для сохранения и загрузки данных библиотеки (по умолчанию 'library_data.json').
    Books (list): Список объектов книг в библиотеке.
    """
    def __init__(self, filename: str = "library_data.json"):
        """
        Инициализация объекта библиотеки.

        Параметры:
        filename (str): Имя файла для хранения данных. По умолчанию используется "library_data.json".
        """
        self.filename = filename
        self.books = self.load_books()  # Загружаем книги из файла

    def load_books(self) -> list:
        """
        Загружает книги из файла в список.

        Возвращает:
        list: Список объектов книг, загруженных из файла.
        Если файл не существует, возвращает пустой список.
        """
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return []  # Если файл пустой, возвращаем пустой список
        with open(self.filename, 'r', encoding='utf-8') as file:
            try:
                return [Book(**book) for book in json.load(file)]
            except json.JSONDecodeError:
                print("Ошибка при загрузке данных из JSON файла.")
                return []

    def save_books(self):
        """
        Сохраняет список книг в файл.

        Сохраняет книги в формате JSON, где каждый объект книги представляется как словарь.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            # Преобразуем объекты книг в словари и сохраняем в JSON формате
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.

        Параметры:
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        """
        new_book = Book(title, author, year)  # Создаем объект книги
        new_book.id = self.generate_book_id()  # Генерируем уникальный ID для книги
        self.books.append(new_book)  # Добавляем книгу в список
        self.save_books()  # Сохраняем изменения в файл

    def generate_book_id(self) -> int:
        """
        Генерирует уникальный идентификатор для книги.

        Возвращает:
        int: Новый уникальный ID книги.
        """
        # Если библиотека пуста, начинаем с ID 1
        return max([book.id for book in self.books], default=0) + 1

    def remove_book(self, book_id: int):
        """
        Удаляет книгу из библиотеки по ID.

        Параметры:
        book_id (int): ID книги, которую нужно удалить.

        Если книга с таким ID не найдена, выводится сообщение об ошибке.
        """
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)  # Удаляем книгу из списка
            self.save_books()  # Сохраняем изменения
        else:
            print(f"Книга с ID {book_id} не найдена.")  # Сообщение, если книга не найдена

    def search_books(self, search_term: str):
        """
        Ищет книги по заданному поисковому запросу.

        Параметры:
        search_term (str): Строка поиска (может быть частью названия, автора или года издания).

        Возвращает:
        list: Список книг, которые соответствуют поисковому запросу.
        """
        return [book for book in self.books if search_term.lower() in book.title.lower() or
                                                    search_term.lower() in book.author.lower() or
                                                    search_term in str(book.year)]

    def change_status(self, book_id: int, new_status: str):
        """
        Изменяет статус книги по ID.

        Параметры:
        book_id (int): ID книги, для которой нужно изменить статус.
        new_status (str): Новый статус книги ("в наличии" или "выдана").

        Если статус неверный или книга не найдена, выводится сообщение об ошибке.
        """
        if new_status not in ["в наличии", "выдана"]:
            print("Неверный статус. Статус должен быть 'в наличии' или 'выдана'.")
            return
        book_to_update = next((book for book in self.books if book.id == book_id), None)
        if book_to_update:
            book_to_update.status = new_status  # Обновляем статус книги
            self.save_books()  # Сохраняем изменения
        else:
            print(f"Книга с ID {book_id} не найдена.")  # Сообщение, если книга не найдена

    def display_books(self):
        """
        Отображает все книги в библиотеке.

        Если библиотека пуста, выводится сообщение о том, что книг нет.
        """
        if not self.books:
            print("Нет доступных книг.")
        for book in self.books:
            print(book)  # Выводим информацию о каждой книге

    def get_book_by_id(self, book_id: int):
        return next((book for book in self.books if book.id == book_id), None)


def menu():
    library = Library()
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Показать все книги")
        print("5. Взять книгу")
        print("6. Вернуть книгу")
        print("7. Выход")

        choice = input("Выберите действие (или введите 'назад' для возврата в меню): ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)
            input("Книга добавлена. Нажмите Enter, чтобы вернуться в меню...")

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)
            input("Книга удалена (если такая была). Нажмите Enter, чтобы вернуться в меню...")

        elif choice == "3":
            search_term = input("Введите название, автора или год для поиска: ")
            results = library.search_books(search_term)
            if results:
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")
            input("Нажмите Enter, чтобы вернуться в меню...")

        elif choice == "4":
            library.display_books()
            input("Нажмите Enter, чтобы вернуться в меню...")

        elif choice == "5":  # Взять книгу
            book_id = int(input("Введите ID книги, которую хотите взять: "))
            book = library.get_book_by_id(book_id)
            if book:
                if book.status == "в наличии":
                    library.change_status(book_id, "выдана")
                    input(f"Книга '{book.title}' выдана. Нажмите Enter, чтобы вернуться в меню...")
                else:
                    input("Эта книга уже выдана. Нажмите Enter, чтобы вернуться в меню...")
            else:
                input("Книга с таким ID не найдена. Нажмите Enter, чтобы вернуться в меню...")

        elif choice == "6":  # Вернуть книгу
            book_id = int(input("Введите ID книги, которую хотите вернуть: "))
            book = library.get_book_by_id(book_id)
            if book:
                if book.status == "выдана":
                    library.change_status(book_id, "в наличии")
                    input(f"Книга '{book.title}' возвращена. Нажмите Enter, чтобы вернуться в меню...")
                else:
                    input("Эта книга уже находится в библиотеке. Нажмите Enter, чтобы вернуться в меню...")
            else:
                input("Книга с таким ID не найдена. Нажмите Enter, чтобы вернуться в меню...")

        elif choice == "7":
            print("Выход из программы.")
            break

        elif choice.lower() == 'назад':
            continue

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    menu()
