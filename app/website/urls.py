from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('vat_payer/', views.vat_payer, name='vat_payer'),
    path('vat_payer_settings/<int:pk>', views.vat_payer_settings_record, name='vat_payer_settings_record'),
    path('update_vat_payer/', views.update_vat_payer, name='update_vat_payer'),
    path('get-vat-payers/', views.get_vat_payers, name='get_vat_payers'),
    path('get-vat-payer_settings/', views.get_vat_payer_settings, name='get_vat_payer_settings'),
    path('get-customer_vat_check/', views.get_customer_vat_check, name='get_customer_vat_check'),
    path('test/', views.test, name='test'),
    path('test_vat_payer/', views.test_vat_payer, name='test_vat_payer'),
    path('delete_vat_payer_settings/<int:pk>', views.delete_vat_payer_settings, name='delete_vat_payer_settings'),
    path('add_vat_payer_settings/', views.add_vat_payer_settings, name='add_vat_payer_settings'),
    
 ]