from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from Time_Tracker.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from .models import Task, Projects, Remarks
from .serializers import TaskSerializer, ProjectsSerializer, RemarksSerializer, RemarksSerializerGET, TaskSerializerEdit
from accounts.views import custom_response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from accounts.views import generate_token
import requests
from django.views.decorators.csrf import csrf_exempt

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



@csrf_exempt
def project(request):
    token = generate_token()
    hed = {"Authorization": f"Bearer {token.get('access')}"}
    print("request", request, request.method)
    if request.GET:
            project_name = request.GET['project_name']
            description = request.GET['description']
            project_deadline = request.GET['project_deadline']

            print(project_name, description, "here")

            base_api = "http://127.0.0.1:8000/projects/"

            data = {
                "project_name": project_name,
                "description": description,
                "project_deadline": project_deadline,
            }
            print(data, "Data")
            req = requests.post(base_api, json=data, headers=hed)
            print(req, "request")
            req.raise_for_status()
            data = req.json()
            print("data", data)
            context = {
                "status": 200,
                "message": data
            }
            return JsonResponse(data)

    else:
        print("invalid")
    return render(request, 'projects.html')



@csrf_exempt
def task(request):
    username = request.user
    print(username)
    token = generate_token()
    hed = {"Authorization": f"Bearer {token.get('access')}"}
    print("request", request, request.method)
    if request.GET:
        project = request.GET['project']
        description = request.GET['description']
        task_name = request.GET['task_name']
        assigned_to = request.GET['assigned_to']
        deadline = request.GET['deadline']

        print(deadline, description, "here")

        base_api = "http://127.0.0.1:8000/task/"

        data = {
            "project": project,
            "description": description,
            "task_name": task_name,
            "assigned_to": assigned_to,
            "deadline": deadline,
        }
        print(data, "Data")
        req = requests.post(base_api, json=data, headers=hed)
        print(req, "request")
        req.raise_for_status()
        data = req.json()
        print("data", data)
        context = {
            "status": 200,
            "message": data
        }
        return JsonResponse(data)

    else:
        print("invalid")
    return render(request, 'task.html')



def demo(request):
    token = generate_token()
    hed = {"Authorization": f"Bearer {token.get('access')}"}
    print("request", request, request.method)
    response = requests.get('http://127.0.0.1:8000/task/9/').json()
    print(response)
    return render(request, 'demo.html', {'response': response})


def logindemo(request):
    return render(request, 'logindemo.html')

