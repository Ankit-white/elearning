from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('ai-help/', views.ai_help),
    path('register/', views.register_view),
    path('upload/', views.upload_file),
]