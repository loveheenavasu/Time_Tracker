from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404,HttpResponseRedirect
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, authenticate
from main_app.forms import ProjectsForm
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import status
from .forms import UserForm, UserUpdateForm
from Time_Tracker.permissions import IsAdmin, IsProjectManager
from .serializers import UserSerializer, MyTokenObtainPairSerializer, UserIdStatusSerializer
import requests
import xlwt
from main_app.models import Projects
from django.views.decorators.csrf import csrf_exempt
from .models import *
from pathlib import Path
from django.contrib.auth import logout
from main_app.models import Task
from main_app.forms import UpdateProjectForm
# import xlwt
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
    user_data = User.objects.get(id=id)
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



# def IdStatus(request):
#     all_users = User.objects.all()
#     if request.method == "POST":
#         print('---------------DATA', request.POST)
#         serializer = UserIdStatusSerializer(data=request.POST)
#         if serializer.is_valid():
#             serializer.save()
#             print(serializer.data, 'SERIALIZER DATA--------------------------')
#
#             return redirect('login_session')
#     else:
#         form = UserForm()
#     return render(request, 'Admin_templates/all_users.html', {'all_users': all_users, 'form': form})

def all_users(request):
    all_users = User.objects.all()
    users = UserSerializer(all_users, many=True)
    user_status = users.data
    users_obj = users.__dict__
    if request.method == "POST":
        form = UserForm(request.POST)
        # print('---------------DATA', request.POST)
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data, 'SERIALIZER DATA--------------------------')
            return redirect('all_users')
    else:
        form = UserForm()
    return render(request, 'Admin_templates/all_users.html', {'all_users': all_users, 'form': form, "users_obj": users_obj})


def projects_details(request, id):
    projectsdata = Projects.objects.filter(id=id)
    task_detail = Task.objects.filter(project__id=id)
    user_image =[]
    for i in task_detail:
        data = i.assigned_to.all()
        print(data, "+++++++++++++++++++++++++++++>")
        for j in data:
            data2 = j.image
            print(data2, "==================================================>")
            user_image.append(j.image)

    print("------------------------------------------------>",task_detail)
    context = {'projectsdata': projectsdata, 'task_detail':task_detail,'user_image':user_image}
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

    return redirect('all_users')

def update_project(request, id):
    context = {}
    obj = Projects.objects.get(id=id)
    print(obj.id, "------------------------>")
    # form = UpdateProjectForm(request.POST or None, instance=obj)
    if request.method == "POST":
        form_data = request.POST
        print("Form DAta : ", form_data)
        project_name = form_data['project-name']
        project_category = form_data['projectt-category']
        project_department = Departments.objects.get(name=form_data['project-department'])
        project_priority = form_data['priority-list']
        project_status = form_data['status-list']
        project_desc = form_data['project-description']
        project_created = form_data['project-description']
        project_deadline = form_data['project-description']

        project_obj = Projects.objects.get(id=id)
        project_obj.project_name=project_name
        project_obj.project_category=project_category
        project_obj.description=project_desc
        project_obj.status=project_status
        project_obj.priority=project_priority
        project_obj.department=project_department ####
        project_obj.save()
        return redirect('project_data')

        
        # update_form = UpdateProjectForm(request.POST, request.FILES, instance=obj)
        # update_form.save()
        # if update_form.is_valid():
        #     update_form.save()
        #     return HttpResponseRedirect("/" + id)
        pass
    else:
        # update_form = UpdateProjectForm(instance=obj)
        pass
    context = {'obj':  obj, 'test': 'test'}
    return render(request, "projects.html", context)

def delete_project(request, id):
    try:
        user_data = Projects.objects.get(id=id)
        user_data.delete()
    except User.DoesNotExist:
        messages.success(request, 'Project Does not exist!')
    messages.success(request, 'Project deleted successfully')
    return redirect('project_data')


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
    columns = ['is_ongoing', 'description', 'department', 'is_completed', 'created_at', 'updated_at', 'received_at', 'completed_at', 'deadline']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, str(columns[col_num]), font_style)
    font_style = xlwt.XFStyle()
    rows = Projects.objects.all().values_list( 'is_ongoing', 'description', 'department', 'is_completed', 'created_at', 'updated_at', 'received_at', 'completed_at', 'deadline')
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


def user_deactivate(request, user_id):
    print("user ID for  deactivate", user_id)
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    print(user_id)
    messages.error(request, "User account has been successfully deactivated!")
    return redirect('all_users')

def user_activate(request, user_id):
    print("user ID for activate ", user_id)
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "User account has been successfully activated!")
    return redirect('all_users')


def profilesetting(request, id):
    user_id = User.objects.get(id=id)
    print(user_id,'-------------------->')
    if request.method == 'POST':
        print("Request data : ", request.POST)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profilesetting') # Redirect back to profile page

    else:
        print('----------------------------->')
        u_form = UserUpdateForm(instance=request.user)

    context = {'user_id':user_id, 'u_form':u_form}
    return render(request, 'profilesetting.html', context)


