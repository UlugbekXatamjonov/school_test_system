from django.shortcuts import render
from pprint import pprint
import json

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Sub_Category, Category, Question, Answer
from .serializer import Sub_CategoryAPISerializer, CategoryAPISerializer, QuestionAPISerializer, AnswerAPISerializer, ResultSerializer

from user_app.models import Result, Student, PSTResult

# Viewset for API serializers

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status="active")
    serializer_class = CategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # lastest_result - o'quvchining eng oxirginchi yechgan psix testi natijasi
        if user.permission_to_test:
            lastest_result = PSTResult.objects.filter(user=user.id).latest('created_at')
            if user.is_authenticated:
                return Category.objects.filter(job=lastest_result.job, status='active')
        return Category.objects.none()


class Sub_CategoryViewset(viewsets.ModelViewSet):
    queryset = Sub_Category.objects.filter(status="active")
    serializer_class = Sub_CategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            """------------------------------------------------"""
            if user.permission_to_test:
                lastest_result = PSTResult.objects.filter(user=user.id).latest('created_at')
                categories = Category.objects.filter(job=lastest_result.job, status='active')
                sub_categories = Sub_Category.objects.filter(parent__in=categories, status='active')
                # sub_categories = sub_categories.filter(parent__in=categories)
                step_by_subcategory = user.step_by_subcategory

                # Umumiy subcategoriyalar ro'yhati
                total_subcategory = [] 

                for key, value in step_by_subcategory.items():
                    # tanlangan bitta categoriyaga bog'langan subcategoriyalar ro'yhati
                    selected_subcategory = [] 
                    for subcategory in sub_categories:
                        if int(key) == subcategory.parent.id:
                            selected_subcategory.append(subcategory)
                    # kerakli miqdorda olingan subcategoriyalarni umumiy categoriyalarga qo'shamiz
                    total_subcategory += selected_subcategory[:value]  

                """------------------------------------------------"""
                return total_subcategory
            return Sub_Category.objects.none()
        return Sub_Category.objects.none()


class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.filter(status="active")
    serializer_class = QuestionAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class AnswerViewset(viewsets.ModelViewSet):
    queryset = Answer.objects.filter(status="active")
    serializer_class = AnswerAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


""" ------------------------ CRUD Viewset -------------------- """

