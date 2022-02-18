from django.urls import path
from . import views


urlpatterns = [

    path('create/', views.ProfileCreate.as_view()),
    path('view_all_profiles/', views.ProfileList.as_view()),
    path('view_deleted/', views.DeletedProfiles.as_view()),
    path('profile_ops/<int:pk>/', views.ProfileDetails.as_view()),

]
