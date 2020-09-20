"""
Game current instances of players
"""

from .models import Games
import json

# Get active users


def get_current_users():
    all_games = Games.objects.all()
    current_users = []

    for game in all_games:
        game_inst = json.loads(game.instance)

        for user in game_inst:
            user_data = game_inst[user]

            if (user_data['status'] != 'end'):
                current_users.append(user_data['user'])

    return current_users
