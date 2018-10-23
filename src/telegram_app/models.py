from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import transaction, models
from django.utils import timezone


class UserManager(BaseUserManager):
    @transaction.atomic
    def create_inactive_user(self, email, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        try:
            user = self.get(email=email)
        except self.model.DoesNotExist as e:
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.is_active = False
            user.is_staff = False
            user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=254, unique=True)
    full_name = models.CharField(verbose_name='ФИО', max_length=512, blank=True, default='')
    phone = models.CharField(verbose_name='Телефон', max_length=250, blank=True, default='')
    date_registration = models.DateTimeField(verbose_name='Дата регитрации', default=timezone.now)

    is_staff = models.BooleanField(verbose_name='статус персонала', default=False)
    is_active = models.BooleanField(verbose_name='active', default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class AccessToken(models.Model):
    LIFE_TIME_MINUTES = 30

    token = models.CharField(verbose_name='Токен доступа', max_length=1024, blank=True, default='', unique=True)
    unique_id_device = models.CharField(
        verbose_name='Уникальное ID устройства', max_length=1024, blank=True, unique=True)
    refresh_token = models.CharField(
        verbose_name='Токен обновления', max_length=1024, blank=True, default='', unique=True)
    created_at = models.DateTimeField(verbose_name='Дата и время создания', default=timezone.now)

    class Meta:
        verbose_name = 'Данные токена доступа'
        verbose_name_plural = 'Данные токена доступа'

    def __str__(self):
        return self.unique_id_device
