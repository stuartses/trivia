# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
import dateutil.parser
from .models import Games
from chat import questions


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.game_id = -1
        self.game_instances = "{}"
        self.user = ""
        self.question = questions.load(self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Create in database
        if Games.objects.filter(name=self.room_name).exists():
            game = Games.objects.filter(name=self.room_name)[0]
            self.game_id = game.id
        else:
            game = Games()
            game.name = self.room_name
            game.save()
            self.game_id = game.id

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # if game is over clear json instance
        # self.game = Games.objects.get(id=self.game_id)
        # self.game_instances = json.loads(self.game.instance)
        #self.game_instances.pop(self.user, None)
        #self.game.instance = json.dumps(self.game_instances)
        # self.game.save()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        self.game = Games.objects.get(id=self.game_id)
        self.game_instances = json.loads(self.game.instance)

        self.game_json = "{}"
        self.status = "bad"
        self.log = ""
        self.room_status = "open"

        # add current time
        now = datetime.now()
        current_time = now.__str__()

        # content
        option = ""
        if 'option' in text_data_json:
            option = text_data_json['option']

        # user
        user = ""
        if 'user' in text_data_json:
            user = text_data_json['user']
        self.user = user

        # status
        if (option == self.question.answer):
            self.status = "good"

        # score
        score = 0
        self.room_status = "close"
        if self.status == "good":
            timeLess = datetime(2100, 1, 1)
            userWinner = self.user

            if self.user in self.game_instances:
                score = self.game_instances[self.user]['score']

            for user_ins in self.game_instances:
                user_value = self.game_instances[user_ins]
                user_time = dateutil.parser.parse(user_value['time'])
                if user_time < timeLess and user_value['status'] == 'good':
                    timeLess = user_time
                    userWinner = user_value['user']
            if (userWinner == self.user):
                score += 10
                self.log = "Correcto"
            else:
                self.log = "La respuesta es correcta pero el usuario {} respondió primero".format(
                    userWinner)
        if self.status == "bad":
            self.log = "Respuesta incorrecta"
            for user_ins in self.game_instances:
                user_value = self.game_instances[user_ins]
                if user_value['status'] == 'good':
                    userWinner = user_value['user']
                    self.log = "El usuario {} ya acertó esta pregunta".format(userWinner)
                    break

        user_data = {
            'time': current_time,
            'status': self.status,
            'user': user,
            'score': score
        }
        self.game_instances[user] = user_data
        self.game.instance = json.dumps(self.game_instances)
        self.game.name = self.room_name
        self.game.save()

        # Send message to current channel (client)
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'game_message',
                'time': current_time,
                'status': self.status,
                'user': self.user,
                'log': self.log,
                'room_status': self.room_status
            }
        )

        # Send message to room group
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'time': current_time,
                'status': self.status,
                'user': self.user,
                'log': self.log
            }
        )
        """

    # Receive message from room group
    def game_message(self, event):
        time = event['time']
        status = event['status']
        user = event['user']
        log = event['log']
        room_status = event['room_status']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'time': time,
            'status': status,
            'user': user,
            'log': log,
            'room_status': room_status
        }))
