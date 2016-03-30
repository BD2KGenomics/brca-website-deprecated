from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, title, affiliation, institution, city, state, country, phone_number,
                    hide_number, hide_email):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            title=title,
            affiliation=affiliation,
            institution=institution,
            city=city,
            state=state,
            country=country,
            phone_number=phone_number,
            hide_number=hide_number,
            hide_email=hide_email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, title, affiliation, institution, city, state, country, phone_number,
                         hide_number, hide_email):
        user = self.create_user(email,
                                password=password,
                                title=title,
                                affiliation=affiliation,
                                institution=institution,
                                city=city,
                                state=state,
                                country=country,
                                phone_number=phone_number,
                                hide_number=hide_number,
                                hide_email=hide_email
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    title = models.TextField(blank=True)
    affiliation = models.TextField(blank=True)
    institution = models.TextField(blank=True)
    city = models.TextField(blank=True)
    state = models.TextField(blank=True)
    country = models.TextField(blank=True)
    phone_number = models.TextField(max_length=30, blank=True)
    # profile_image = ImageField(upload_to=get_image_path, blank=True, null=True)
    hide_number = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
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
        # Simplest possible answer: All admins are staff
        return self.is_admin
