from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser, BaseUserManager,AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
from autoslug import AutoSlugField
from rest_framework.response import Response

# Create your models here.


GENDER_CHOICES = (
    ('man','Man'),
    ('woman','Woman')
)

STATUS = (
    ('active', "Faol"),
    ("deactive", "Faol emas"),
    ("delate", "O'chirish"),
)

_validate_phone = RegexValidator(
    regex = r"^[\+]?[9]{2}[8]?[0-9]{2}?[0-9]{3}?[0-9]{2}?[0-9]{2}$",
    message = "Telefon raqamingiz 9 bilan boshlanishi va 12 belgidan oshmasligi lozim. Masalan: 998334568978",
)


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name,  email, age, \
        gender, state, photo, phone_number, father_number, password=None, password2=None):

        if not username:
            raise ValueError("Foydalanuvchida 'username' bo'lishi shart !")
        
        user = self.model(
            username = username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            age = age,
            gender = gender,
            state = state,
            photo = photo,
            phone_number = phone_number,
            father_number = father_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        
        user = self.create_user(
            password = password,
            username = username,
            first_name = 'Admin',
            last_name= 'last_name',
            email=email,
            age = 20,
            gender = 'man',
            state = 3,
            photo = 'C:/Users/xatam/OneDrive/Pictures/Saved_Pictures/default_person_picture(2).png',
            phone_number = '+998663216547',
            father_number = '+998663216547',
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Student(AbstractUser):    
    slug  = AutoSlugField(populate_from='first_name', unique=True)
    age = models.PositiveIntegerField(default=5, verbose_name="yosh")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='man', verbose_name="jins") # DELETE -> default
    state = models.PositiveIntegerField(default=1, verbose_name="sinf")
    photo  = models.ImageField(upload_to="user_photo", verbose_name="rasm", blank=True, null=True,\
            default='C:/Users/xatam/OneDrive/Pictures/Saved_Pictures/default_person_picture(2).png')
    email = models.EmailField(null=True, blank=True, verbose_name="email")
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[_validate_phone], verbose_name="shaxsiy raqam") # ADD unique=True, ///  front 13 ta belgiga cheklov qo'yib qo'ysin !!!
    father_number = models.CharField(max_length=20, null=True, blank=True, validators=[_validate_phone], verbose_name="ota-ona raqami") # ADD unique=True, ///  front 13 ta belgiga cheklov qo'yib qo'ysin !!!
    status = models.CharField(max_length=30, choices=STATUS, default='active', verbose_name='holati')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    created_at = models.DateTimeField(auto_now=True, verbose_name="yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"
        ordering = ("-created_at",)
        
    def __str__(self):
        text = f"{self.first_name}"
        return text

    def avatar_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.photo))

    avatar_tag.short_description = 'Rasmi'

    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin












