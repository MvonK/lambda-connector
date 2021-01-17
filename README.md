# Lambda connector
This is a client to the lambda server, designed with ease-of-use in mind. It offers three 
abstract classes, Lambda, which represents a connection to the server, GameState, which 
represents the current state of game being played and Bot, which represents one bot on the
battlefield. Use `example.py` as a point of reference.

### Lambda
This class requires three parameters: ID, token and move generator. ID and token can be
obtained on [the website](https://lambda.kalab.sk/account). Move generator is your function
that will be used to generate commands to the bots. Your logic will go into this function.
It will receive the current GameState as the only parameter.

There is also a local visualizer, utilizing pygame that offers you real-time view on the 
battlefield, so you can see how are your bots performing. Turn it off by specifying 
`visualizer=False` when creating the Lambda object.

Address is the remote location of the lambda server. This should rarely be changed.

Rate limit is the minimum waiting time between sending rate limited events, in seconds.
The normal rate limit is 0.2 seconds, however since it goes over the internet, events can
be delayed, so that when event A gets dispatched, but if it gets delayed by 0.05 seconds 
and the event B, dispatched after event A, arrives to the server on time, server sees them
arriving within 0.2 seconds space. Therefore the local limit is higher to allow some space 
for unstable latency. 

### Game state
Game state is the active state of the battlefield. It contains these main attributes

- `my_bots`: List of bots, you control
- `enemy_bots`: List of bots that your opponent controls
- `time`: Current game time

### Bot
Bot is an object representing one bot on the field. It has these main attributes:

- `x`: X position on the battlefield
- `y`: Y position on the battlefield
- `speed`: Speed in pixels per second, derived from `speed_category`
- `speed_category`: Speed category of the bot
- `current_angle`: How the bot is rotated
- `id`: ID of the bot (zero to five for each team)

It also offers command functions, used to control the bots behavior.

- `accelerate()`: Increases the bots speed category by one, if possible
- `brake()`: Decreases the bots speed category by one, if possible
- `rotate_towards(angle)`: Tells the bot to start rotating towards a specified angle.
Note, that rotation can be stopped, for example if two bots collide. 

### Notes
Angle is in degrees, where 0 is headed to the west, then increasing clockwise, 
until 360, which is equal to 0. Position x, y of (0, 0) is in the top left corner.