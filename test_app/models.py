from django.db import models
from django.core.validators import RegexValidator

from autoslug import AutoSlugField

# Create your models here.

STATUS = (
    ('active', "Faol"),
    ("deactive", "Faol emas"),
)

JOB_TYPES = (
    ('tabiat', "Tabiat"),
    ('texnika', "texnika"),
    ('belgi','Belgi'),
    ('sanat',"San'at"),
    ('inson', "Inson"),
)

timeDurationRegex = RegexValidator(regex = r"^\d{1,3}$")
        
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Katta kategoriya")
    slug = AutoSlugField(populate_from = 'name', unique=True)
    job = models.CharField(max_length=30, verbose_name='Kasb', blank=True, null=True, choices=JOB_TYPES, default='tabiat')
    description = models.CharField(max_length=350, blank=True, null=True, verbose_name="Kategoriya haqida")
    
    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at','status')
        verbose_name = "Katta kategoriya"
        verbose_name_plural = "Katta kategoriyalar"

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi")
    slug = AutoSlugField(populate_from = 'name', unique=True)
    parent = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, verbose_name = "Katta kategoriya")
    description = models.CharField(max_length=350, blank=True, null=True, verbose_name="Kategoriya haqida")
    number_of_questions = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Savollar soni")
    # number_of_answer = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Yechgan testlari soni")
    lesson_link  = models.CharField(max_length=300, verbose_name="Dars uchun link", blank=True, null=True)

    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at','status')
        verbose_name = "kichik kategoriya"
        verbose_name_plural = "kichik kategoriyalar"

    def __str__(self):
        return self.name


class Question(models.Model):
    category_id = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, related_name="question", verbose_name="Kategoriya")
    question = models.CharField(max_length=350, blank=True, null=True, verbose_name="Savol matni")
    slug = AutoSlugField(populate_from ='question', unique=True)
    photo = models.ImageField(upload_to="question_photo/%Y/%m/%d/", verbose_name="Rasm", blank=True, null=True)
    
    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at','status')
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        text = f"{self.category_id.name} - {self.question} - {self.slug}"
        return text


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer', verbose_name="Savol")
    answer = models.CharField(max_length=350, verbose_name="Variant", blank=True, null=True)
    slug = AutoSlugField(populate_from ='answer', unique=True)
    true_answer = models.BooleanField(default=False, verbose_name="To'g'ri javob", blank=True, null=True)
    
    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at','status')
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"

    def __str__(self):
        text = f"{self.question_id.category_id.name} - {self.answer} - {self.slug}"
        return text

