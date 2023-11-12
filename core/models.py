from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group as AuthGroup
from django.db import models
from django.utils.translation import gettext_lazy as _


from retail.models import Partner, Shop


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.EmailField(_("email address"), unique=True)
    middle_name = models.CharField(max_length=150, blank=True, verbose_name=_("Middle name"))
    shops = models.ManyToManyField(Shop, blank=True, verbose_name=_("Shops"))
    partner_profile = models.ForeignKey(
        Partner,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="user",
        verbose_name=_("Partner profile"),
    )


class Group(AuthGroup):
    class Meta:
        proxy = True
