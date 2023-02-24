
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class Author(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postrat = self.post_set.all().aggregate(postRating=Sum('rating'))
        prat = 0
        prat += postrat.get('postRating')
        comrat = self.account.comment_set.all().aggregate(commentRating=Sum('rating'))
        crat = 0
        crat += comrat.get('commentRating')
        self.ratingAuthor = prat * 3 + crat
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through="AuthorCategory")

    def __str__(self):
        return f'{self.categoryName}'

class AuthorCategory(models.Model):
	in_user = models.ForeignKey(User, on_delete=models.CASCADE)
	in_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    authorArticle = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = 'AR'
    news = 'NW'

    TEXT = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    textContent = models.CharField(max_length=2,
                                   choices=TEXT,
                                   default=news)
    creationTime = models.DateTimeField(auto_now_add=True)
    textCategory = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    postText = models.TextField()
    rating = models.IntegerField(default=1)

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        if self.rating:
            self.rating -= 1
            self.save()
        return self.rating

    def preview(self):
        return self.postText[0:123] + '...'

    def __str__(self):
        return f'{self.header} {self.postText}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentTime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating:
            self.rating -= 1
            self.save()

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )