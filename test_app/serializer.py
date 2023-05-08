from rest_framework import serializers

from .models import Sub_Category, Category, Question, Answer
from user_app.models import Result

""" Serializers for API """
class AnswerAPISerializer(serializers.ModelSerializer):
    question_slug = serializers.CharField(source='question_id.slug')

    class Meta:
        model = Answer
        fields = ('id', 'answer', 'slug', 'question_slug')


class QuestionAPISerializer(serializers.ModelSerializer):
    sub_category_slug = serializers.CharField(source='category_id.slug')
    answer = AnswerAPISerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question', 'slug',
                  'sub_category_slug', 'photo', 'answer')


class Sub_CategoryAPISerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source='parent.slug')
    category_id = serializers.CharField(source='parent.id')
    question = QuestionAPISerializer(many=True, read_only=True)

    class Meta:
        model = Sub_Category
        fields = ('id', 'name', 'slug', 'category_slug', 'category_id',
                  'description', 'number_of_questions', 'number_of_answer', 'question')


class CategoryAPISerializer(serializers.ModelSerializer):
    category = Sub_CategoryAPISerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'category')


class ResultAPISerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='subcategory.name')

    class Meta:
        model = Result
        fields = ('id', 'subcategory_name',
                  'ball', 'try_count', 'created_at', 'created_at')


""" ----------------------------  CRUID Serialazers ------------------------------------ """

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('__all__')

""" ----------------------------  CRUD Serialazers ------------------------------------ """




