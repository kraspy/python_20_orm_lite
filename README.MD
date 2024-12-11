## Полное описание созданных моделей, включая объяснение связей между ними.
### Book (Книга): Хранит основную информацию о книге.

Добавленные поля:
- `genre` (ManyToManyField к Genre): Жанр(ы), к которым относится книга. Связь "многие ко многим" — у одной книги может быть несколько жанров, и один жанр может относиться ко многим книгам.
- `publisher` (ForeignKey к Publisher): Издатель, выпустивший книгу. Связь "многие к одному" — у книги один издатель, у издателя может быть много книг. Указано blank=True, null=True для возможности отсутствия издателя.
- `store` (ManyToManyField к Store): Магазины, в которых продаётся книга. Связь "многие ко многим" — у одной книги может быть несколько магазинов, и один магазин может продавать много разных книг.

### Genre (Жанр): Хранит информацию о жанрах книг.

**Поля:**
- name (CharField): Название жанра.
- description (TextField): Описание жанра.

**Связи:**
- Многие ко многим с Book.

### Publisher (Издатель): Хранит информацию об издательстве.

**Поля:**
- title (CharField): Название издательства.
- country (CharField): Страна, в которой зарегистрировано издательство.

**Связи:**
- Один ко многим с Book (через foreign key у Book).

### Store (Магазин): Хранит информацию о книжных магазинах.

**Поля:**
- title (CharField): Название магазина.
- city (CharField): Город, где находится магазин.

**Связи:**
- Многие ко многим с Book.

### Review (Отзыв): Хранит отзывы (рецензии) на книги.

**Поля:**
- mark (PositiveIntegerField с валидаторами): Оценка книги от 1 до 5.
- comment (TextField): Текст отзыва.
- created_at (DateTimeField, auto_now_add=True): Время создания отзыва.
- book (ForeignKey к Book): Книга, к которой относится отзыв. Связь "многие к одному" — одна книга может иметь много отзывов, у одного отзыва — только одна книга.


## Пошаговые инструкции по созданию тестовых данных для издательств, магазинов и книг через административную панель.
1. Создаем Издательства.
2. Создаем Жанры.
3. В Книгах заполняем поля Издательства и жанра по созданных выше записям.

## Описание выполненных запросов, объясняя их логику и результаты.
```python
# Список книг, отфильтрованных по стране издательства.
Book.objects.filter(publisher__country='Россия')
```

```python
# Список книг, доступных в магазинах данного города.
Book.objects.filter(store__city='Красноярск')
```

```python
# Список книг с высоким средним рейтингом
avg = Book.objects.annotate(avg_reviews=Avg('reviews__mark'))
avg.filter(avg_reviews__gt=4.5)
```

```python
# Список словарей, где для каждого магазина указано название и количество книг.
Store.objects.values('title').annotate(Count('books'))
```

```python
# Список магазинов с информацией о количестве книг и самой поздней дате публикации, отсортированный по числу книг.
Store.objects.values('title').annotate(Max('books__published_date'), Count('books')).order_by('-books__count')

```

## Использование `select_related()` и `prefetch_related()`
### Простой запрос
```python
books = Book.objects.all()
for book in books:
    print(book.title, book.publisher.title)
```
```sql
SELECT "books_book"."id",
       "books_book"."title",
       "books_book"."author_id",
       "books_book"."published_date",
       "books_book"."description",
       "books_book"."publisher_id"
  FROM "books_book"

Execution time: 0.000298s [Database: default]
SELECT "books_publisher"."id",
       "books_publisher"."title",
       "books_publisher"."country"
  FROM "books_publisher"
 WHERE "books_publisher"."id" = 1
 LIMIT 21
...
```
### select_related()
```python
books = Book.objects.select_related('publisher').all()
for book in books:
    print(book.title, book.publisher.title)
```
```sql
SELECT "books_book"."id",
       "books_book"."title",
       "books_book"."author_id",
       "books_book"."published_date",
       "books_book"."description",
       "books_book"."publisher_id",
       "books_publisher"."id",
       "books_publisher"."title",
       "books_publisher"."country"
  FROM "books_book"
  LEFT OUTER JOIN "books_publisher"
    ON ("books_book"."publisher_id" = "books_publisher"."id")
```
### prefetch_related()
```python
books = Book.objects.prefetch_related('publisher').all()
for book in books:
    print(book.title, book.publisher.title)
```
```sql
SELECT "books_book"."id",
       "books_book"."title",
       "books_book"."author_id",
       "books_book"."published_date",
       "books_book"."description",
       "books_book"."publisher_id"
  FROM "books_book"

SELECT "books_publisher"."id",
       "books_publisher"."title",
       "books_publisher"."country"
  FROM "books_publisher"
 WHERE "books_publisher"."id" IN (1, 2, 3)
```