from django.urls import path
from .views import home, webhook

urlpatterns = [
    path('', webhook, name="webhook"),
    path('home/', home, name="home"),
    
]
