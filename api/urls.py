from django.urls import path
from . import views


urlpatterns = [

    # path('super_view/', views.SuperList.as_view()),

    path('create/', views.ProfileCreate.as_view()),
    path('view_profile/<int:pk>/', views.ViewProfile),
    path('profile_ops/', views.ProfileOperations.as_view()),

    path('upload_resume/', views.UploadResume),
    path('view_current_resume/<int:pk>/', views.ViewCurrentResume),
    path('view_old_resume/<int:pk>/', views.ViewOldResume),
    
    path('super_view/', views.SuperList),
    path('view_deleted/', views.ViewDeletedProfiles),
]
