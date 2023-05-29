from rest_framework.serializers import ModelSerializer
from .models import PSTSub_Category, PSTQuestion, PSTAnswer
from user_app.models import PSTResult

class PSTAnswerSerializer(ModelSerializer):
    class Meta:
        model = PSTAnswer
        fields = ('id', 'slug', 'answer')

class PSTQuestionSerializer(ModelSerializer):
    answer = PSTAnswerSerializer(many=True, read_only=True)
    class Meta:
        model = PSTQuestion
        fields = ('id', 'question', 'slug', 'answer')

class PSTSub_CategorySerializer(ModelSerializer):
    pstquestion = PSTQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = PSTSub_Category
        fields = ('id', 'name', 'slug', 'description', 'number_of_questions', 'pstquestion')

class PSTResultSerializer(ModelSerializer):
    class Meta:
        model = PSTResult
        fields = ('__all__')


