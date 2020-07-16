from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('home/', views.index, name="home"),
    path('active_projects/', views.active_projects, name="active_projects" ),
    path('myprojects/', views.myprojects, name="myprojects" ),
    path('project_details/<int:project_id>/', views.project_details, name="project_details" ),
    path('sign_mou/<project_id>/', views.sign_mou, name="sign_mou" ),
    # path('confirmation_mail_received/', views.confirmation_mail_received, name="confirmation_mail_received" ),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('update_info/', views.update_info, name='update_info'),
    path('services/', views.services, name='services'),
    path('delete_service/', views.delete_service, name='delete_service'),


    path('search/', views.search, name='search'),
    path('create_milestone/<int:project_id>', views.create_milestone, name='create_milestone'),
    path('delete_milestone/', views.delete_milestone, name='delete_milestone'),
    path('mou_details/<int:project_id>', views.mou_details, name='mou_details'),
    path('confirm_deal/<project_id>/<company_id>/', views.confirm_deal, name="confirm_deal" ),
    path('done_project_deal/<project_id>/<company_id>/', views.done_project_deal, name="done_project_deal" ),
    

    path('api/chart/data/<int:user_id>', views.ListChartData.as_view()),
    
]
