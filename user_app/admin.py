from django.contrib import admin
from .models import Student

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'avatar_tag', 'age', 'sex','state',\
                    'phone_number','father_number','status','created_at')
    list_filter = ('age','sex','state','status','created_at')
    search_fields = ('first_name','last_name','username','phone_number','father_number')




    