class ResultViewset(viewsets.ModelViewSet):
    """
        O'quvchi test yechganda, yechilgan testni balini hisoblaydi va yetarli % da to'g'ri yechsa 
        o'quvchini joriy categoriyasi bo'yicha keyingi bosqichga o'tkazadi
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [AllowAny]

    """ CRUD operations """

    """ ------------------------- Xatolik turlari --------------------------------- 
        101 - Requestdan kelgan malumotlarni ajratib olishda sodir bo'ladi
        102 - Requestdan kelgan malumotlar asosida bazadagi mos malumotlarni ajratib olishda sodir bo'ladi
        103 - Testning ball hisoblash qismida xatolik yuz berdi
        104 - update() da kerakli ma'lumot va o'zgaruvchilarni yig'ib olish qismida sodir bo'ladi
        105 - update() da balllarni hisoblash va category bosqichini oshirishda sodir bo'ladi
    """

    def create(self, request, *args, **kwargs):
        result_data = request.data

        """ Requestdan kelgan malumotlar ajratib olinadi(o'zining asl ma'lumot turida) """
        try:
            # requestdan kelgan subcategory id si
            request_subcategory = int(result_data['subcategory'])
            # requestdan kelgan belgilangan javoblar json dan asl ma'lumot turiga o'tgazildi
            request_answers_ids = json.loads(result_data['test_api'])
            # requestdan kelgan o'quvchi bali
            result_ball = int(result_data['ball'])
        except:
            return Response({'error': "101 - xatolik turi aniqlandi(ResultViewset)"})
        
        """ Requestdan kelgan malumotlar asosida bazadagi mos malumotlarni ajratib olamiz """
        try:
            data_subcategory = Sub_Category.objects.get(id=request_subcategory)
        
            data_answers = []  # bazadan ajratib olingan 'answer'lar(obyektlar)
            for answer_id in request_answers_ids:  # requestdan kelgan 'answer' 'id'lari asosida shu 'id'ga mos bazadagi 'answer'lar obyekt ko'rinishida ro'yhatga yig'ib olindi
                answer = Answer.objects.get(id=answer_id)
                data_answers.append(answer)
        except:
            return Response({'error': "102 - xatolik turi aniqlandi(ResultViewset)"})

        """ Yechilgan testlar bo'yicha ballarni hisoblash  """
        try:
            for answer in data_answers:
                if answer.true_answer == True:
                    result_ball += 1
            
            """ 5/5 bo'lganda Student malumotlarini ichidan joriy categoryning leveleini 1 taga oshirib qo'yamiz """
            student = Student.objects.get(id=result_data['user'])
            message = ""
            if result_ball == 5: # Agar hammasini to'g'ri topgan bo'lsa
                for key, value in student.step_by_subcategory.items():
                    if int(key) == data_subcategory.parent.id and data_subcategory.id == student.step_by_subcategory[key]:
                            student.step_by_subcategory[key] += 1                    
                            student.save()
                            message = "Tabriklaymiz siz keyingi bosqichga o'tdingiz !"
                    message = "Tabriklaymiz siz keyingi bosqichga o'tdingiz !"
        except:
            return Response({'error': "103 - xatolik turi aniqlandi(ResultViewset)"})

        """ ForegnKey Malumotlariga aniqlik kitilyapdi """
        user = False
        if 'user' in result_data:
            try:
                if int(result_data['user']) == int(request.user.id):
                    user = Student.objects.get(pk=str(result_data['user']))
                else:
                    return Response({"error": "Ro'yhatdan o'tgan user 'id'si, test yechgan user 'id'siga to'g'ri kelmadi!!!"})
            except Exception as e:
                return Response({"error": "Bunday user mavjud emas!!!"})

        subcategory = False
        if 'subcategory' in result_data:
            try:
                subcategory = Sub_Category.objects.get(
                    pk=str(result_data['subcategory']))
            except Exception as e:
                return Response({"error": "Bunday kichik kategoriya mavjud emas!!!"})

        """ Barcha tayor bo'lgan ma'lumotlar bazaga saqlanyapdi """
        try:
            new_result = Result.objects.create(
                user=user,
                subcategory=subcategory,
                ball=result_ball,
                test_api=result_data['test_api']
            )
            new_result.save()
            serializer = ResultSerializer(new_result)
            return Response({'message':message, 'data':serializer.data})
        except Exception as e:
            return Response({'errors': "Ma'lumot to'liq emas!!!"})


    def update(self, request, *args, **kwargs):
        result = self.get_object()
        data = request.data

        # kerakli qiymat va o'zgaruvchilarni yig'ib olamiz
        try:
            request_answer = json.loads(data['test_api'])[0]
            answer = Answer.objects.get(id=request_answer)
            student = Student.objects.get(id=result.user.id)
            data_subcategory = Sub_Category.objects.get(id=result.subcategory.id) 
            message = ""       
        except:
            return Response({"error":"104-xatolik turi aniqlandi(ResultViewset)"})

        # Agar belgilangan javob to'g'ri bo'lsa natijadagi ball ni 1ta ga oshiramiz va urinishlar sonini ham 1 taga oshiramiz
        try:
            if answer.true_answer == True:
                result.ball += 1
            result.try_count += 1
            result.save()

            # Agar kerakli miqdor 70% dan yuqori bo'lsa o'quvchi uchun keyingi bosqichni ochamiz
            margin = result.ball / result.try_count
            if margin >= 0.7:
                for key, value in student.step_by_subcategory.items():
                    if int(key) == data_subcategory.parent.id and result.subcategory.id == student.step_by_subcategory[key]:
                        student.step_by_subcategory[key] += 1                    
                        student.save()
                        message = "Tabriklaymiz siz keyingi bosqichga o'tdingiz !"
                    message = "Tabriklaymiz siz keyingi bosqichga o'tdingiz !"
        except:
            return Response({"error":"105-xatolik turi aniqlandi(ResultViewset)"})

        # subcategoriyga oydinlik kiritamiz
        try:
            try:
                subcategory = Sub_Category.objects.filter(pk=data['subcategory']).first()
            except:
                subcategory = None
        except Exception as e:
            return Response({"error": "Bunday  subkategoriya mavjud emas!!!"})

        # Yig'ilgan va xisob kitob qilingan malumotlarni baza ga saqlaymiz
        try:
            result.subcategory = subcategory if 'subcategory' in data else result.subcategory
            result.ball = result.ball
            result.try_count = result.try_count
                        
            result.save()
            serializer = ResultSerializer(result)
            return Response({'msg': "Ma'lumot muvaffaqiyatli yangilandi", "message":message, 'data': serializer.data})
        except Exception as e:
            return Response({'errors': "Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})


