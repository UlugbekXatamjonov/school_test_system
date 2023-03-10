from .models import Sub_Category, Category, Question, Answer, Result
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

class Sub_CategoryAPISerializer(serializers.ModelSerializer):
    question = QuestionAPISerializer(many=True, read_only=True)
    class Meta:
        model = Sub_Category
        fields = ('id','name','slug','description','number_of_questions','time_duration','question')

class CategoryAPISerializer(serializers.ModelSerializer):
    category = Sub_CategoryAPISerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('id','name','slug','description','category')

class ResultAPISerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    subcategory_name = serializers.CharField(source='subcategory.name')
    
    class Meta:
        model = Result
        fields = ('id', 'category_name', 'subcategory_name', 'ball', 'tashxis', 'created_at', 'created_at')



""" ----------------------------  CRUID Serialazers ------------------------------------ """
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('__all__')


        
""" ----------------------------  CRUD Serialazers ------------------------------------ """










