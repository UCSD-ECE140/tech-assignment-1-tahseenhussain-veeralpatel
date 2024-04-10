import os
import json
from dotenv import load_dotenv

import paho.mqtt.client as paho
from paho import mqtt
import time
import math

from collections import deque
import random
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    print("------------------------------------------------------------------------------------")

    print("\nmessage: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
    
    # OKAY need to skip the games/TestLobby/scores message when its sent 
    playerIDX = search(msg.topic)
    
    chosenPlayer = players[playerIDX]

    print(f"Found: {chosenPlayer}\n")

    # OKAY FOUND ISSUE SOMETIMES IS PUBLISHES TO WRONG THING AND BREAKS LOOP
    # maybe just  
    
    #if playerIDX:
    #user_move = input("\nEnter to iteratate next move...\n")

    
    cmd = pathPlanning(msg.payload, chosenPlayer)
    time.sleep(1)
    client.publish(f"games/{lobby_name}/{chosenPlayer}/move", cmd)
    print("------------------------------------------------------------------------------------")
#else: 
    #    print("\n\nDifferent message type sent - attempting to skip...")
    #    print(f"{msg.topic}")
        #client.publish(f"games/{lobby_name}/Player4/move", "RIGHT")

def is_substring_present(substring, string):
    """Check if the substring is present in the string and return its index if found."""
    return substring in string

def search(msg):
    for index, player in enumerate(players):
        if is_substring_present(player, msg):
            print(f"Identifier found at index: {index} ({player})")
            break
        if is_substring_present('scores',msg):
            return None
    else:
        print(f"processed message that cause error: {msg}")
        print("\n\nNo identifier found.\n\n")
        print("------------------------------------")
        # defaulting to just a random player honestly cus not sure 
        index = random.randint(0,3)
        print(f"\n\n Picked random idx: {index} \n\n")

        print("------------------------------------")

    return index 

def pathPlanning(payload, chosenPlayer) -> str:
    # Path planning algorithm 
    """
    Known:
    Global knowns 
    - currentPosition
    Local knowns 
    - walls in 5x5 radius 

    Choices 
    - Random 
    
    
    - shouldnt try and do global share of data might be awkward in how data is transfered
    - just keep local lists per player 
    
    - for now just develop a path that will read coin location and direct target towards it 
    - have it prompt for user input to take each turn 
    
    okay using BFS - only reset the dict storing tracked squares once target has been reached 
    so only when target has changed we reset the queue pathing 
    
    once a target is found, keep that target until lcoation reached do not change 
    first iteration what do... just go towards edge okay, so two states, edge approach state and 
    target approach state. initial state should just be go towards edge. 
    
    
    
    """
    
    # process msg.topic data first 
    #print(f"String to decode: {str(payload)} + datatype: {type(payload)}")
        
    decoded_payload = payload.decode('utf-8')   
    parsed_data = json.loads(decoded_payload)
    current_position = parsed_data['currentPosition']
    wall_positions = parsed_data['walls']
    
    allCoins = parsed_data['coin1'] + parsed_data['coin2'] +  parsed_data['coin3']
    wallLoc.append(wall_positions)
    #wallLoc.append(parsed_data["teammatePositions"])
    #wallLoc.append(parsed_data["enemyPositions"])
    print(f"Wall & player locations: {wallLoc}")
    # uhhh mid, implemented wrong, switch it up 
    #move_position, move_description = bfs(grid_size, current_position, allCoins, wallLoc, vision_range)
    #destination = movement(current_position, allCoins,wallLoc, chosenPlayer)
    
    
    #print(f"Move info: target {move_position} + descrip {move_description}")
    # Initialize to be -> RIGHT, just a start description 
    nextComm = "RIGHT"
    
    nextComm = moveMethod(current_position, allCoins, wallLoc)
    print(f"Next command: {nextComm}")
    
    return nextComm
    # # If a coin is visible, move towards it
    # if move_description == 'Move to coin':
    #     nextComm = move_towards_target(current_position, move_position, wallLoc)
    # # If no coin is visible, move towards the edge
    # elif move_description == 'Move to edge and rotate':
    #     nextComm = move_towards_target(current_position, move_position, wallLoc)
    #     # If the current position is at the edge, rotate to the next direction
    #     if is_at_edge(current_position[0], current_position[1], grid_size):
    #         current_direction = get_next_direction(current_direction)
    #         # Set the next move based on the new direction
    #         nextComm = move_towards_target(current_position, move_position, wallLoc)
    # else:
    #     # If we are stuck and cannot move
    #     nextComm = get_next_direction(current_direction)
        
    # print(f"Move action: {nextComm}")    
    # command = comm_Move(nextComm, current_position)
    # print(f"Move command: {command}")    
    # return command
    pass
def moveMethod(current_position, allCoins, wallLoc):
    """
    

    Args:
        current_position (_type_): _description_
        allCoins (_type_): _description_
        wallLoc (_type_): _description_
        
    much more simple pp approach, what you originally thought. For now, direct to edge by default!! 
    
    """
    #return edge(current_position,wallLoc )

    # default edge path for now 
    if not allCoins:
        print("\n\nNo coins nearby, going towards edge...")
        return edge(current_position,wallLoc )
    else: 
        print("\n\nCoin found, move toward coin...")
        return coinFinder(current_position, allCoins)
    pass
def coinFinder(cPos, allCoins):
    coinIdx = distance(cPos, allCoins)
    target = allCoins[coinIdx]
    print(f"Coin target: {target}")
    targetCoords = move_towards_target(cPos, target, wallLoc)
    return comm_Move(targetCoords, cPos)
    pass
def edge(cPos, wallLoc):
    if is_at_edge(cPos[0], cPos[1], 9):
        # do rotate 
        #newX, newY = cPos[0] + direction[0], cPos[1] + direction[1]
        print("is at edge, rotate")
        
        return rotateCCw(cPos[0], cPos[1])
    else:
        # go towards edge 
        print("approaching edge")
        borderIdx = distance(cPos, border)
        target = border[borderIdx]
        print(f"edge target: {target}")
        targetCoords = move_towards_target(cPos, target, wallLoc)
        
        return comm_Move(targetCoords, cPos)
def rotateCCw(x,y):
    
    if x == 0 and y > 0:
        return "LEFT"
    elif x == 9 and y < 9:
        return "RIGHT"
    elif y == 0 and x >= 0:
        return "DOWN"
    elif y == 9 and x > 0:
        return "UP"
    else: 
        return "INCORRECT VALUE - THROW ERROR NOW"
    
    # okay okay, change it so that the target INSTEAD of CCW rotation, is to default to CCW direction, but always checking target 
    # block in front of itself
    # 
def rotateCw(x,y):
    
    if x == 0 and y < 9:
        return "RIGHT"
    elif x == 9 and y > 0:
        return "LEFT"
    elif y == 0 and x <= 9:
        return "UP"
    elif y== 9 and x > 0:
        return "DOWN"
    else: 
        return "INCORRECT VALUE - THROW ERROR NOW"
    
def comm_Move(nextComm, cPos):
    # translate nextComm (4,4) into command based on currentPosition (3,4) for exampel
    if (nextComm[0] > cPos[0]):
        return "DOWN"
    elif (nextComm[0] < cPos[0]):
        return "UP"
    elif (nextComm[1] < cPos[1] ):
        return "LEFT"
    elif (nextComm[1] > cPos[1] ):
        return "RIGHT"

    pass

def movement(cPos, aCoins,wallLoc, chosenPlayer):
    # picks the first index of the allCoins array and moves towards it 
    # chance it may get in infinte loop when trying to traverse walls, just try and see for now account for this if it happens
    # fear of global variable conflicting with each other between iterations...?
    # maybe just create global variable to keep track of it one at a time...? 
    print(f"current position: {cPos} + all coins: {aCoins}")

    coinIdx = distance(cPos, aCoins)
    if coinIdx is not None:
        cTarget = aCoins[coinIdx]
    else: 
        cTarget = edge[distance(cPos, edge)]
        
    # for now just set target to be the edge 
    cTarget = edge[distance(cPos, edge)]

    targetLoc[chosenPlayer] = cTarget
    print(f"Target Locations are: {targetLoc}")
    return targetLoc[chosenPlayer]
    pass
def is_valid(x, y, grid_size):
    # s within the grid bounds, not a wall, and not visited
    return 0 <= x <= grid_size and 0 <= y <= grid_size 
def is_at_edge(x, y, grid_size):
    return x == 0 or x == grid_size or y == 0 or y == grid_size

def move_towards_target(current_position, target_position, walls):
    x, y = current_position
    target_x, target_y = target_position
    potential_moves = []

    # Check all directions and categorize based on the target's position
    for direction in DIRECTIONS:
        if direction == "UP" and not is_wall_border((x-1, y), walls, direction):
            potential_moves.append((x-1, y))
        elif direction == "DOWN" and not is_wall_border((x+1, y), walls, direction):
            potential_moves.append((x+1, y))
        elif direction == "LEFT" and not is_wall_border((x, y-1), walls, direction):
            potential_moves.append((x, y-1))
        elif direction == "RIGHT" and not is_wall_border((x, y+1), walls, direction):
            potential_moves.append((x, y+1))

    # sort moves by their distance to the target position
    print(f"\npotential moves list: {potential_moves} <- check if wall loc is added here shouldnt be")
    potential_moves.sort(key=lambda position: (position[0] - target_x) ** 2 + (position[1] - target_y) ** 2)

    # move closest to the target and not blocked by a wall
    return potential_moves[0] if potential_moves else current_position #<- should always be a path so should never happen the if but error checking 

def onlyWalls(position, walls, direction):
    wallPres = any(list(position) in sublist for sublist in walls)
    return wallPres

def is_wall_border(position, walls, direction):
    x = any(list(position) in sublist for sublist in walls)
    # true means wall present, false means not present (valid)
    y = not(is_valid(position[0], position[1] , 9))
    # true means next move is OOB, false means valid
    #print(f"Current wall: {walls[0]} \ntest Position: {position}\nWall present:{x} ")
    #print(f"OOB issue: {y}")
    #print(f"Tested direction: {direction}")
    z = []
    z = x+y
    print(z)
    return z
def distance(cPos, targets) -> list: 
    #print(f"current position: {cPos} + all distances: {aCoins}")
    # extract shorted distance to coin based on cPos
    nearDist = 100
    idx = None
    for i,j in enumerate(targets): 

        dist = (math.sqrt((j[0] - cPos[0])**2 + (j[1] - cPos[1])**2))
        #print(dist)
        if dist < nearDist: # doesnt matter for ties
            nearDist = dist
            idx = i        
    return idx

    pass

def bfs(grid_size, start, allCoins, walls, vision_range):
    queue = deque([start])
    visited = set([(tuple(start),)])
    path_to_edge = None

    while queue:
        x, y = queue.popleft()
        print(f" X Y values that are popped {x} + {y}")
        # Check if the current position is a coin
        if [x, y] in allCoins:
            return [x, y], 'Move to coin'

        # Check if the current position is at the edge and a path to the edge has not been set
        if is_at_edge(x, y, grid_size) and not path_to_edge:
            path_to_edge = [x, y]

        # Check vision range (if beyond, continue)
        if abs(x - start[0]) > vision_range or abs(y - start[1]) > vision_range:
            continue

        # Check and add adjacent nodes to the queue if they are within the vision range
        for dx, dy in xyDir:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y, grid_size, walls, visited):
                queue.append((new_x, new_y))
                visited.add((new_x, new_y))

    # If no coin is found but a path to the edge exists, return that path
    if path_to_edge:
        return path_to_edge, 'Move to edge and rotate'

    return None, 'No coins in sight and no path - should never happen error here '
