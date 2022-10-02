from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rec import views

urlpatterns = [
    path('apart/', views.ApartmentsList.as_view()),
    path('apart/<int:pk>/', views.ApartmentsDetail.as_view()),
    path('apart/price/', views.PriceInfoList.as_view()),
    path('apart/price/<int:pk>/', views.PriceInfoDetail.as_view()),
    path('apart/search/', views.SearchApartmentsList.as_view()),
    path('apart/today/', views.TodayApartmentsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
