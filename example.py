import lambda_connector
import random

id = ""       # Your token and ID. You can generate them on https://lambda.kalab.sk/account
token = ""


def generate_moves(game_state):
    '''
    Put your logic here. You don't need to worry about anything else. You get a nice GameState object as a parameter.
    Don't return anything, only modify bot commands by calling brake(), accelerate() and rotate_towards(angle)
    '''
    for bot in game_state.my_bots:
        bot.accelerate()
        bot.rotate_towards(random.randrange(0, 360))


l = lambda_connector.Lambda(id, token, generate_moves, visualizer=False)
l.run(ranked=False)
