from django.contrib import admin

from .models import Sub_Category, Category, Question, Answer

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin. ModelAdmin):
    list_display = ('name','id','description','status','created_at')
    list_filter = ('status','created_at')

@admin.register(Sub_Category)
class Sub_CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'parent','number_of_questions','status','created_at')
    list_filter = ('parent', 'status', 'created_at')
    search_fields = ('name',)

""" Question modeli uchun Answer modelining Tabline classi """
class AnswerInlineAdmin(admin.TabularInline):
    model = Answer
    fields = ('question_id','answer','true_answer','status')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question','id','category_id', 'status', 'created_at')
    list_filter = ('category_id','status', 'created_at')
    search_fields = ('question',)
    inlines = [AnswerInlineAdmin,]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer','id','true_answer','status','created_at')
    list_filter = ('true_answer','status','created_at')
    search_fields = ('answer',)

