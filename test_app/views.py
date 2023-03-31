from django.shortcuts import render
from pprint import pprint
import json

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Sub_Category, Category, Question, Answer
from .serializer import Sub_CategoryAPISerializer, CategoryAPISerializer, QuestionAPISerializer, AnswerAPISerializer, ResultSerializer

from user_app.models import Result, Student

# Viewset for API serializers

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status="active")
    serializer_class = CategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class Sub_CategoryViewset(viewsets.ModelViewSet):
    queryset = Sub_Category.objects.filter(status="active")
    serializer_class = Sub_CategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.filter(status="active")
    serializer_class = QuestionAPISerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class AnswerViewset(viewsets.ModelViewSet):
    queryset = Answer.objects.filter(status="active")
    serializer_class = AnswerAPISerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]



""" ------------------------ CRUD Viewset -------------------- """

class ResultViewset(viewsets.ModelViewSet):
    """
    O'quvchi test yechganda, yechilgan testni balini berilgan bir nechta parametrlar
    bo'yicha hisoblab chiqadi.
    To'plangan balga qarab belgilangan 'teashxis' yani hulosa olinadi
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [AllowAny] 

    """ CRUD operations """
    def create(self, request, *args, **kwargs):
        result_data = request.data

        # pprint(result_data)

        # request_category = int(result_data['category'])
        # pprint(request_category)
        # print(type(request_category))    

        # request_subcategory = int(result_data['subcategory'])
        # pprint(request_subcategory)
        # pprint(type(request_subcategory))

        # request_ball = int(result_data['ball'])
        # pprint(request_ball)
        # pprint(type(request_ball))

        # request_tashxis = result_data['tashxis']
        # pprint(request_tashxis)
        # pprint(type(request_tashxis))

        # request_tests = result_data['test_api']
        # pprint(request_tests)
        # pprint(type(request_tests))









        user =  False        
        if 'user' in result_data:
            try:
                if int(result_data['user']) == int(request.user.id):
                    user = Student.objects.get(pk=str(result_data['user']))
                else:
                    return Response({"error":"Ro'yhatdan o'tgan user 'id'si, test yechgan user 'id'siga to'g'ri kelmadi!!!"})

            except Exception as e:
                return Response({"error":"Bunday user mavjud emas!!!"})
            
        category =  False        
        if 'category' in result_data:
            try:
                category = Category.objects.get(pk=str(result_data['category']))
            except Exception as e:
                return Response({"error":"Bunday kategoriya mavjud emas!!!"})
            
        subcategory =  False        
        if 'subcategory' in result_data:
            try:
                subcategory = Sub_Category.objects.get(pk=str(result_data['subcategory']))
            except Exception as e:
                return Response({"error":"Bunday kichik kategoriya mavjud emas!!!"})
                
        try: 
            new_result = Result.objects.create(
                user = user,
                category = category,
                subcategory = subcategory,
                ball = result_data['ball'],
                tashxis = result_data['tashxis'],
                test_api = {'api':"API"} #result_data['test_api'],
                )
            new_result.save()
            serializer = ResultSerializer(new_result)
            return Response(serializer.data)
        except Exception as e:
    	    return Response({'errors':"Ma'lumot to'liq emas!!!"})






