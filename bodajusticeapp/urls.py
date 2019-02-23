from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include

from . import views

urlpatterns = [
    #User Auth URLs
    path('api-auth/', include('rest_framework.urls')),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.UserCreate.as_view(), name='register'),

    #lawyers urls
    path('add-lawyer/', views.LawyersListCreate.as_view(), name='add_lawyer'),
    path('list-lawyers/', views.LawyersListCreate.as_view(), name='list_lawyers'),
    path('get-lawyer/<str:pk>/', views.LawyersDetails.as_view(), name='get_lawyer'),
    path('update-lawyer/<str:pk>/', views.LawyersDetails.as_view(), name='update_lawyer'),
    path('delete-lawyer/<str:pk>/', views.LawyersDetails.as_view(), name='delete_lawyer'),

    #complainant add profile
    path('add-profile/', views.ComplainantListCreate.as_view(), name='add_profile'),

    #Offences
    path('list-offences/', views.OffenceList.as_view(), name='offences_list'),
    ]