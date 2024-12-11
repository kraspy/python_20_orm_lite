from django.contrib import admin
from .models import Author, Book, Genre, Publisher, Store, Review

from books.models import Publisher, Review, Store


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author__name')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name', 'bio')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    list_editable = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class StoreAdmin(admin.ModelAdmin):
    pass
