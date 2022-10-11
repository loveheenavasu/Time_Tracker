from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from Time_Tracker.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from .models import Task, Projects, Remarks
from .serializers import TaskSerializer, ProjectsSerializer, RemarksSerializer, RemarksSerializerGET, TaskSerializerEdit
from accounts.views import custom_response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from accounts.views import generate_token
from django.contrib import messages
import requests
from accounts.models import User
from datetime import date

from .forms import ProjectsForm, TaskForm


# Create your views here.


class TaskViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = Task.objects.all()
            serializer = TaskSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))


    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:

            serializer = TaskSerializerEdit(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                id = serializer.data.get('id')
                queryset = Task.objects.get(id=id)
                serializer = TaskSerializer(queryset)
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
                task_id = request.data.get(id)
                queryset = Task.objects.all()
                user = get_object_or_404(queryset, pk=task_id)
                serializer = TaskSerializer(user, data=request.data.get('assigned_to'), partial=True)
                if serializer.is_valid():
                    serializer.save()
                    context = custom_response(status.HTTP_200_OK, serializer.data, "Updated Successfully.")
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, "Unsuccessful.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get("sta3tus"))


    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_user = Task.objects.get(id=pk)
                serializer = TaskSerializer(get_user)
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


class ProjectsViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = Projects.objects.all()
            serializer = ProjectsSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))


    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            data = request.data
            serializer = ProjectsSerializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
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
                queryset = Projects.objects.all()
                user = get_object_or_404(queryset, pk=pk)
                serializer = ProjectsSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # user_obj = Projects.objects.get(id=serializer.data["id"])
                    # serializer = Projects(user_obj)
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
                get_user = Projects.objects.get(id=pk)
                serializer =ProjectsSerializer(get_user)
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


class RemarksViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Remarks.objects.all()
    # serializer_class = RemarksSerializer
    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = Remarks.objects.all()
            serializer = RemarksSerializerGET(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = RemarksSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                id = serializer.data.get('id')
                queryset = Remarks.objects.get(id=id)
                serializer = RemarksSerializerGET(queryset)
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
                queryset = Remarks.objects.all()
                user = get_object_or_404(queryset, pk=pk)
                serializer = RemarksSerializerGET(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # user_obj = Remarks.objects.get(id=serializer.data["id"])
                    # serializer = Remarks(user_obj)
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
                get_user = Remarks.objects.get(id=pk)
                serializer =RemarksSerializerGET(get_user)
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



def project(request):
    if request.method == "POST":
        form = ProjectsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_session')
    else:
        form = ProjectsForm()
    return render(request, 'projects.html', {'form': form})



def task(request):
    in_progress_task = Task.objects.filter(in_progress=True)
    approve_project = Task.objects.filter(in_review=True)
    completed_projects = Task.objects.filter(is_completed=True)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_session')
    else:
        form = TaskForm()
    context = {'in_progress_task': in_progress_task, 'approve_project': approve_project, 'completed_projects':completed_projects, 'form':form}
    return render(request, 'task.html',context)




def project_data(request):
    data_project = Projects.objects.all()
    started_project = Projects.objects.filter(is_started=True)
    approve_project = Projects.objects.filter(is_approval=True)
    completed_projects = Projects.objects.filter(is_completed=True)
    if request.method == "POST":
        form = ProjectsForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form1 = ProjectsForm()
    context ={'data_project': data_project, 'started_project':started_project,'approve_project':approve_project, 'completed_projects': completed_projects, 'form': form1}
    return render(request, 'projects.html', context)

def task_detail(request, id):
    task_data = Task.objects.get(id=id)
    context = {'task_data':task_data}
    return render(request, 'task_detail.html', context)



