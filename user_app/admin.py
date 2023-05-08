from django.contrib import admin
from .models import Student, Result
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id', 'email', 'username', 'avatar_tag', 'age', 'gender','state',\
                    'phone_number','status','created_at')
    list_filter = ('age','gender','state','status','created_at')
    search_fields = ('first_name','last_name','username','phone_number')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'yoshi', 'sinfi', 'subcategory', 'ball', 'try_count', 'created_at')
    list_filter = ('user__age', 'user__gender', 'user__state', 'subcategory', ('created_at', DateTimeRangeFilter),)
    search_fields = ('full_name',)

    @admin.display(ordering='created_at', description="O'quvchi ismi")
    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    @admin.display(ordering='created_at', description="Yoshi")
    def yoshi(self, obj):
        return obj.user.age
    
    @admin.display(ordering='created_at', description="Sinfi")
    def sinfi(self, obj):
        return f"{obj.user.state}-sinf"


    