from django.contrib import admin
from django.urls import path
from accounts.views import home_view, custom_register, custom_login, admin_panel, dashboard
from accounts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('register/', custom_register, name='register'),
    path('login/', custom_login, name='login'),
    path("dashboard/", dashboard, name="user_dashboard"),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('boost/', views.boost, name='boost'),
]
