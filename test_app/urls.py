from django.urls import path, include
from rest_framework import routers

from .views import Sub_CategoryViewset, CategoryViewset, QuestionViewset, AnswerViewset, ResultViewset

router = routers.DefaultRouter()

router.register(r'subcategory', Sub_CategoryViewset, basename='subcategory')
router.register(r'category', CategoryViewset, basename='category')
router.register(r'question', QuestionViewset, basename='question')
router.register(r'answer', AnswerViewset, basename='answer')
router.register(r'result', ResultViewset, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]
