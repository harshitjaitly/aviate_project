from django.urls import path
from . import views


urlpatterns = [

    path('super_view/', views.SuperList.as_view()),
    path('create/', views.ProfileCreate.as_view()),
    path('view_deleted/', views.ViewDeletedProfiles.as_view()),
    path('profile_ops/<int:pk>/', views.ProfileOperations.as_view()),
    path('resume_ops/<int:pk>/', views.ResumeOperations.as_view()),

]
