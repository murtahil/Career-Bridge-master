from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, fullname, phone, email, user_type, password):

        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(fullname=fullname, phone=phone, email=self.normalize_email(email), user_type=user_type, password=password)

        user.set_password(password)
        user.user = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, fullname, phone, email, user_type, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.model(fullname=fullname, phone=phone,  email=self.normalize_email(email), user_type=user_type, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(phone=phone, email=self.normalize_email(email), password=password)
        user.set_password(password)
        user.staff = True
        user.admin = True
        user.user = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):    
    USER_TYPE_CHOICES = (
        (1, 'University'),
        (2, 'Company'),
        (3, 'Select Category'),

    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    fullname = models.CharField(max_length=50)
    password = models.CharField(max_length=1000)
    phone = models.CharField(unique=True, max_length=13)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    website = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)    # a admin user; non super-user
    user = models.BooleanField(default=False)    # a admin user; non super-user
    admin = models.BooleanField(default=False)   # a superuser
    email_verify = models.BooleanField(default=False)
    phone_verify = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']    # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_user(self):
        "Is the local user  member?"
        return self.user

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    def get_absolute_url(self):
        return reverse("articles:article_detail", kwargs={"id": self.pk})


class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name