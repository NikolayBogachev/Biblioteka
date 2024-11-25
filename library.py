import json
import os
from datetime import datetime
from typing import List, Optional
from enum import Enum


class BookStatus(Enum):
    """
    Перечисление для состояния книги.
    - AVAILABLE: Книга доступна для выдачи.
    - BORROWED: Книга выдана пользователю.
    """
    AVAILABLE = "в наличии"
    BORROWED = "выдана"


class Book:
    """
    Класс для представления книги в библиотеке.

    Атрибуты:
    - title (str): Название книги.
    - author (str): Автор книги.
    - year (int): Год издания книги.
    - status (BookStatus): Статус книги (доступна или выдана).
    - book_id (Optional[int]): Уникальный идентификатор книги.

    Методы:
    - __str__: Строковое представление книги.
    """

    def __init__(self, title: str, author: str, year: int, status: BookStatus = BookStatus.AVAILABLE, book_id: Optional[int] = None):
        """
        Инициализирует объект книги.

        Параметры:
        - title (str): Название книги.
        - author (str): Автор книги.
        - year (int): Год издания.
        - status (BookStatus): Статус книги.
        - book_id (Optional[int]): Уникальный идентификатор книги (по умолчанию None).
        """
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.book_id = book_id

    def __str__(self) -> str:
        """
        Возвращает строковое представление книги в формате:
        ID: {book_id}, Title: {title}, Author: {author}, Year: {year}, Status: {status}

        Возвращаемое значение:
        - str: Строковое описание книги.
        """
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status.value}"


class LibraryDataAccess:
    """
    Класс для работы с данными библиотеки, которые хранятся в JSON-файле.

    Атрибуты:
    - filename (str): Имя файла, в котором хранятся данные библиотеки (по умолчанию 'library_data.json').

    Методы:
    - load_books: Загружает книги из файла.
    - save_books: Сохраняет список книг в файл.
    """

    def __init__(self, filename: str = "library_data.json"):
        """
        Инициализирует объект для работы с файлом данных библиотеки.

        Параметры:
        - filename (str): Имя файла для хранения данных.
        """
        self.filename = filename

    def load_books(self) -> List[Book]:
        """
        Загружает список книг из файла JSON.

        Возвращаемое значение:
        - List[Book]: Список объектов книг.

        Исключения:
        - Если файл не существует или поврежден, возвращается пустой список.
        """
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return []

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                books = []
                for book_data in data:
                    book_data["status"] = BookStatus(book_data["status"])
                    books.append(Book(**book_data))
                return books
        except (json.JSONDecodeError, KeyError):
            print("Ошибка при загрузке данных из JSON файла.")
            return []

    def save_books(self, books: List[Book]):
        """
        Сохраняет список книг в файл JSON.

        Параметры:
        - books (List[Book]): Список книг, которые нужно сохранить.
        """
        books_data = []
        for book in books:
            books_data.append({
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "status": book.status.value,
                "book_id": book.book_id
            })
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(books_data, file, ensure_ascii=False, indent=4)


