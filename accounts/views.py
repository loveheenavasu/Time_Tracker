from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .forms import UserForm
from Time_Tracker.permissions import IsAdmin, IsProjectManager
from .serializers import UserSerializer, MyTokenObtainPairSerializer
import requests
from main_app.models import Projects
from django.views.decorators.csrf import csrf_exempt
from .models import *
from pathlib import Path
from django.contrib.auth import logout
from main_app.models import Task
import xlwt
from django.http import HttpResponse
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
        print('---------------------------------->', user_id)
        data = User.objects.filter(id=user_id)
        print(data)
        if user is not None:
            login(request, user)
            # Redirect to a success
            for i in data:
                project_manager = i.is_projectmanager
                team_leader = i.is_TeamLeader
                employee = i.is_employee
                staff = i.is_staff
                print("------------------------------------", project_manager, team_leader)
                admin = i.is_admin
                superuser = i.is_superuser
                print(admin, superuser,'----------------------------------')
                if admin or superuser:
                    return redirect('all_users/')
                else:
                    return redirect('/project_data')
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









def index(request):
    return render(request, 'index.html')


def user_profile(request, id):
    user_data = User.objects.get(id = id)
    user = request.user.id
    try:
        task_details = Task.objects.get(assigned_to=user)
        project_detail_user = Task.objects.filter(project__id=id)
        print("------------------->", task_details.description)
        tast_data = task_details.assigned_to.all()
        print("------------------------------------------------------------->", tast_data)
        context = {'user_data': user_data, 'task_details': task_details}
    except:
        pass
        context = {'user_data': user_data}
    return render(request, 'user_profile.html', context)


def all_users(request):
    all_users = User.objects.all()
    if request.method == "POST":
        print('---------------DATA', request.POST)
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data, 'SERIALIZER DATA--------------------------')

            # form = UserForm(request.POST)
            # print('----------------FORM', form)
            # if form.is_valid():
            #     form.save()
            return redirect('login_session')
    else:
        form = UserForm()
    return render(request, 'Admin_templates/all_users.html', {'all_users': all_users, 'form': form})


def projects_details(request, id):
    projectsdata = Projects.objects.filter(id=id)
    context = {'projectsdata': projectsdata}
    return render(request, 'Admin_templates/project_detail.html', context)

def delete_user(request, id):
    try:
        u = User.objects.get(id=id)
        u.delete()
        messages.success(request, "The user is deleted")

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")
        return render(request, 'Admin_templates/all_users.html')

    except Exception as e:
        return render(request, 'front.html', {'err': e.message})

    return render(request, 'Admin_templates/all_users.html')


def delete_project(request, id):
    try:
        user_data = Projects.objects.get(id=id)
    except User.DoesNotExist:
        messages.success(request, 'Project Does not exist!')
    user_data.delete()
    messages.success(request, 'Project deleted successfully')
    return render(request, 'projects.html')


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['fullname', 'email', 'contact', 'department', 'designation', 'is_admin', 'is_active', 'is_projectmanager','is_employee', 'is_TeamLeader', 'date_joined', 'is_staff' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, str(columns[col_num]), font_style)
    font_style = xlwt.XFStyle()
    rows = User.objects.all().values_list('fullname', 'email', 'contact', 'department', 'designation', 'is_admin', 'is_active', 'is_projectmanager','is_employee', 'is_TeamLeader', 'date_joined', 'is_staff')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response



def export_projects_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Projects.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Projects Data')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['project', 'is_ongoing', 'description', 'department', 'is_completed', 'created_at', 'updated_at', 'received_at', 'completed_at', 'deadline']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, str(columns[col_num]), font_style)
    font_style = xlwt.XFStyle()
    rows = Projects.objects.all().values_list('project', 'is_ongoing', 'description', 'department', 'is_completed', 'created_at', 'updated_at', 'received_at', 'completed_at', 'deadline')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response

def forgetpassword(request):
    return render(request, 'forgetpassword.html')


def logout_view(request):
    logout(request)
    return redirect('login_session')
