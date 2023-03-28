from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser, BaseUserManager,AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
from autoslug import AutoSlugField
from rest_framework.response import Response

from test_app.models import Sub_Category, Category

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
    def create_user(self, username, first_name, last_name,  email, age, gender, state, photo, phone_number,\
                    password=None, password2=None):

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
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        
        user = self.create_user(
            password = password,
            username = username,
            email=email,
            first_name = 'Admin',
            last_name= 'Admin',
            age = 1,
            gender = 'man',
            state = 1,
            photo = 'C:/Users/xatam/OneDrive/Pictures/Saved_Pictures/default_person_picture(2).png',
            phone_number = '+998111111111',
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
    email = models.EmailField(null=True, blank=True, verbose_name="email") # delete 'blank' and 'null'
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[_validate_phone], verbose_name="shaxsiy raqam") # ADD unique=True, ///  front 13 ta belgiga cheklov qo'yib qo'ysin !!!
    status = models.CharField(max_length=30, choices=STATUS, default='active', verbose_name='holati')
    student_tests = models.ForeignKey(Sub_Category, on_delete=models.CASCADE ,related_name="student_tests", blank=True, null=True)
    
    father_email = models.EmailField(blank=True, null=True, verbose_name='email') # delete 'blank' and 'null'
    father_number = models.CharField(max_length=20, null=True, blank=True, validators=[_validate_phone], verbose_name="ota-ona raqami") # ADD unique=True, ///  front 13 ta belgiga cheklov qo'yib qo'ysin !!!
    father_password = models.CharField(max_length=30, null=True, blank=True, verbose_name="ota-ona paroli")
    
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




class Result(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="test_results", verbose_name="O'quvchi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="result_category", verbose_name="categoriya")
    subcategory = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, related_name="result_subcategory", verbose_name="kichik kategoriya")
    ball = models.PositiveIntegerField(default=0, verbose_name="ball")
    tashxis = models.CharField(max_length=255, blank=True, null=True, verbose_name="tashxis")
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"







