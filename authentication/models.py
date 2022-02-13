
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from .managers import UserManager



class UserType(models.Model):

    name = models.CharField('Имя',max_length=255)

    def __str__(self):

        return self.name

    class Meta:
        verbose_name = 'Тип пользавателей'
        verbose_name_plural = 'Типы пользователей'




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser
    user_type = models.ForeignKey(UserType,null=True,blank=True,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='Avatar/',null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    surname = models.CharField(max_length=255,null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    phone = models.TextField(null=True,blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользаватель'
        verbose_name_plural = 'Пользаватели'


class Rating(models.Model):
    user = models.ForeignKey(User,related_name='ratings',on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name='my_ratings',on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    ball = models.BigIntegerField(null=True,blank=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

class NotifcationType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Тип уведемлений'
        verbose_name_plural = 'Типы уведемлений'

    def __str__(self):
        return self.name

class Notification(models.Model):
    type = models.ForeignKey(NotifcationType,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='notifcations',on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name='my_notifcations',on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"{self.author} to {self.user} type: {self.type.name}"
    
    class Meta:
        verbose_name = 'Уведемление'
        verbose_name_plural = 'Уведемлений'


