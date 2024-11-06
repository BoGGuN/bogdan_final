# Create your models here.
from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    birth_date = models.DateField("Дата рождения")

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="profile",
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    avatar = models.ImageField(
        verbose_name="Изображение",
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username


class Group(models.Model):
    name = models.CharField("Название", max_length=255)
    admin = models.ForeignKey(
        User,
        verbose_name="Админ группы",
        related_name="group_admin",
        on_delete=models.CASCADE,
    )
    subscribers = models.ManyToManyField(
        User,
        verbose_name="Участники",
        related_name="user_groups",
        blank=True,
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField("Название", max_length=255)
    text = models.TextField("Текст", blank=True)
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    edited_at = models.DateTimeField(
        verbose_name="Дата редактирования",
        auto_now=True,
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Группа",
        related_name="posts",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name="posts",
        on_delete=models.CASCADE,
    )
    image_field = models.ImageField(
        verbose_name="Изображение",
        upload_to="posts/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at", "title"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    edited_at = models.DateTimeField(
        verbose_name="Дата редактирования",
        auto_now=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name="comments",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Пост",
        related_name="post_comments",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username}, {self.created_at}"


class ItemsInBasket(models.Model):
    count = models.IntegerField("Кол-во")
    basket = models.ForeignKey(
        "Basket",
        verbose_name="Корзина",
        related_name="items_in_basket",
        on_delete=models.CASCADE,
    )
    items = models.ForeignKey(
        "Item",
        verbose_name="Товар",
        related_name="items_in_basket",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def __str__(self):
        return f"{self.basket.id} - {self.item.name}"


class Basket(models.Model):
    profile = models.OneToOneField(
        Profile,
        verbose_name="Профиль",
        related_name="basket",
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField(
        "Item",
        verbose_name="Товар в корзине",
        related_name="basket",
        through=ItemsInBasket,
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Item(models.Model):
    TYPE_CHOISES = (
        ("default", "Без типа"),
        ("electronics", "Электроника"),
        ("clothes", "Одежда"),
        ("toys", "Детские товары"),
        ("books", "Книги"),
        ("furniture", "Мебель"),
    )

    name = models.CharField("Название", max_length=255)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    type = models.CharField(choices=TYPE_CHOISES, default="default", max_length=255)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-type", "-name"]

    def __str__(self):
        return f"{self.type} - {self.name}"
