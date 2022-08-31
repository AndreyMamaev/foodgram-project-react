from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    ADMIN = 'admin'
    CHOICES = [
        ('admin', ADMIN),
        ('user', USER)
    ]
    username = models.CharField(
        'Имя пользователя', max_length=50, blank=False, unique=True
    )
    email = models.EmailField(
        'Email',
        blank=False,
        unique=True,
        validators=[validators.validate_email]
    )
    bio = models.TextField('О себе', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=30, blank=True, null=True
    )
    role = models.CharField(
        'Права юзера', max_length=150, choices=CHOICES, default='user'
    )
    first_name = models.CharField(
        'Имя', max_length=150, null=True, blank=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=150, null=True, blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return True if not self.is_staff else None

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def save(self, *args, **kwargs):
        if self.role == self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписавшийся пользователь',
        help_text='Задаётся автоматически аутентифицированный пользователь.'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Пользователь на которого подписались',
        help_text='Задаётся автоматически пользователь на '
        'записи которого подписались.'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique follow'
            )
        ]
