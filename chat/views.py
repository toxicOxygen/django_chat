from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        users = get_user_model().objects.exclude(id=self.request.user.id)
        return render(self.request, 'chat/home.html',{'users': users})



class UserChatPageView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        target_user_id = kwargs["user_id"]
        target_user = get_object_or_404(get_user_model(),id=target_user_id)
        return render(self.request, 'chat/user_chat.html', {'target_user': target_user})


class GroupChatPageView(View):
    def get(self, *args, **kwargs):
        room_name = kwargs['room_name']
        print(room_name)
        return render(self.request, 'chat/room.html', {'room_name': room_name})