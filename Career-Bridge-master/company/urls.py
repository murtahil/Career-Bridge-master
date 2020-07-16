from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.index, name="home" ),
    path('', views.index, name="home" ),
    path('add_new_project/', views.add_new_project, name="add_new_project" ),
    path('my_projects/', views.my_projects, name="my_projects" ),    
    path('projet_details/<int:project_id>/', views.projet_details, name="projet_details" ),  
    path('end_auction/<int:project_id>/', views.end_auction, name="end_auction" ),  
    path('sign_mou/<int:project_id>/', views.sign_mou, name="sign_mou" ),  
    path('confirm_mou/<project_id>/<company_id>/', views.confirm_mou, name="confirm_mou" ),
    path('profile/<int:user_id>/', views.profile, name="profile" ),
    path('update_info/', views.update_info, name="update_info" ),
    path('search/', views.search, name="search" ),
    path('active_projects/', views.active_projects, name="active_projects" ),
    path('milestones/<int:project_id>', views.milestones, name="milestones" ),
    path('delete_projet/', views.delete_projet, name="delete_projet" ),
    path('mark_as_complete/', views.mark_as_complete, name="mark_as_complete" ),
    path('mou_details/<int:project_id>', views.mou_details, name="mou_details" ),    
    path('start_deal/<project_id>/<university_id>/', views.start_deal, name="start_deal" ),
    path('confirm_deal/<project_id>/<company_id>/', views.confirm_deal, name="confirm_deal" ),    

]