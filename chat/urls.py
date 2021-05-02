from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="chat-home"),
    path('user/<user_id>/', views.UserChatPageView.as_view(), name="chat-user"),
    path('room/<str:room_name>/', views.GroupChatPageView.as_view(), name="chat-group")
]