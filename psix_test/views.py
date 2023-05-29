from django.shortcuts import render
import json
from pprint import pprint

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user_app.models import PSTResult
from .models import PSTSub_Category, PSTQuestion, PSTAnswer
from .serializers import PSTSub_CategorySerializer, PSTQuestionSerializer, PSTAnswerSerializer, \
    PSTResultSerializer

# Create your views here.

class PSTSub_CategoryViewset(ModelViewSet):
    queryset = PSTSub_Category.objects.filter(status='active')
    serializer_class = PSTSub_CategorySerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

class PSTQuestionViewset(ModelViewSet):
    queryset = PSTQuestion.objects.filter(status='active')
    serializer_class = PSTQuestionSerializer
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

class PSTAnswerViewset(ModelViewSet):
    queryset = PSTAnswer.objects.filter(status='active')
    serializer_class = PSTAnswerSerializer
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

class PSTResultViewset(ModelViewSet):
    queryset = PSTResult.objects.all()
    serializer_class = PSTResultSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user

        try:
            if 'subcategory' in request_data:
                subcategory = PSTSub_Category.objects.get(id = request_data['subcategory'])
            else:
                subcategory = None
        except:
            return Response({'error':"Bunday kategoriya mavjud emas !"})


        """ Requestdan kelgan malumotlar ajratib olinadi(o'zining asl ma'lumot turida) """
        try:
            request_tests = json.loads(request_data['test_api']) # requestdan kelgan testlar va belgilangan javoblar json dan asl ma'lumot turiga o'tgazildi
            request_tests = request_tests['tests']

            request_test_ids = []  # requestdan kelgan testlar idsi to'plangan list
            request_answer_ids = []  # requestdan kelgan answer idsi to'plangan list

            for test in request_tests:  # tsikl yordamida test va answer idlarini bo'sh ro'yhatga qo'shib olindi
                request_test_ids.append(test['test_id'])
                request_answer_ids.append(test['answer_id'])
        except:
            return Response({'error':"Requestdan kelgan malumotlar ajratib olishda xatolik !"})


        """ Requestdan kelgan malumotlar asosida bazadagi mos malumotlarni ajratib olamiz """
        try:
            data_tests = []  # bazadan ajratib olingan 'test'lar(obyektlar)
            for test_id in request_test_ids:  # requestdan kelgan test 'id'lari asosida shu 'id'ga mos bazadagi testlar obyekt ko'rinishida ro'yhatga yig'ib olindi
                test = PSTQuestion.objects.get(id=test_id)
                data_tests.append(test)

            data_answers = []  # bazadan ajratib olingan 'answer'lar(obyektlar)
            for answer_id in request_answer_ids:  # requestdan kelgan 'answer' 'id'lari asosida shu 'id'ga mos bazadagi 'answer'lar obyekt ko'rinishida ro'yhatga yig'ib olindi
                a = PSTAnswer.objects.get(id=answer_id)
                data_answers.append(a)
        except:
            return Response({'error':"Requestdan kelgan malumotlar asosida bazadagi mos malumotlarni ajratib olishda xatolik !"})


        """ Eng yuqori 'True' qiymatiga ega kasbni aniqlash """
        try:
            job_balls = {
                'tabiat' : 0,
                "texnika" : 0,
                "belgi" : 0,
                "sanat" : 0,
                "inson" : 0
            }

            for test_couple in request_tests:
                """ Belgilangan variantlardan kasb bo'yicha to'plangan ballni hisoblash """
                data_test = PSTQuestion.objects.get(id=test_couple['test_id'])
                data_answer = PSTAnswer.objects.get(id=test_couple['answer_id'])

                if data_test.job_type == 'tabiat' and data_answer.true_answer == True:
                    job_balls['tabiat'] += 1
                elif data_test.job_type == 'texnika' and data_answer.true_answer == True:
                    job_balls['texnika'] += 1
                elif data_test.job_type == 'belgi' and data_answer.true_answer == True:
                    job_balls['belgi'] += 1
                elif data_test.job_type == 'sanat' and data_answer.true_answer == True:
                    job_balls['sanat'] += 1
                elif data_test.job_type == 'inson' and data_answer.true_answer == True:
                    job_balls['inson'] += 1
                else:
                    continue

            job_key = ''  # bali eng yuqori  bo'lgan kasb
            max_value = max(job_balls.values())
            for k, v in job_balls.items():
                if v == max_value:
                    job_key = k
        except:
            return Response({'error':"Eng yuqori 'True' qiymatiga ega kasbni aniqlashda xatolik !"})


        """ Yangi obyekt yaratish  """
        user.permission_to_test = True
        user.save()

        try:
            new_result = PSTResult.objects.create(
                user = user,
                subcategory = subcategory,
                job = job_key,
            )
            serializer = PSTResultSerializer(new_result)
            return Response(serializer.data)
        except:
            return Response({'error':"Malumotlarni saqlashda xatolik yuzaga keldi !!!"})