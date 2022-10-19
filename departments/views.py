from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Departments
from .serializers import DepartmentsSerializer, DepartmentsSerializerEdit
from accounts.views import custom_response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import User
from main_app.models import Projects, Task
from main_app.forms import ProjectsForm
from accounts.forms import UserForm
from accounts.serializers import UserSerializer
from main_app.views import project_data
from .forms import DepartmentsForm 
# import xlwt
from django.http import HttpResponse

# Create your views here.


class DeparmentsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DepartmentsSerializer
    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = Departments.objects.all()
            serializer = DepartmentsSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))


    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = DepartmentsSerializerEdit(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                id = serializer.data.get('id')
                queryset = Departments.objects.get(id=id)
                serializer = DepartmentsSerializer(queryset)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, "Created Successfully.")
            else:
                context = custom_response(status.HTTP_400_BAD_REQUEST, serializer.errors, "Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False)


    def partial_update(self, request, pk):

        data = []
        try:
            try:
                queryset = Departments.objects.all()
                user = get_object_or_404(queryset, pk=pk)
                serializer = DepartmentsSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    user_obj = Departments.objects.get(id=serializer.data["id"])
                    serializer = Departments(user_obj)
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
        try:
            try:
                get_user = Departments.objects.get(id=pk)
                serializer = DepartmentsSerializer(get_user)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
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


def departments(request):
    data = Departments.objects.all()
    department_name = []
    department_count = {}
    for obj in data:
        department_name.append(obj.name)
    for department in department_name:
        department_count[department] = User.objects.filter(department__name=department).count()
    if request.method == "POST":
        create_form = DepartmentsForm(request.POST)
        if create_form.is_valid():
            create_form.save()
        return redirect('admin_departments')
    else:
        department_form = DepartmentsForm()
    context = {'data': data, 'department_count': department_count, 'department_form':department_form}
    return render(request, 'Admin_templates/department.html', context)


def department_info(request, name):
    users = User.objects.filter(department__name=name)
    projects = Projects.objects.filter(department__name=name)
    # started_project = Projects.objects.filter(department__name=name)
    # approve_project = Projects.objects.filter(is_approval=True)
    # completed_projects = Projects.objects.filter(is_completed=True)
    all_users = User.objects.all()
    if request.method == "POST":
        print('---------------DATA', request.POST)
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data, 'SERIALIZER DATA--------------------------')
    else:
        form = UserForm()
    if request.method == "POST":
        create_form = ProjectsForm(request.POST)
        if create_form.is_valid():
            create_form.save()
        return redirect('project_data')

    else:
        create_form = ProjectsForm()
    context = {'users': users, 'projects': projects,'form':form, 'create_form':create_form}
    return render(request, 'Admin_templates/department_details.html', context)

def update_project_department(request, id):
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
    else:
        # update_form = UpdateProjectForm(instance=obj)
        pass
    context = {'obj':  obj}
    return render(request, "Admin/department_details", context)


def screenshorts(request):
    return render(request, 'screenshorts.html')

def delete_department(request, id):
    try:
        user_data = Departments.objects.get(id=id)
        user_data.delete()
    except User.DoesNotExist:
        messages.success(request, 'Department Does not exist!')
    messages.success(request, 'Department deleted successfully')
    return redirect('admin_departments')

