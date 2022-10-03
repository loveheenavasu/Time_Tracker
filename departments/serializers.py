from rest_framework import serializers
from .models import *
from accounts.serializers import UserDepartmentSerializer
from main_app.serializers import ProjectsSerializer


class DepartmentsSerializer(serializers.ModelSerializer):
    team_leader = UserDepartmentSerializer(read_only=True)
    completed_projects = ProjectsSerializer(read_only=True)


    class Meta:
        model = Departments
        fields = '__all__'
        # fields = (
        #     'id', 'name', 'description', 'members', 'completed_projects', 'team_leader')

        # read_only_fields = ('team_leader', 'completed_projects')

class DepartmentsSerializerEdit(serializers.ModelSerializer):
    # team_leader = UserDepartmentSerializer(many=True, read_only=True)
    # completed_projects = ProjectDetailSerializer(read_only=True)

    class Meta:
        model = Departments
        # fields = '__all__'
        fields = (
            'id', 'name', 'description', 'members', 'completed_projects', 'team_leader')
