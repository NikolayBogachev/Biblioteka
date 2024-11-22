import pytest
from library import LibraryLogic, Book, BookStatus, LibraryDataAccess


@pytest.fixture
def sample_file(tmpdir):
    """Создает временный файл с данными для теста."""
    # Создаем временный файл
    test_file = tmpdir.join("test_library.json")

    # Передаем путь к файлу для использования в тесте
    yield test_file


# Тест для класса LibraryLogic
@pytest.fixture
def sample_library(sample_file):
    """Создает экземпляр библиотеки для тестов с временным файлом."""
    data_access = LibraryDataAccess(str(sample_file))  # Передаем путь к временному файлу
    library = LibraryLogic(data_access)
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
    assert len(sample_library.books) == 1  # Убедитесь, что книга добавлена
    book_id = sample_library.books[0].book_id

    message = sample_library.remove_book(book_id)
    assert "успешно удалена" in message
    assert len(sample_library.books) == 0  # Убедитесь, что книга удалена


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
    book_id = sample_library.books[0].book_id

    # Проверка успешного изменения статуса
    message = sample_library.change_status(book_id, BookStatus.BORROWED)
    assert "изменен на 'выдана'" in message
    assert sample_library.books[0].status == BookStatus.BORROWED

    # Проверка попытки установить тот же статус
    message = sample_library.change_status(book_id, BookStatus.BORROWED)
    assert "уже имеет статус 'выдана'" in message

    # Проверка возврата книги
    message = sample_library.change_status(book_id, BookStatus.AVAILABLE)
    assert "изменен на 'в наличии'" in message
    assert sample_library.books[0].status == BookStatus.AVAILABLE


# Тестирование ошибки при удалении несуществующей книги
def test_remove_nonexistent_book(sample_library):
    message = sample_library.remove_book(999)
    assert "не найдена" in message


# Тестирование ошибки при изменении статуса несуществующей книги
def test_change_status_nonexistent_book(sample_library):
    message = sample_library.change_status(999, BookStatus.BORROWED)
    assert "не найдена" in message
