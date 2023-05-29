from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PSTSub_CategoryViewset, PSTQuestionViewset, PSTAnswerViewset, PSTResultViewset

router = DefaultRouter()
router.register(r'subcategory', PSTSub_CategoryViewset)
router.register(r'question', PSTQuestionViewset)
router.register(r'answer', PSTAnswerViewset)
router.register(r'result', PSTResultViewset)

urlpatterns = [
    path('', include(router.urls)),
]
