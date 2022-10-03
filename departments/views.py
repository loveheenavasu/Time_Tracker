from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Departments
from .serializers import DepartmentsSerializer, DepartmentsSerializerEdit
from accounts.views import custom_response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from accounts.models import User

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
    context = {'data': data}
    return render(request, 'Admin_templates/department.html', context)


def department_info(request, department_name):
    users = User.objects.filter(department__name=department_name)
    context = {'users': users}
    usercount = User.objects.all().count
    print(usercount, "--------------------------------->")
    return render(request, 'Admin_templates/department_details.html', context)


