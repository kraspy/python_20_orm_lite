from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    description = models.TextField()
    genre = models.ManyToManyField('Genre', related_name='books')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, related_name='books', blank=True, null=True)
    store = models.ManyToManyField('Store', related_name='books', blank=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class Publisher(models.Model):
    title = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Store(models.Model):
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    mark = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    
    def __str__(self):
        return self.comment