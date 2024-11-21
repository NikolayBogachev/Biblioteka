import json
import os
from typing import List, Optional


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

    def __init__(self, title: str, author: str, year: int, status: str = "в наличии", id: Optional[int] = None):
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

    def __str__(self) -> str:
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
    books (List[Book]): Список объектов книг в библиотеке.
    """

    def __init__(self, filename: str = "library_data.json"):
        """
        Инициализация объекта библиотеки.

        Параметры:
        filename (str): Имя файла для хранения данных. По умолчанию используется "library_data.json".
        """
        self.filename = filename
        self.books = self.load_books()  # Загружаем книги из файла

    def load_books(self) -> List[Book]:
        """
        Загружает книги из файла в список.

        Возвращает:
        List[Book]: Список объектов книг, загруженных из файла.
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
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> str:
        """
        Добавляет новую книгу в библиотеку.

        Параметры:
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.

        Возвращает:
        str: Сообщение об успешности добавления книги.
        """
        new_book = Book(title, author, year)  # Создаем объект книги
        new_book.id = self.generate_book_id()  # Генерируем уникальный ID для книги
        self.books.append(new_book)  # Добавляем книгу в список
        self.save_books()  # Сохраняем изменения в файл
        return f"Книга '{new_book.title}' успешно добавлена в библиотеку."

    def generate_book_id(self) -> int:
        """
        Генерирует уникальный идентификатор для книги.

        Возвращает:
        int: Новый уникальный ID книги.
        """
        return max([book.id for book in self.books], default=0) + 1

    def remove_book(self, book_id: int) -> str:
        """
        Удаляет книгу из библиотеки по ID.

        Параметры:
        book_id (int): ID книги, которую нужно удалить.

        Возвращает:
        str: Сообщение об успешности или неуспешности удаления.
        """
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)  # Удаляем книгу из списка
            self.save_books()  # Сохраняем изменения
            return f"Книга с ID {book_id} успешно удалена."
        else:
            return f"Книга с ID {book_id} не найдена."

    def search_books(self, search_term: str) -> List[Book]:
        """
        Ищет книги по заданному поисковому запросу.

        Параметры:
        search_term (str): Строка поиска (может быть частью названия, автора или года издания).

        Возвращает:
        List[Book]: Список книг, которые соответствуют поисковому запросу.
        """
        results = [book for book in self.books if search_term.lower() in book.title.lower() or
                                                    search_term.lower() in book.author.lower() or
                                                    search_term in str(book.year)]
        if results:
            return results
        else:
            return []  # Возвращаем пустой список, если ничего не найдено

    def change_status(self, book_id: int, new_status: str) -> str:
        """
        Изменяет статус книги по ID.

        Параметры:
        book_id (int): ID книги, для которой нужно изменить статус.
        new_status (str): Новый статус книги ("в наличии" или "выдана").

        Возвращает:
        str: Сообщение об успешности изменения статуса.
        """
        if new_status not in ["в наличии", "выдана"]:
            return "Неверный статус. Статус должен быть 'в наличии' или 'выдана'."

        book_to_update = next((book for book in self.books if book.id == book_id), None)
        if book_to_update:
            # Проверка, если книга уже в нужном статусе
            if new_status == "выдана" and book_to_update.status == "выдана":
                return f"Книга с ID {book_id} уже выдана."
            if new_status == "в наличии" and book_to_update.status == "в наличии":
                return f"Книга с ID {book_id} уже в наличии."

            book_to_update.status = new_status  # Обновляем статус книги
            self.save_books()  # Сохраняем изменения
            return f"Статус книги с ID {book_id} изменен на '{new_status}'."
        else:
            return f"Книга с ID {book_id} не найдена."

    def borrow_book(self, book_id: int) -> str:
        """
        Проверка и изменение статуса книги на "выдана".

        Параметры:
        book_id (int): ID книги, которую нужно взять.

        Возвращает:
        str: Сообщение об успешности операции.
        """
        book_to_borrow = self.get_book_by_id(book_id)
        if book_to_borrow:
            if book_to_borrow.status == "выдана":
                return f"Книга с ID {book_id} уже выдана."
            else:
                return self.change_status(book_id, "выдана")
        else:
            return f"Книга с ID {book_id} не найдена."

    def return_book(self, book_id: int) -> str:
        """
        Проверка и изменение статуса книги на "в наличии".

        Параметры:
        book_id (int): ID книги, которую нужно вернуть.

        Возвращает:
        str: Сообщение об успешности операции.
        """
        book_to_return = self.get_book_by_id(book_id)
        if book_to_return:
            if book_to_return.status == "в наличии":
                return f"Книга с ID {book_id} уже в наличии."
            else:
                return self.change_status(book_id, "в наличии")
        else:
            return f"Книга с ID {book_id} не найдена."

    def display_books(self):
        """
        Отображает все книги в библиотеке.

        Если библиотека пуста, выводится сообщение о том, что книг нет.

        Возвращает:
        str: Сообщение о наличии книг в библиотеке.
        """
        if not self.books:
            return "Нет доступных книг."
        else:
            return "\n".join(str(book) for book in self.books)

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Получает книгу по ID.

        Параметры:
        book_id (int): ID книги.

        Возвращает:
        Book или None: Книга с данным ID или None, если книга не найдена.
        """
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

        match choice:
            case "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                message = library.add_book(title, author, year)
                print(message)
                input("Нажмите Enter, чтобы вернуться в меню...")

            case "2":
                book_id = int(input("Введите ID книги для удаления: "))
                message = library.remove_book(book_id)
                print(message)
                input("Нажмите Enter, чтобы вернуться в меню...")

            case "3":
                search_term = input("Введите название, автора или год для поиска: ")
                results = library.search_books(search_term)
                if results:
                    for book in results:
                        print(book)
                else:
                    print("Книги не найдены.")
                input("Нажмите Enter, чтобы вернуться в меню...")

            case "4":
                books = library.display_books()
                print(books)
                input("Нажмите Enter, чтобы вернуться в меню...")

            case "5":  # Взять книгу
                book_id = int(input("Введите ID книги, которую хотите взять: "))
                message = library.change_status(book_id, "выдана")
                print(message)
                input("Нажмите Enter, чтобы вернуться в меню...")

            case "6":  # Вернуть книгу
                book_id = int(input("Введите ID книги, которую хотите вернуть: "))
                message = library.change_status(book_id, "в наличии")
                print(message)
                input("Нажмите Enter, чтобы вернуться в меню...")

            case "7":
                print("Выход из программы.")
                break

            case _:
                print("Некорректный выбор. Попробуйте еще раз.")
                input("Нажмите Enter, чтобы вернуться в меню...")


if __name__ == "__main__":
    menu()
