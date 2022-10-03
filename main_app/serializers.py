from rest_framework import serializers
from accounts.serializers import UserDepartmentSerializer
from .models import *






class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectsSerializer(read_only=True)
    assigned_to = UserDepartmentSerializer(read_only=True, many=True)
    class Meta:
        model = Task
        fields = '__all__'

class TaskSerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class RemarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks
        fields = '__all__'

class RemarksSerializerGET(serializers.ModelSerializer):
    project = ProjectsSerializer(read_only=True)
    task = TaskSerializerEdit(read_only=True)
    class Meta:
        model = Remarks
        fields = '__all__'




