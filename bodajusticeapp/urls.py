from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from rest_framework.authtoken import views as authviews

from . import views

urlpatterns = [
    #User Auth URLs
    path('api-auth/', include('rest_framework.urls')),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.UserCreate.as_view(), name='register'),
    path('api-token-auth/', authviews.obtain_auth_token),

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

    #cases
    path('accept-complaint/<str:complaint_id>/', views.CaseCreate.as_view(), name="create_case"),
    path('view-all-cases/', views.CaseCreate.as_view(), name="list_all_cases"),
    path('close-case/<str:pk>/', views.CloseCase.as_view(), name='close_Case'),

    #complaints
    path('create-complaint/', views.ComplaintListCreate.as_view(), name='list_create_complaint'),
    path('complaint/<str:pk>/', views.ComplaintRetrieveUpdateDelete.as_view(), name='complaint-details'),
    ]