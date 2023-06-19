from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import TextChoices

from users.managers import UserManager


class User(AbstractBaseUser):
    class Roles(TextChoices):
        ADMIN = 'admin', 'Администратор'
        USER = 'user', 'Пользователь'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    objects = UserManager()

    first_name = models.CharField(max_length=150, blank=True, help_text='Имя пользователя')
    last_name = models.CharField(max_length=150, blank=True, help_text='Фамилия пользователя')
    email = models.EmailField(unique=True, null=True, help_text='Email пользователя')
    password = models.CharField(max_length=200, help_text='Пароль пользователя')
    phone = models.CharField(max_length=20, null=True, blank=True, help_text='Телефон пользователя')
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER, help_text='Роль пользователя')
    image = models.ImageField(upload_to='images/', null=True, help_text='Фото пользователя')
    is_active = models.BooleanField(default=True, help_text='Активен ли пользователь')
    last_login = models.DateTimeField(auto_now_add=True, help_text='Дата последней авторизации')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_superuser(self) -> bool:
        return self.is_admin

    @property
    def is_staff(self) -> bool:
        return self.is_admin

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label) -> bool:
        return self.is_admin

    @property
    def is_admin(self) -> bool:
        return self.role == User.Roles.ADMIN

    @property
    def is_user(self) -> bool:
        return self.role == User.Roles.USER
