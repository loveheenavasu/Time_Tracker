
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from PIL import ImageGrab
from datetime import date
import time
import datetime
import os
from random import randrange
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent


# def screenshort(user_email):
#     pass
#     # generate_token("roman1@gmail.com","123456789" )
#     screenshort_root_dir = 'screenshots'
#     current_dt = date.today()
#     path_to_save_screenshot=(f"{BASE_DIR}\\{screenshort_root_dir}\\{current_dt.year}\\{current_dt.month}\\{current_dt.day}\\{user_email}")
#     try:
#         if not os.path.exists(path_to_save_screenshot):
#             os.makedirs(path_to_save_screenshot)
#     except OSError:
#         pass
#     while True:
#             random_time = randrange(10)
#             time.sleep(random_time)
#             snapshot = ImageGrab.grab()
#             file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
#             snapshot.save(os.path.join(path_to_save_screenshot, file_name))


class UserIdStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_active']
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password','username','email', 'contact')
        # exclude = ['password']
    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        user.set_username(attrs['username'])
        user.set_contact(attrs['contact'])
        return user
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    USERNAME_FIELD = 'email'
    def validate(self, attrs):
        password = attrs.get('password')
        user_obj = User.objects.filter(email=attrs.get('email'))
        if user_obj:
            credentials = {
                'email': user_obj[0].email,
                'password': password
            }
            user_email = User.objects.get(email=user_obj[0].email)
            print("user_email", user_email)
            print("user_email", user_email.email)
            # print(user.check_password(password))
            # user = authenticate(request=self.context['request'], email=user_obj[0].email, password=password)
            if user_email.check_password(password):
                refresh = self.get_token(user_email)
                data = {
                        'success': True,
                        'status': 200,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'email': user_email.email,
                        'message': 'Login successfully',
                        'META': {}
                    }
                return(data)
            return {"message": 'please enter valid email and password', 'status': 400}
         
        else:
            return {"message": 'please enter valid email and password', 'status': 400}
            
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user)
        token['email'] = user.email
        return token
        

    
    




class UserDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', ]
