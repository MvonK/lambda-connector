import socketio
import time
import datetime
import math

from .pygame_visualizer import PygameVisualization


class Lambda(socketio.ClientNamespace):
    def __init__(self, id, token, move_generator, visualizer=True, address='https://lambda.kalab.sk:5000/play',
                 ratelimit=0.23):
        """
        Creates a connection to a lambda server.
        :param id: Your user ID
        :param token: Your secret token
        :param move_generator: Function to execute to get commands for your bots
        :param visualizer: Whether the local pygame visualizer should be on
        :param address: Remote location of the lambda server
        :param ratelimit: Minimum time to wait between two rate limited requests
        """
        super().__init__(namespace="/play")
        self.id = id           # put your ID and token in these two variables
        self.token = token
        self.address = address

        self.rate_limiting_intervals = ratelimit
        self.sio = socketio.Client()

        self.loggedin = False
        self.last_sent = datetime.datetime.now()
        self.move_generator = move_generator
        if visualizer:
            self.visualizer = PygameVisualization()
        else:
            class NoVis:
                def print_state(self, _):
                    pass

                def quit(self):
                    pass
            self.visualizer = NoVis()

    def run(self, ranked=False):
        """
        Run a match
        :param ranked: Whether the match should be against other people or not
        :return:
        """
        self.sio.register_namespace(self)
        self.sio.connect(self.address, headers={"X-Id": self.id, "X-Token": self.token})

        while True:
            time.sleep(1)
            if self.loggedin:
                break

        self.last_sent = datetime.datetime.now()
        if not ranked:
            self.sio.emit("start_training", namespace="/play")
        else:
            self.sio.emit("join_game_queue", namespace="/play")

    def on_connect(self):
        print("I'm connected!")

    def on_connect_error(self):
        print("The connection failed!")

    def on_disconnect(self):
        print("I'm disconnected!")

    def on_message(self, data):
        print('I received a message: ' + data)

    def on_bad_login(self, message):
        print("Bad login! Reason: " + str(message))

    def on_login_successful(self, message):
        self.loggedin = True
        print("Login worked! " + message["message"])

    def on_rate_limit(self, message):
        self.on_game_state_update(None)

    def on_game_results(self, results):
        self.visualizer.quit()
        print("End.")
        if results["winner"] == id:
            print("You won! Congrats!")
        else:
            print("Your opponent was victorious.")
        self.sio.disconnect()

    def on_game_state_update(self, new_data):
        response = []
        if new_data is not None:
            self.visualizer.print_state(new_data)
            state = GameState(new_data, self.id)
            self.move_generator(state)
            response = state.generate_commands()

        to_sleep = (self.last_sent + datetime.timedelta(0, self.rate_limiting_intervals) - datetime.datetime.now()).total_seconds()
        if to_sleep > 0:
            time.sleep(to_sleep)
        self.last_sent = datetime.datetime.now()
        self.sio.emit("commands_update", response, namespace="/play")


class GameState:
    def __init__(self, state, local_id):
        self.time = state["time"]
        self.my_bots = [Bot(b) for b in state["bots"][local_id]]
        opponent_id = list(state["bots"].keys())
        opponent_id.remove(local_id)
        opponent_id = opponent_id[0]
        self.enemy_bots = [Bot(b) for b in state["bots"][opponent_id]]

    def generate_commands(self):
        response = []
        for bot in self.my_bots:
            response.append(bot.generate_commands())
        return response


class Bot:
    def __init__(self, state):
        self.x = None
        self.y = None
        for atr in state:
            self.__dict__[atr] = state[atr]

        self.new_target_angle = None
        self.speed_change = None

    def find_direction_towards(self, bot):
        relative_angle = math.degrees(math.atan2(bot.y - self.y, bot.x - self.x))
        if relative_angle < 0:
            relative_angle = 360 - abs(relative_angle)
        return relative_angle

    def accelerate(self):
        self.speed_change = "accelerate"

    def brake(self):
        self.speed_change = "brake"

    def rotate_towards(self, angle):
        self.new_target_angle = angle

    def generate_commands(self):
        resp = {"bot_id": self.id}
        if self.new_target_angle != None:
            resp["target_angle"] = self.new_target_angle
        if self.speed_change != None:
            resp["speed"] = self.speed_change
        return resp