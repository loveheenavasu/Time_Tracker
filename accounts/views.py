from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import status
from .models import User
from .forms import UserForm
from Time_Tracker.permissions import IsAdmin, IsProjectManager
from .serializers import UserSerializer, MyTokenObtainPairSerializer
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def custom_response(status, data=[], message=""):
    """return custom response for all the APIs"""
    if status == 404:
        if not message:
            message = "do not have permission"
        context = {
            "status": status,
            "message": message,
            "data": data
        }
    elif status == 400 or status == 202:
        error_list = list()
        if isinstance(data, str):
            message = data
            context = {
                "status": status,
                "message": message,
                "data": []
            }
        else:
            for i, j in data.items():
                j = "".join(j)
                message = f"{i}: {j}"
                error_list.append(message)

            context = {
                "status": status,
                "message": ", ".join(error_list),
                "data": []
            }
    elif status == 409:
        context = {
            "status": status,
            "message": "Already exists",
            "data": []
        }
    else:
        context = {
            "status": status,
            "message": message,
            "data": data
        }
    return context


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class CustomViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [AllowAny, ]

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""

        if self.action == 'list':
            permission_classes = [IsAdmin, IsProjectManager]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request):
        data, context = [], {}
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, "Created Successfully.")
            else:
                context = custom_response(status.HTTP_400_BAD_REQUEST, serializer.errors, "Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False)

    def partial_update(self, request, pk):

        data, context = [], {}
        try:
            try:
                queryset = User.objects.all()
                user = get_object_or_404(queryset, pk=pk)
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # user_obj = User.objects.get(id=serializer.data["id"])
                    # serializer = User(user_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, "Updated Successfully.")
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, "Unsuccessful.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        UserIsAdmin = request.user.is_admin
        print(UserIsAdmin)
        if UserIsAdmin == True:
            try:
                try:
                    get_user = User.objects.get(id=pk)
                    serializer = UserSerializer(get_user)
                    context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
                except Exception as error:
                    context = custom_response(status.HTTP_404_NOT_FOUND)
            except Exception as error:
                context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
            return JsonResponse(context, status=context.get("status"), safe=False)
        else:
            try:
                try:
                    user_id = request.user.id
                    # print(user_id)
                    get_user = User.objects.get(id=pk)
                    userget = get_user.id
                    # print(get_user.id)
                    if userget == user_id:
                        serializer = UserSerializer(get_user)
                        context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
                    else:
                        context = custom_response(status.HTTP_200_OK, serializer.data,
                                                  "Not have permessions for this king of access")
                except Exception as error:
                    context = custom_response(status.HTTP_404_NOT_FOUND)
            except Exception as error:
                context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
            return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                user = self.get_object()
                user.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get('status'), safe=False)

def demo(request):
    token = generate_token()
    hed = {"Authorization": f"Bearer {token.get('access')}"}
    print("request", request, request.method)
    response = requests.get('http://127.0.0.1:8000/task/9/').json()
    return render(request, 'demo.html')

@csrf_exempt
def login_session(request):
    if request.GET:
        email = request.GET['email']
        password = request.GET['password']
        print(email, password)
        user = authenticate(request, email=email, password=password)
        user_id = request.user.id
        print('---------------------------------->',user_id)
        data = User.objects.filter(id=user_id)
        if user is not None:
            login(request, user)
            # Redirect to a success
            for i in data:
                project_manager = i.is_projectmanager
                team_leader = i.is_TeamLeader
                admin = i.is_admin
                superuser = i.is_superuser
                print("------------------------------------", project_manager, team_leader)
                admin = i.is_admin
                superuser = i.is_superuser
                if admin or superuser:
                    return redirect('admin_templates/index')
                else:
                    print("Something else went wrong")
                    return redirect('/index/')
        else:
            messages.success(request, 'Please enter valid Details!')
    return render(request, 'login.html')



def generate_token():
    """generate token to access the API's"""
    endpoint = '/api/token'

    api = "http://127.0.0.1:8000/login/"
    data = {
        "email": 'admin@gmail.com',
        "password": '123456789'
    }
    req = requests.post(api, json=data)
    token = req.json()
    return token

def home_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_session')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})



    # token = generate_token()
    # hed = {"Authorization": f"Bearer {token.get('access')}"}
    # print("request", request, request.method)
    # data = None
    # department_users = Department.objects.all()
    # if request.GET:
    #     username = request.GET['username']
    #     first_name = request.GET['first_name']
    #     last_name = request.GET['last_name']
    #     email = request.GET['email']
    #     password = request.GET['password']
    #     contact = request.GET['contact']
    
    #     userregister = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password, contact=contact)
    #     userregister.save()
    #     return redirect('/loginpage')
    #     return JsonResponse(data)
    # else:
    #     print("invalid")
    # return render(request, 'register.html')





def index(request):
    return render(request, 'index.html')


def user_profile(request, id):
    user_data = User.objects.get(id=id)
    context = {'user_data': user_data}
    return render(request, 'user_profile.html', context)

def admin_register(request):
    if request.method == "POST":
        form = USerForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = USerForm()
    return render(request, 'Admin_templates/departments_.html', {'form': form})

def all_users(request):
    all_users = User.objects.all()
    context = {'all_users': all_users}
    return render(request, 'Admin_templates/all_users.html', context)

def delete_user(request, id):
        try:
            user_data = User.objects.get(id=id)
        except User.DoesNotExist:
            messages.success(request, 'User Does not exist!')
        user_data.delete()
        messages.success(request, 'User deleted successfully')
        return render(request, 'Admin_templates/department_details.html')



def index2(request):
    data = User.objects.all()
    context = {'data': data}
    return render(request, 'Admin_templates/index2.html')