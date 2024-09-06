from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'), 
    path('i18n/', set_language, name='set_language'),
]
