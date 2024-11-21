import pytest

from library import Library, Book


# Тест для класса Library
@pytest.fixture
def sample_library():
    """Создает экземпляр библиотеки для тестов."""
    library = Library("test_library.json")
    library.books = []
    return library


@pytest.fixture
def sample_book():
    """Создает объект книги для тестов."""
    return Book(title="Test Book", author="Test Author", year=2024)


# Тестирование добавления книги
def test_add_book(sample_library):
    message = sample_library.add_book("New Book", "Author", 2024)
    assert "успешно добавлена" in message
    assert len(sample_library.books) == 1
    assert sample_library.books[0].title == "New Book"
    assert sample_library.books[0].author == "Author"
    assert sample_library.books[0].year == 2024


# Тестирование удаления книги
def test_remove_book(sample_library, sample_book):

    sample_library.add_book(sample_book.title, sample_book.author, sample_book.year)
    book_id = sample_library.books[0].id

    message = sample_library.remove_book(book_id)
    assert "успешно удалена" in message
    assert len(sample_library.books) == 0


# Тестирование поиска книги
def test_search_books(sample_library, sample_book):
    sample_library.add_book(sample_book.title, sample_book.author, sample_book.year)
    search_term = "Test Book"
    results = sample_library.search_books(search_term)
    assert len(results) == 1
    assert results[0].title == sample_book.title

    results = sample_library.search_books("Test")
    assert len(results) == 1
    assert results[0].title == sample_book.title


# Тестирование изменения статуса книги
def test_change_status(sample_library, sample_book):
    sample_library.add_book(sample_book.title, sample_book.author, sample_book.year)
    book_id = sample_library.books[0].id

    message = sample_library.change_status(book_id, "выдана")
    assert "изменен на 'выдана'" in message
    assert sample_library.books[0].status == "выдана"

    message = sample_library.change_status(book_id, "выдана")
    assert "уже выдана" in message

    message = sample_library.change_status(book_id, "в наличии")
    assert "изменен на 'в наличии'" in message
    assert sample_library.books[0].status == "в наличии"

    message = sample_library.change_status(book_id, "неизвестный статус")
    assert "Неверный статус" in message


# Тестирование ошибки при удалении несуществующей книги
def test_remove_nonexistent_book(sample_library):
    message = sample_library.remove_book(999)
    assert "не найдена" in message


# Тестирование ошибки при изменении статуса несуществующей книги
def test_change_status_nonexistent_book(sample_library):
    message = sample_library.change_status(999, "выдана")
    assert "не найдена" in message

