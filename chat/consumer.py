import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Message, MessageHead
from django.db.models import Q

class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        msg = data["message"]

        self.add_new_message_to_db(msg)

        async_to_sync(self.channel_layer.group_send)(
            self.group_chat_name,
            {
                'type':'chat_message',
                'message': msg
            }
        )

    def fetch_message(self, data=None):
        messages = self.get_latest_message()
        data = json.dumps(messages)
        self.send(text_data=json.dumps({'data': data, 'type':'fetched_messages'}))

    commands = {
        'new_message': new_message,
        'fetch_message': fetch_message
    }

    def connect(self):
        self.user = self.scope["user"]
        targetUser_id = self.scope["url_route"]["kwargs"]["user_id"]

        try:
            self.group_chat_name, self.target_user = self.generate_group_name(targetUser_id)
        except:
            self.close(404)
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_chat_name,
            self.channel_name
        )
        self.accept()
    
    def close(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_chat_name,
            self.channel_name
        )
        

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)


    
    def chat_message(self, data):
        msg = data['message']
        self.send(text_data=json.dumps({'message': msg}))
    

    def add_new_message_to_db(self, message):
        head,_ = MessageHead.objects.get_or_create(userFrom=self.user, userTo=self.target_user)
        print(head)
        Message.objects.create(head=head,message=message)
    

    #personal functions

    def generate_group_name(self, target_id):
        curren_user_name = self.scope['user'].username

        target = get_user_model().objects.filter(id=target_id)[0]

        if not target: raise Exception

        if target.id > self.scope['user'].id :
            return f"{curren_user_name}-{target.username}", target
        return f"{target.username}-{curren_user_name}", target
    
    def get_latest_message(self):
        a = self.user
        s = self.target_user
        messages = Message.objects.filter(Q(head__userTo=a, head__userFrom=s)|Q(head__userTo=s, head__userFrom=a))[:10]

        messages_json = []

        for msg in messages:
            messages_json.append(msg.get_json())
        
        return messages_json




class GroupChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_group_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name
        )
        self.accept()
    
    def close(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type':'chat_message',
                'message': data['message']
            }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps({'message':event['message']}))