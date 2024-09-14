from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('vat_payer/', views.vat_payer, name='vat_payer'),
    path('vat_payer/<int:pk>', views.vat_payer_record, name='vat_payer_record'),
    path('update_vat_payer/', views.update_vat_payer, name='update_vat_payer'),
 ]