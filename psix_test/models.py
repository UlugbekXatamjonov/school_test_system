from django.db import models
from autoslug import AutoSlugField
from django.core.validators import RegexValidator

# Create your models here.

JOB_TYPES = (
    ('tabiat', "Tabiat"),
    ('texnika', "texnika"),
    ('belgi','Belgi'),
    ('sanat',"San'at"),
    ('inson', "Inson"),
)

STATUS = (
    ('active', "Faol"),
    ("deactive", "Faol emas"),
)



class PSTSub_Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Kategoriya nomi")
    slug = AutoSlugField(populate_from = 'name', unique=True)
    description = models.CharField(max_length=350, blank=True, null=True, verbose_name="Kategoriya haqida")
    number_of_questions = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Savollar soni")
    
    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at','status')
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class PSTQuestion(models.Model):
    category_id = models.ForeignKey(PSTSub_Category, on_delete=models.CASCADE, related_name="pstquestion", verbose_name="Kategoriya")
    question = models.CharField(max_length=350, verbose_name="Savol matni")
    slug = AutoSlugField(populate_from ='question', unique=True)
    job_type = models.CharField(max_length=100, choices=JOB_TYPES, default='no', verbose_name="Kasb turi", blank=True, null=True)

    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at','status')
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return self.question


class PSTAnswer(models.Model):
    question_id = models.ForeignKey(PSTQuestion, on_delete=models.CASCADE, related_name='answer', verbose_name="Savol")
    answer = models.CharField(max_length=350, verbose_name="Variant", blank=True, null=True)
    slug = AutoSlugField(populate_from ='answer', unique=True)
    # ball = models.PositiveIntegerField(default=0, verbose_name="Variant ostidagi Ball", blank=True, null=True)
    true_answer = models.BooleanField(default=False, verbose_name="To'g'ri javob", blank=True, null=True)
    
    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at','status')
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"

    def __str__(self):
        return self.answer



