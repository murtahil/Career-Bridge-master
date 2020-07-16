from django.urls import path, include
from .views import LoginView, Projects, Universities, GetMilestones, GetCollaborations, Login, PersonalDetails
urlpatterns = [
    path('login/', Login.as_view(), name="login" ),
    path('personal_details/', PersonalDetails.as_view(), name="login" ),

    path('projects/', Projects.as_view(), name="projects" ),
    path('universities/', Universities.as_view(), name="universities" ),
    path('milestones/', GetMilestones.as_view(), name="milestones" ),
    path('collaborations/', GetCollaborations.as_view(), name="collaborations" ),

]