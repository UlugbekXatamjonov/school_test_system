from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import Student
from .utils import Util

from test_app.serializer import ResultAPISerializer
from psix_test.serializers import PSTResultSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
  # Ro'yhatdan o'tish vaqtida parolni tekshirish uchun password2 maydoni yaratib olindi
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = Student
    fields = (
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
            "age",
            "gender",
            "state",
            "email",
            "phone_number",
        )
    extra_kwargs={
      'password':{'write_only':True}
    }

  # parollarni validatsiyadan o'tkazish va bir biriga mosligini tekshirib chiqamiz
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Kiritilgan parollar birxil emas !!!")
    return attrs

  def create(self, validate_data):
    return Student.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
  # login uchun 'username' maydonini yaratib olish kerak
  username = serializers.CharField(max_length=255)
  class Meta:
    model = Student
    fields = ['username', 'password']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class UserProfileSerializer(serializers.ModelSerializer): 
  test_results = ResultAPISerializer(many=True, read_only=True)
  psttest_results = PSTResultSerializer(many=True, read_only=True)
  class Meta:
    model = Student
    fields = (
            "id",
            "username",
            "slug",
            "first_name",
            "last_name",
            "age",
            "gender",
            "state",
            "photo",
            "email",
            "phone_number",
            "step_by_subcategory",
            'test_results',   
            'psttest_results',        
        )


class UserChangePasswordSerializer(serializers.Serializer):
  current_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

  class Meta:
    fields = ['current_password', 'password', 'password2']

  def validate_current_password(self, value):
    user = self.context.get('user')
    if not user.check_password(value):
      raise serializers.ValidationError("Joriy parol noto'g'ri kiritildi !")
    return value

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("parol o'zgartirilmadi!")
    user = self.context.get('user')
    user.set_password(password)
    user.save()
    return attrs

# class UserChangePasswordSerializer(serializers.Serializer):
#   password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   class Meta:
#     fields = ['password', 'password2']

#   def validate(self, attrs):
#     password = attrs.get('password')
#     password2 = attrs.get('password2')
#     user = self.context.get('user')
#     if password != password2:
#       raise serializers.ValidationError("Password and Confirm Password doesn't match")
#     user.set_password(password)
#     user.save()
#     return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        # print(f"attrs ---- {email}")
        
        if Student.objects.filter(email=email).exists():
            user = Student.objects.get(email = email)
            # print(f"user ---- {user.email}")
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print("--------------------------------------------------------------------------------")
            # print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            # print('Password Reset Link', link)
            # print("-------------------------------------------------------------------------------")
            # Send EMail
            body = 'Parolingizni tiklash uchun quyidagi havolani bosing '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("Siz ro'yhatdan o'tmagansiz")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = Student.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
  


