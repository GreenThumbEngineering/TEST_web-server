from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, deviceID, email, password, is_staff, is_superuser):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        deviceID=deviceID,
        email=email,
        is_staff=is_staff,
        is_active=True,
        is_superuser=is_superuser,
        last_login=now,
        date_joined=now,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, deviceID, email, password):
    return self._create_user(deviceID, email, password, False, False)

  def create_superuser(self, deviceID, email, password):
    user=self._create_user(deviceID, email, password, True, True)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    deviceID = models.CharField(max_length=11, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['deviceID']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)