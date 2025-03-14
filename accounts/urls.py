from django.urls import path
from .views import home, custom_register, custom_login, admin_panel

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", custom_login, name="login"),
    path("admin-panel/", admin_panel, name="admin_panel"),
    path("dashboard/", views.dashboard, name="user_dashboard"),
    path('boost/', boost_view, name='boost'),
]
