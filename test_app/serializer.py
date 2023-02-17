from .models import Sub_Category, Category, Question, Answer
from rest_framework import serializers


""" Serializers for API """

class AnswerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','answer','slug','photo')

class QuestionAPISerializer(serializers.ModelSerializer):
    answer = AnswerAPISerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ('id','question','slug','photo','answer')

class CategoryAPISerializer(serializers.ModelSerializer):
    question = QuestionAPISerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('id','name','slug','description','number_of_questions','time_duration','question')

class Sub_CategoryAPISerializer(serializers.ModelSerializer):
    category = CategoryAPISerializer(many=True, read_only=True)
    class Meta:
        model = Sub_Category
        fields = ('id','name','slug','description','category')












