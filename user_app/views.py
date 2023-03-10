from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Student
from .serializers import StudentSerializer

from pprint import pprint

# Create your views here.

""" --------------------  CRUD Viewsets  -------------------- """
class RegisterView():
    pass



class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class  = StudentSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        student_data = request.data
        if Student.objects.filter(username=student_data['username']):
            return Response({'error': "Bunday 'username' avval yaratilgan !"})
        try:
            new_student = Student.objects.create(
                password = student_data['password'],
                username = student_data['username'],
                first_name = student_data['first_name'],
                last_name= student_data['last_name'],
                age = student_data['age'],
                sex = student_data['sex'],
                state = student_data['state'],
                photo = student_data['photo'],
                email = student_data['email'],
                phone_number= student_data['phone_number'],
                father_number= student_data['father_number'],
            )
            new_student.save()
            serializer = StudentSerializer(new_student)
            return Response(serializer.data)
        except Exception as e:
    	    return Response({'errors':"Ma'lumot to'liq emas !!!"})
        
    def update(self, request, *args, **kwargs):
        student_data = self.get_object()
        data = request.data
        
        try:
             if Student.objects.filter(username=data['username']) and student_data.username != data['username']:
                return Response({'error': "Bunday 'username' avval yaratilgan ! Iltimos boshqa 'username' tanlang."})
        except:
            pass

        try:
            student_data.password = data['password'] if 'password' in data else student_data.password
            student_data.username = data['username'] if 'username' in data else student_data.username
            student_data.first_name = data['first_name'] if 'first_name' in data else student_data.first_name
            student_data.last_name = data['last_name'] if 'last_name' in data else student_data.last_name
            
            student_data.age = data['age'] if 'age' in data else student_data.age
            student_data.sex = data['sex'] if 'sex' in data else student_data.sex
            student_data.state = data['state'] if 'state' in data else student_data.state
            student_data.photo = data['photo'] if 'photo' in data else student_data.photo
            student_data.email = data['email'] if 'email' in data else student_data.email
            student_data.phone_number = data['phone_number'] if 'phone_number' in data else student_data.phone_number
            student_data.father_number = data['father_number'] if 'father_number' in data else student_data.father_number
            
            student_data.save()
            serializer = StudentSerializer(student_data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})



""" --------------------  API Viewsets  -------------------- """