class LibraryLogic:
    """
    Класс для реализации бизнес-логики библиотеки.

    Атрибуты:
    - data_access (LibraryDataAccess): Объект для доступа к данным библиотеки.
    - books (List[Book]): Список книг в библиотеке.

    Методы:
    - _get_current_year: Получает текущий год.
    - _generate_book_id: Генерирует уникальный идентификатор для новой книги.
    - add_book: Добавляет книгу в библиотеку.
    - remove_book: Удаляет книгу из библиотеки по ID.
    - search_books: Ищет книги по заданному критерию (название, автор или год).
    - change_status: Меняет статус книги (доступна или выдана).
    """

    def __init__(self, data_access: LibraryDataAccess):
        """
        Инициализирует объект логики библиотеки.

        Параметры:
        - data_access (LibraryDataAccess): Объект для работы с данными библиотеки.
        """
        self.data_access = data_access
        self.books = self.data_access.load_books()

    @staticmethod
    def _get_current_year() -> int:
        """
        Возвращает текущий год.

        Возвращаемое значение:
        - int: Текущий год.
        """
        return datetime.now().year

    def _generate_book_id(self) -> int:
        """
        Генерирует уникальный ID для новой книги, основываясь на максимальном ID существующих книг.

        Возвращаемое значение:
        - int: Генерируемый уникальный ID книги.
        """
        return max([book.book_id for book in self.books], default=0) + 1

    def add_book(self, title: str, author: str, year: int) -> str:
        """
        Добавляет книгу в библиотеку.

        Параметры:
        - title (str): Название книги.
        - author (str): Автор книги.
        - year (int): Год издания книги.

        Возвращаемое значение:
        - str: Сообщение об успешном добавлении книги.
        """
        new_book = Book(title, author, year)
        new_book.book_id = self._generate_book_id()
        self.books.append(new_book)
        self.data_access.save_books(self.books)
        return f"Книга '{new_book.title}' успешно добавлена в библиотеку."

    def remove_book(self, book_id: int) -> str:
        """
        Удаляет книгу по ID.

        Параметры:
        - book_id (int): ID книги для удаления.

        Возвращаемое значение:
        - str: Сообщение об успешном удалении книги или ошибке, если книга не найдена.
        """
        book_to_remove = next((book for book in self.books if book.book_id == book_id), None)
        if not book_to_remove:
            return f"Книга с ID {book_id} не найдена."

        self.books.remove(book_to_remove)
        self.data_access.save_books(self.books)
        return f"Книга с ID {book_id} успешно удалена."

    def search_books(self, search_term: str) -> List[Book]:
        """
        Ищет книги по критерию поиска (название, автор, год).

        Параметры:
        - search_term (str): Строка для поиска.

        Возвращаемое значение:
        - List[Book]: Список найденных книг.
        """
        search_term_lower = search_term.lower()
        return [
            book for book in self.books
            if search_term_lower in book.title.lower()
               or search_term_lower in book.author.lower()
               or search_term in str(book.year)
        ]

    def change_status(self, book_id: int, new_status: BookStatus) -> str:
        """
        Изменяет статус книги (доступна или выдана).

        Параметры:
        - book_id (int): ID книги, статус которой нужно изменить.
        - new_status (BookStatus): Новый статус книги.

        Возвращаемое значение:
        - str: Сообщение об успешном изменении статуса или ошибке, если книга не найдена.
        """
        book_to_update = next((book for book in self.books if book.book_id == book_id), None)
        if book_to_update:
            if book_to_update.status == new_status:
                return f"Книга с ID {book_id} уже имеет статус '{new_status.value}'."
            book_to_update.status = new_status
            self.data_access.save_books(self.books)
            return f"Статус книги с ID {book_id} изменен на '{new_status.value}'."
        else:
            return f"Книга с ID {book_id} не найдена."


def input_with_validation(prompt, validation_func=None, error_message="Неверный ввод. Попробуйте снова."):
    """
    Функция для ввода с валидацией.

    Параметры:
    - prompt (str): Сообщение для пользователя.
    - validation_func (Optional[callable]): Функция для проверки ввода (по умолчанию None).
    - error_message (str): Сообщение об ошибке при неверном вводе (по умолчанию "Неверный ввод. Попробуйте снова.").

    Возвращаемое значение:
    - str: Введенная строка, прошедшая валидацию.
    """
    while True:
        user_input = input(prompt)
        if validation_func:
            if validation_func(user_input):
                return user_input
            else:
                print(error_message)
        else:
            return user_input


def safe_input_int(prompt: str) -> int:
    """
    Запрашивает у пользователя ввод целого числа с обработкой ошибок.

    Параметры:
    - prompt (str): Строка для отображения приглашения на ввод.

    Возвращает:
    - int: Введенное пользователем целое число.
    """
    while True:
        try:
            value = int(input(prompt).strip())
            return value
        except ValueError:
            print("Ошибка: введите целое число.")


