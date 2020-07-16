from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from .serializers import MyTokenObtainPairSerializer, ProjectsSerializer, UniversitiesSerializer, MilestonesSerializer,	LoginSerializer, CompanySerializer, CollaborationsSerializer

from accounts.models import User
from project.models import Project, Milestones
from company.models import Company
from university.models import University
# Create your views here.

class LoginView(TokenObtainPairView):	
	serializer_class = MyTokenObtainPairSerializer

class Login(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request, *args, **kwargs):
		email = request.data.get("email")
		password = request.data.get("password")
		user = authenticate(email=email, password=password)
		if user and user.user_type == 2:
			data = {
				"message": "Validated",
				"user_id": user.pk,
				'status': status.HTTP_200_OK
			}
			return Response(data, status=status.HTTP_200_OK)
		else:
			data = {
				"message": "Invalid email or password",
				'status': status.HTTP_401_UNAUTHORIZED
			}
			return Response(data, status=status.HTTP_401_UNAUTHORIZED)

class PersonalDetails(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request, *args, **kwargs):
		user_id = request.data.get("user_id")
		company = Company.objects.filter(admin=user_id)
		json_object = CompanySerializer(company, many=True).data
		return Response(json_object)

class Projects(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request, *args, **kwargs):
		user_id = request.data.get("user_id")
		user = User.objects.filter(pk=user_id).first()
		if user:
			company = Company.objects.filter(admin=user.pk).first()
			projects = Project.objects.filter(
				developed_for=company,
				is_deleted=False, 
				developed_by__isnull=False
			).order_by("-created_at")
			json_object = ProjectsSerializer(projects, many=True).data
			return Response(json_object, status=status.HTTP_200_OK)
		else:
			data = {
				"error": "Invalid User ID",
				'status': 401
			}
			return Response(data, status=status.HTTP_401_UNAUTHORIZED)

class GetCollaborations(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request, *args, **kwargs):
		user_id = request.data.get("user_id")
		user = User.objects.filter(pk=user_id).first()
		if user:
			company = Company.objects.filter(admin=user.pk).first()
			projects = Project.objects.filter(
				developed_for=company,
				is_deleted=False, 
				developed_by__isnull=False
			).order_by("-created_at")
			json_object = CollaborationsSerializer(projects, many=True).data
			return Response(json_object, status=status.HTTP_200_OK)
		else:
			data = {
				"error": "Invalid User ID",
				'status': 401
			}
			return Response(data, status=status.HTTP_401_UNAUTHORIZED)

class Universities(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, *args, **kwargs):
		universities = University.objects.all().order_by("ranking")
		json_object = UniversitiesSerializer(universities, many=True).data
		return Response(json_object, status=status.HTTP_200_OK)

class GetMilestones(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request, *args, **kwargs):
		project_id = request.data.get("project_id")
		milestones = Milestones.objects.filter(project=project_id).order_by("created_at")
		json_object = MilestonesSerializer(milestones, many=True).data
		return Response(json_object, status=status.HTTP_200_OK)