def get_next_direction(current_direction):
    # Find the index of the current direction and get the next direction
    print(f"cu")
    current_index = DIRECTIONS.index(current_direction)
    # Get the next direction (right turn, clockwise)
    next_index = (current_index + 1) % len(DIRECTIONS)
    return DIRECTIONS[next_index]




# def edgeRotate() -> str:
#     # move towards center of map if no coins read, if allCoins not None or not empty or whatever
#     # just do 4,4 as our closest, if 4,4 not available then the closest one that is 
#     # nvm the edge of the map is always present!!!! so just rotate around the edge lmaooo 
    
    
#     pass


if __name__ == '__main__':
    load_dotenv(dotenv_path='./credentials.env')
    
    broker_address = os.environ.get('BROKER_ADDRESS')
    broker_port = int(os.environ.get('BROKER_PORT'))
    username = os.environ.get('USER_NAME')
    password = os.environ.get('PASSWORD')

    client = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION1, client_id="Player1", userdata=None, protocol=paho.MQTTv5)
    
    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set(username, password)
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect(broker_address, broker_port)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe # Can comment out to not print when subscribing to new topics
    client.on_message = on_message
    client.on_publish = on_publish # Can comment out to not print when publishing to topics

    lobby_name = "TestLobby"
    T1_p1 = "Player1"
    T1_p2 = "Player2"
    T2_p1 = "Player3"
    T2_p2 = "Player4"
    players = [T1_p1, T1_p2, T2_p1, T2_p2]
    border = []
    for j in range(9):
        border.append([0, j])  # Top edge
        border.append([9, j])  # Bottom edge

    for i in range(1, 8):
        border.append([i, 0])  # Left edge
        border.append([i, 9])  # Right edge
 
    print(border)
    
    grid_size = 9
    vision_range = 5
    DIRECTIONS = ["RIGHT", "LEFT", "UP" , "DOWN"]
    xyDir = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
    targetLoc = {T1_p1: "EDGE", T1_p2: "EDGE", T2_p1: "EDGE", T2_p2: "EDGE"}
    visitedLoc = {T1_p1: "None", T1_p2: "None", T2_p1: "None", T2_p2: "None"}
    wallLoc = [] 
    
    print("\n\n\n")
    client.subscribe(f"games/{lobby_name}/lobby")
    client.subscribe(f'games/{lobby_name}/+/game_state')
    #client.subscribe(f'games/{lobby_name}/scores')

    client.publish("new_game", json.dumps({'lobby_name':lobby_name,
                                            'team_name':'ATeam',
                                            'player_name' : T1_p1}))
    
    client.publish("new_game", json.dumps({'lobby_name':lobby_name,
                                            'team_name':'ATeam',
                                            'player_name' : T1_p2}))
    
    client.publish("new_game", json.dumps({'lobby_name':lobby_name,
                                        'team_name':'BTeam',
                                        'player_name' : T2_p1}))
    
    client.publish("new_game", json.dumps({'lobby_name':lobby_name,
                                        'team_name':'BTeam',
                                        'player_name' : T2_p2}))
    
    
    time.sleep(1) # Wait a second to resolve game start
    print("\n\n\n")
    client.publish(f"games/{lobby_name}/start", "START")
    
    
    client.loop_forever()
