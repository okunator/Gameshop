from django.db import models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from store.models import Game

# #'''Extension of our Custom user model'''
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL)
#     profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
#     my_games = models.ManyToManyField(Game)
#
#     def __str__(self):
#         return str(self.user.username)
#
# #'''Signal that when a new user is created, also a new Profile for the user is created'''
# def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         try:
#             Profile.objects.create(user=instance)
#         except:
#             pass

# post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

#'''Custom User model overrides the built-in User model'''
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

USERNAME_REGEX='^[a-zA-Z0-9.@+-]*$'

class User(AbstractBaseUser):
    username = models.CharField(
        max_length=120,
        unique=True,
        validators=[
            RegexValidator(
                regex = USERNAME_REGEX,
                message = 'Username must be alphanumeric or contain any of the following ". @ + -"',
                code = 'invalid username',
            )
        ],
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    my_games = models.ManyToManyField(Game, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
