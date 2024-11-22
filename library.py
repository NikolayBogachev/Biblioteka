import json
import os
from datetime import datetime
from typing import List, Optional
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "в наличии"
    BORROWED = "выдана"


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

    def __init__(self, title: str, author: str, year: int, status: BookStatus = BookStatus.AVAILABLE, book_id: Optional[int] = None):
        """
        Инициализация объекта книги.

        Параметры:
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (BookStatus): Статус книги, по умолчанию "в наличии".
        """
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.book_id = book_id

    def __str__(self) -> str:
        """
        Возвращает строковое представление книги для удобного вывода.
        """
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status.value}"


class LibraryDataAccess:
    """
    Класс для работы с файлом данных библиотеки.
    """

    def __init__(self, filename: str = "library_data.json"):
        self.filename = filename

    def load_books(self) -> List[Book]:
        """
        Загружает книги из файла.
        """
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return []
        with open(self.filename, 'r', encoding='utf-8') as file:
            try:
                return [Book(**{**book, "status": BookStatus(book["status"])}) for book in json.load(file)]
            except (json.JSONDecodeError, KeyError):
                print("Ошибка при загрузке данных из JSON файла.")
                return []

    def save_books(self, books: List[Book]):
        """
        Сохраняет список книг в файл.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([{
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "status": book.status.value,
                "book_id": book.book_id
            } for book in books], file, ensure_ascii=False, indent=4)


class LibraryLogic:
    """
    Класс для реализации бизнес-логики библиотеки.

    Использует слой доступа к данным (LibraryDataAccess) для загрузки и сохранения списка книг.
    """

    def __init__(self, data_access: LibraryDataAccess):
        """
        Инициализирует экземпляр класса LibraryLogic.

        Аргументы:
            data_access (LibraryDataAccess): Экземпляр класса доступа к данным, используемый для загрузки и сохранения книг.

        Атрибуты:
            data_access (LibraryDataAccess): Ссылка на слой доступа к данным.
            Books (List[Book]): Список объектов Book, загруженных из хранилища.
        """
        self.data_access = data_access
        self.books = self.data_access.load_books()

    @staticmethod
    def _get_current_year() -> int:
        """
        Возвращает текущий год.

        Используется для проверки корректности года издания книги.
        """
        from datetime import datetime
        return datetime.now().year

    def _generate_book_id(self) -> int:
        """
        Генерирует уникальный идентификатор для новой книги.

        Возвращает:
            int: Уникальный идентификатор.

        Логика:
            1. Находит максимальный существующий book_id в текущем списке книг.
            2. Если книг нет, возвращает 1.
            3. Увеличивает максимальный ID на 1 и возвращает результат.
        """
        return max([book.book_id for book in self.books], default=0) + 1

    def add_book(self, title: str, author: str, year: int) -> str:
        """
        Добавляет новую книгу в библиотеку.

        Аргументы:
            title (str): Название книги.
            Author (str): Автор книги.
            Year (int): Год издания книги.

        Возвращает:
            str: Сообщение об успешном добавлении книги.

        Исключения:
            ValueError: Если данные книги не проходят проверку.

        Проверки:
            1. Название и автор не должны быть пустыми.
            2. Год издания книги должен быть в диапазоне от 1450 (изобретение книгопечатания) до текущего года.
        """

        new_book = Book(title, author, year)
        new_book.book_id = self._generate_book_id()
        self.books.append(new_book)
        self.data_access.save_books(self.books)
        return f"Книга '{new_book.title}' успешно добавлена в библиотеку."

    def remove_book(self, book_id: int) -> str:
        """
        Удаляет книгу из библиотеки по уникальному идентификатору.

        Аргументы:
            book_id (int): Уникальный идентификатор книги для удаления.

        Возвращает:
            str: Сообщение о результате операции.

        Логика:
            1. Находит книгу с указанным ID в списке `books`.
            2. Если книга найдена, удаляет её из списка и сохраняет изменения.
            3. Если книга не найдена, возвращает соответствующее сообщение.
        """
        book_to_remove = next((book for book in self.books if book.book_id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)  # Удаление книги
            self.data_access.save_books(self.books)  # Сохранение изменений
            return f"Книга с ID {book_id} успешно удалена."
        else:
            return f"Книга с ID {book_id} не найдена."

    def search_books(self, search_term: str) -> List[Book]:
        """
        Ищет книги по ключевому слову в названии, авторе или году издания.

        Аргументы:
            search_term (str): Строка для поиска (регистр игнорируется).

        Возвращает:
            List[Book]: Список книг, соответствующих поисковому запросу.

        Логика:
            1. Приводит поисковый запрос и данные о книгах к нижнему регистру для удобства сравнения.
            2. Ищет совпадения в полях `title`, `author` или `year` каждой книги.
        """
        return [
            book for book in self.books
            if search_term.lower() in book.title.lower()
            or search_term.lower() in book.author.lower()
            or search_term in str(book.year)
        ]

    def change_status(self, book_id: int, new_status: BookStatus) -> str:
        """
        Изменяет статус книги на новый.

        Аргументы:
            book_id (int): Уникальный идентификатор книги.
            new_status (BookStatus): Новый статус книги.

        Возвращает:
            str: Сообщение о результате операции.

        Логика:
            1. Находит книгу с указанным ID в списке `books`.
            2. Если книга найдена:
                - Проверяет, совпадает ли текущий статус с новым.
                - Если статус уже совпадает, возвращает сообщение об этом.
                - В противном случае обновляет статус книги и сохраняет изменения.
            3. Если книга не найдена, возвращает сообщение об ошибке.
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


def menu():
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

        choice = input("Выберите действие: ")

        match choice:
            case "1":
                while True:
                    while True:
                        title = input("Введите название книги: ").strip()
                        if not title:
                            print("Название книги не может быть пустым. Попробуйте снова.")
                            continue

                        existing_titles = [book.title.lower() for book in library.books]
                        if title.lower() in existing_titles:
                            print(f"Книга с названием '{title}' уже существует. Введите другое название.")
                            continue

                        break

                    author = input("Введите автора книги: ").strip()
                    if not author:
                        print("Имя автора не может быть пустым. Попробуйте снова.")
                        continue

                    try:
                        current_year = datetime.now().year
                        year = int(input("Введите год издания: ").strip())
                        if not (1500 <= year <= current_year):
                            print(f"Год издания должен быть между 1500 и {current_year}. Попробуйте снова.")
                            continue
                    except ValueError:
                        print("Год издания должен быть числом. Попробуйте снова.")
                        continue

                    print(library.add_book(title, author, year))
                    break
            case "2":
                book_id = int(input("Введите ID книги для удаления: "))
                print(library.remove_book(book_id))

            case "3":
                search_term = input("Введите название, автора или год для поиска: ")
                results = library.search_books(search_term)
                if results:
                    for book in results:
                        print(book)
                else:
                    print("Книги не найдены.")

            case "4":
                if not library.books:
                    print("Нет доступных книг.")
                else:
                    for book in library.books:
                        print(book)

            case "5":
                book_id = int(input("Введите ID книги, которую хотите взять: "))
                print(library.change_status(book_id, BookStatus.BORROWED))

            case "6":
                book_id = int(input("Введите ID книги, которую хотите вернуть: "))
                print(library.change_status(book_id, BookStatus.AVAILABLE))

            case "7":
                print("Выход из программы.")
                break

            case _:
                print("Некорректный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    menu()
