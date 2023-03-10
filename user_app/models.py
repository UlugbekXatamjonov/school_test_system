from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser
from django.core.validators import RegexValidator
from django.utils.html import mark_safe

# Create your models here.


SEX_CHOICES = (
    ('man','Man'),
    ('woman','Woman')
)

STATE = (
    ('1','1-sinf'),
    ('2','2-sinf'),
    ('3','3-sinf'),
    ('4','4-sinf'),
    ('5','5-sinf'),
    ('6','6-sinf'),
    ('7','7-sinf'),
    ('8','8-sinf'),
    ('9','9-sinf'),
    ('10','10-sinf'),
    ('11','11-sinf'),
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
from autoslug import AutoSlugField

class Student(AbstractUser):    
    slug  = AutoSlugField(populate_from='first_name', unique=True)
    age = models.PositiveIntegerField(default=5, verbose_name="yosh")
    sex = models.CharField(max_length=50, choices=SEX_CHOICES, default='man', verbose_name="jins") # DELETE -> default
    state = models.PositiveIntegerField(default=1, verbose_name="sinf")
    photo  = models.ImageField(upload_to="user_photo", verbose_name="rasm")
    email = models.EmailField(null=True, blank=True, verbose_name="email")
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[_validate_phone], verbose_name="shaxsiy raqam") # ADD unique=True, ///  front 13 ta belgiga cheklov qo'yib qo'ysin !!!
    father_number = models.CharField(max_length=20, null=True, blank=True, validators=[_validate_phone], verbose_name="ota-ona raqami") # ADD unique=True, ///  front 13 ta belgiga cheklov qo'yib qo'ysin !!!
    status = models.CharField(max_length=30, choices=STATUS, default='active', verbose_name='holati')
    
    created_at = models.DateTimeField(auto_now=True, verbose_name="yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"
        ordering = ("-created_at",)
        
    def __str__(self):
        text = f"{self.first_name}"
        # text = f"{self.first_name} {self.last_name} - {self.state}-sinf"
        return text

    def avatar_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.photo))

    avatar_tag.short_description = 'Rasmi'














