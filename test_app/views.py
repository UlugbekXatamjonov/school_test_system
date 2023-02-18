from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 
from rest_framework import viewsets

from .models import Sub_Category, Category, Question, Answer
from .serializer import Sub_CategoryAPISerializer, CategoryAPISerializer, QuestionAPISerializer, AnswerAPISerializer


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









