from django.test import TestCase

# Create your tests here.


# """
# Django REST frameworkda, bir-to-kop o'zaro aloqada o'zgartirish qilish oddiy jihatdan boshqa massiv 
#     elementlarga o'girilishi bilan bir xil. Bitta-to-kop aloqani yangilash uchun, siz farovonliklarni 
#     serializersni update() metodini qayta yozib olishingiz lozim.
# Namuna ko'rab, agar sizda ikkita model bo'lsa: Book va Author, BookAuthor modeli orqali 
#     ko'plik-ko'paytirish aloqasi mavjud:
# """

# from django.db import models

# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     authors = models.ManyToManyField("Author", through="BookAuthor")

# class Author(models.Model):
#     name = models.CharField(max_length=100)

# class BookAuthor(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)

# """
# Endi, kitoblarni mualliflari bilan yangilashni serializers orqali amalga oshirishingiz kerak. 
#     Book modeli uchun bir serializers yaratishingiz kerak, authors maydonini ichiga olish kerak:
# """

# from rest_framework import serializers
# from .models import Book

# class BookSerializer(serializers.ModelSerializer):
#     authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)

#     class Meta:
#         model = Book
#         fields = ("id", "title", "authors")

# """
# Ushbu serializers-da biz authors maydonini PrimaryKeyRelatedField sifatida qo'shtik. 
#     Bu maydon bizga kitobingizning mualliflarini ro'yxatni so'ralib, buyruqda o'tkazilgan 
#     avtorlar soni bo'yicha ro'yxat yuzasidan kitoblarning mualliflarini yangilashga imkon beradi.
#     Aytgancha, serializersning update() metodini qayta yozish yoli bilan ko'plik-koplik aloqani
#     yangilashimiz kerak:
# """

# from rest_framework import serializers
# from .models import Book

# class BookSerializer(serializers.ModelSerializer):
#     authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)

#     class Meta:
#         model = Book
#         fields = ("id", "title", "authors")

#     def update(self, instance, validated_data):
#         authors = validated_data.pop("authors", None)
#         instance = super().update(instance, validated_data)

#         if authors is not None:
#             instance.authors.set(authors)

#         return instance

# """
# Ushbu update() metodida, biz birinchi navbatda authors datani tasdiqlangan ma'lumotlardan olamiz 
#     va uning lug'atidan u to'rtayamiz pop() metodidan foydalanib. Keyingi navbatda, update() metodining 
#     superiga Book modelining namunasi o'zgartirish uchun chaqirib olishimiz kerak. Oxirgi navbatda, biz
#     kitobning mualliflarini authors maydonida joylab, set() metodini ishlatib turib, ro'yxatni qayta tiklaymiz.
#     Massiv elementlar ro'yxatini o'zgartirish uchun set() metodidan foydalanishingiz zarur, chunki bu usul 
#     ro'yxatdagi avtomatik bog'lanishlarni to'liq moslashtirib, siz buyruqda to'g'ri kiritilgan ma'lumotlarni 
#     qo'llaydi. Bu hammasi! Endi siz buyruqni PUT yoki PATCH bilan API-ga yuborib, buyruq o'zida avtor 
#     ID-ning ro'yxatini yuborishingiz mumkin. Bunga qarab, siz kitobning mualliflarini o'zgartirishingiz mumkin.
# """