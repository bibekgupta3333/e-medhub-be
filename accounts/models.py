from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from .validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.contrib import auth
from django.utils import timezone
from emedhub import settings
from .validators import (validate_phone_number,)
import uuid
from datetime import datetime

# Create your models here.


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_seller', True)
        extra_fields.setdefault('is_buyer', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An MyUser base class implementing a fully featured User model with
    admin-compliant permissions.

    email and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ('username'), unique=True,
        max_length=150,

        help_text=(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
    email = models.EmailField(('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'),
    )
    is_seller = models.BooleanField(
        ('seller status'),
        default=False,
        help_text=(
            'Designates whether the user is a seller.'),
    )
    is_buyer = models.BooleanField(
        ('buyer status'),
        default=False,
        help_text=(
            'Designates whether the user is a buyer.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


def image_path(_, filename):
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    new_file_name = unique_id+'.'+extension
    new_file_name = f"{datetime.now().date()}/{_.user}/{new_file_name}"
    print(new_file_name)
    return "users/"+new_file_name


class Profile(models.Model):
    phone = models.CharField(max_length=14,
                             validators=[validate_phone_number, ], blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(
        upload_to=image_path, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


fields = ['id', 'user', 'company_name', 'phone', 'bio', 'photo', 'address']


class CompanyProfile(Profile):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="company_profile", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class UserProfile(Profile):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user_profile", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class ResetToken(models.Model):
    token = models.UUIDField()
    email = models.CharField(max_length=100, blank=True)
    used = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email) + str(self.created_date)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            if instance.is_buyer:
                UserProfile.objects.create(user=instance)
            if instance.is_seller:
                CompanyProfile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver,
                  sender=MyUser)
