from django.db import models
from autoslug import AutoSlugField
from django.core.validators import RegexValidator



# Create your models here.

TEST_TYPES = (
    ('oddiy','Oddiy test'), # ballar yig'indisi bo'yicha hisoblash uchun 
    ('ota',"O'quvchi tepmeramentini aniqlash"), # 1 ta savol bor. Savolda 4 ta rasm bor tanlangan rasmga mos javob chiqadi
    ('ktta',"KASB TANLASHGA TAYYORLIKNI ANIQLASH"), # Variantlar Ha/Yo'q dan iborat 'Ha' lar yig'ilib hisoblanadi
    ("ehsa","Emotsional holati va stressni aniqlash"), # Savol ostidagi ballar yig'iladi
    ('kta',"Kasb tiplarini aniqlash"), # Variantlar Ha/Yo'q dan iborat 'Ha' lar yig'ilib hisoblanadi
)

JOB_TYPES = (
    ('no',"Yo'q"),
    ('tabiat', "Tabiat"),
    ('texnika', "texnika"),
    ('belgi','Belgi'),
    ('sanat',"San'at"),
    ('inson', "Inson"),
)

STATUS = (
    ('active', "Faol"),
    ("deactive", "Faol emas"),
    ("delate", "O'chirish"),
)

timeDurationRegex = RegexValidator(regex = r"^\d{1,3}$")

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Katta kategoriya")
    slug = AutoSlugField(populate_from = 'name', unique=True)
    description = models.CharField(max_length=350, blank=True, null=True, verbose_name="Kategoriya haqida")
    
    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at','status')
        verbose_name = "Katta kategoriya"
        verbose_name_plural = "Katta kategoriyalar"

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Kategoriya nomi")
    slug = AutoSlugField(populate_from = 'name', unique=True)
    parent = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Katta kategoriya")
    description = models.CharField(max_length=350, blank=True, null=True, verbose_name="Kategoriya haqida")
    question_type = models.CharField(max_length=100, choices=TEST_TYPES, default="oddiy", verbose_name="Test turi")
    number_of_questions = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Savollar soni")
    time_duration = models.CharField(validators = [timeDurationRegex], default=0, max_length=3, null=True, blank=True, verbose_name="Test davomiyligi")

    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at','status')
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Question(models.Model):
    category_id = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, related_name="question", verbose_name="Kategoriya")
    question = models.CharField(max_length=350, verbose_name="Savol matni")
    slug = AutoSlugField(populate_from ='question', unique=True)
    photo = models.ImageField(upload_to="question_photo/%Y/%m/%d/", verbose_name="Rasm", blank=True, null=True)
    job_type = models.CharField(max_length=100, choices=JOB_TYPES, default='no', verbose_name="Kasb turi")

    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at','status')
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        # return f"{self.category_id.name} - {self.question}"
        return self.question


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer', verbose_name="Savol")
    answer = models.CharField(max_length=350, verbose_name="Variant", blank=True, null=True)
    slug = AutoSlugField(populate_from ='answer', unique=True)
    ball = models.PositiveIntegerField(default=0, verbose_name="Variant ostidagi Ball", blank=True, null=True)
    true_answer = models.BooleanField(default=False, verbose_name="To'g'ri javob", blank=True, null=True)
    question_result = models.CharField(max_length=350, blank=True, null=True, verbose_name="Savol natijasi")
    photo = models.ImageField(upload_to="answer_photo/%Y/%m/%d/", blank=True, null=True)

    status = models.CharField(max_length=100, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at','status')
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"

    def __str__(self):
        # return f"{self.category_id.name} - {self.question}"
        return self.answer











