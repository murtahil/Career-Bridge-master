from rest_framework import serializers, status
from accounts.models import User
from django.contrib.auth import authenticate


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from project.models import Project, Milestones
from university.models import University
from accounts.models import User as MyUser
from company.models import Company

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        data['email'] = str(self.user.email)
        data['id'] = str(self.user.pk)
        return data

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'fullname', 'phone', 'email', 'website')
class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('__all__')
    admin = serializers.SerializerMethodField()
    def get_admin(self, obj):
        user = User.objects.get(pk=obj.admin.pk)
        return UserSerializer(user).data

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'project_name', 'project_description', 'developed_by')
        #fields = ('id', 'project_name', 'project_description', 'is_completed', 'developed_by')
    developed_by = serializers.SerializerMethodField()
    def get_developed_by(self, obj):
        university = University.objects.get(pk=obj.developed_by.pk)
        return UniversitiesSerializer(university).data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'email', 'website')

class UniversitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        exclude = ('created_at',)

    admin = serializers.SerializerMethodField()
    def get_admin(self, obj):
        user = User.objects.get(pk=obj.admin.pk)
        return UserSerializer(user).data

class CollaborationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','project_name', 'developed_by', 'university_mou')
    developed_by = serializers.SerializerMethodField()
    def get_developed_by(self, obj):
        university = University.objects.get(pk=obj.developed_by.pk)
        return UniversitiesSerializer(university).data

class MilestonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestones
        exclude = ('created_at', 'project')