def input_new_book(library):
    """
    Логика добавления новой книги в библиотеку с обработкой ошибок ввода.

    Параметры:
    - library (Library): Объект библиотеки, в который добавляется новая книга.
    """
    global year
    while True:
        title = input_with_validation(
            "Введите название книги (или 'exit' для возврата): ",
            validation_func=lambda x: bool(x.strip()),
            error_message="Название книги не может быть пустым. Попробуйте снова."
        )
        if title is None:
            print("Возврат в главное меню.")
            return

        existing_titles = [book.title.lower() for book in library.books]
        if title.lower() in existing_titles:
            print(f"Книга с названием '{title}' уже существует. Введите другое название.")
            continue
        break

    while True:
        author = input_with_validation(
            "Введите автора книги (или 'exit' для возврата): ",
            validation_func=lambda x: bool(x.strip()),
            error_message="Имя автора не может быть пустым. Попробуйте снова."
        )
        if author is None:
            print("Возврат в главное меню.")
            return
        break

    while True:
        try:
            year = int(input("Введите год издания: ").strip())
        except ValueError:
            print("Год издания должен быть числом. Попробуйте снова.")
            continue

        current_year = datetime.now().year
        if not (1500 <= year <= current_year):
            print(f"Год издания должен быть между 1500 и {current_year}. Попробуйте снова.")
            continue
        break

    print(library.add_book(title, author, year))


def delete_book(library):
    """
    Логика удаления книги по ID из библиотеки.

    Параметры:
    - library (Library): Объект библиотеки, из которого удаляется книга.
    """
    while True:
        book_id = safe_input_int("Введите ID книги для удаления (или '0' для возврата): ")
        if book_id == 0:
            print("Возврат в главное меню.")
            return

        print(library.remove_book(book_id))
        break


def search_books(library):
    """
    Поиск книг в библиотеке по названию, автору или году издания.

    Параметры:
    - library (Library): Объект библиотеки, в которой будет осуществляться поиск.
    """
    search_term = input("Введите название, автора или год для поиска (или 'exit' для возврата): ").strip()
    if search_term.lower() == 'exit':
        print("Возврат в главное меню.")
        return

    results = library.search_books(search_term)
    if results:
        for book in results:
            print(book)
    else:
        print("Книги не найдены.")


def show_all_books(library):
    """
    Вывод всех книг в библиотеке.

    Параметры:
    - library (Library): Объект библиотеки, из которой выводятся книги.
    """
    if not library.books:
        print("Нет доступных книг.")
    else:
        for book in library.books:
            print(book)


def change_book_status(library, status):
    """
    Изменение статуса книги в библиотеке.

    Параметры:
    - library (Library): Объект библиотеки, в которой изменяется статус книги.
    - status (BookStatus): Новый статус для книги (например, доступна, выдана и т.д.).
    """
    while True:
        book_id = safe_input_int(
            f"Введите ID книги, чтобы изменить статус на '{status.value}' (или '0' для возврата): ")
        if book_id == 0:
            print("Возврат в главное меню.")
            return

        print(library.change_status(book_id, status))
        break


def menu():
    """
    Главное меню программы для взаимодействия с библиотекой. Пользователю предлагается выбрать действие,
    которое будет выполнено в зависимости от выбранной опции.

    Взаимодействие с пользователем:
    - Позволяет добавлять, удалять, искать книги, показывать все книги, а также изменять статус книг (взять или вернуть).
    - Программа продолжает работать до тех пор, пока пользователь не выберет опцию выхода.
    """
    data_access = LibraryDataAccess()
    library = LibraryLogic(data_access)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Показать все книги")
        print("5. Взять книгу")
        print("6. Вернуть книгу")
        print("7. Выход")

        choice = input("Выберите действие: ").strip()

        match choice:
            case "1":
                input_new_book(library)
            case "2":
                delete_book(library)
            case "3":
                search_books(library)
            case "4":
                show_all_books(library)
            case "5":
                change_book_status(library, BookStatus.BORROWED)
            case "6":
                change_book_status(library, BookStatus.AVAILABLE)
            case "7":
                print("Выход из программы.")
                break
            case _:
                print("Некорректный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    menu()
