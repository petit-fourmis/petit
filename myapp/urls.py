from django.urls import path
from .views import signup_view, login_view,logout_view, dashboard_view, add_measurement_view, edit_measurement_view, delete_measurement_view,index,download_all_measurements_pdf, download_measurement_pdf,CustomLoginView




urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', index, name='index'),
    path('dashboard', dashboard_view, name='dashboard'),
    path('add/', add_measurement_view, name='add_measurement'),
    path('edit/<int:pk>/', edit_measurement_view, name='edit_measurement'),
    path('delete/<int:pk>/', delete_measurement_view, name='delete_measurement'),
    path('download_all/', download_all_measurements_pdf, name='download_all_measurements'),
    path('download/<int:pk>/', download_measurement_pdf, name='download_measurement'),
]

