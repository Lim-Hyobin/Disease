from django.db import models

# Create your models here.
from django.contrib.auth.models import User,BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, nickname, password, name, email, disease):
        user=self.model(
            username=username,
            nickname=nickname,
            name=name,
            email=email,
            disease=disease,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, nickname, username, password):
        user=self.create_user(
            username=username,
            nickname=nickname,
            password=password,
            name='',
            email='',
            disease='',
        )
        user.set_password(password)
        user.is_admin=True
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, default='')
    #아이디
    nickname = models.CharField(max_length=100, unique=True, default='')
    #닉네임
    name=models.CharField(max_length=30, default='')
    #이름
    email = models.EmailField(max_length=30,default='')
    #질병
    CHOICE_DISEASE=(
        ('당뇨병','당뇨병'),
        ('고혈압','고혈압'),
        
    )
    disease=models.CharField(max_length=50, choices=CHOICE_DISEASE,default='')
    
    objects=UserManager()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['nickname']

    def __str__(self):
        return self.username
