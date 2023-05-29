from django.contrib import admin
from .models import PSTSub_Category, PSTQuestion, PSTAnswer
from user_app.models import Result

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter, NumericRangeFilter

# Register your models here.

@admin.register(PSTSub_Category)
class Sub_CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id','number_of_questions','status','created_at')
    list_filter = ( 'status', 'created_at')
    search_fields = ('name',)

""" Question modeli uchun Answer modelining Tabline classi """
class AnswerInlineAdmin(admin.TabularInline):
    model = PSTAnswer
    fields = ('question_id','answer','true_answer','status')

@admin.register(PSTQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question','id','category_id','job_type', 'status', 'created_at')
    list_filter = ('category_id','job_type','status', 'created_at')
    search_fields = ('question',)
    inlines = [AnswerInlineAdmin,]


@admin.register(PSTAnswer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer','id','true_answer','status','created_at')
    list_filter = ('true_answer','status','created_at')
    search_fields = ('answer',)


# @admin.register(Result)
# class ResultAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'yoshi', 'sinfi', 'category', 'subcategory', 'ball', 'tashxis', 'created_at')
#     list_filter = ('user__age', 'user__sex', 'user__state', 'category', 'subcategory', ('created_at', DateTimeRangeFilter),)
#     search_fields = ('full_name',)


#     @admin.display(ordering='created_at', description="O'quvchi ismi")
#     def full_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}"
    
#     @admin.display(ordering='created_at', description="Yoshi")
#     def yoshi(self, obj):
#         return obj.user.age
    
#     @admin.display(ordering='created_at', description="Sinfi")
#     def sinfi(self, obj):
#         return f"{obj.user.state}-sinf"