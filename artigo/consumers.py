from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
import constants, connections, utils
import json,random,string
import ast

"""
Callback when client is connected
"""
def ws_connect(message):
    message.reply_channel.send({"accept": True})

"""
Callback when client is disconnected, Remove the user from queue
"""
def ws_disconnect(message):
    name = str(constants.CONNECTED_USERS[str(message.content['reply_channel'])])
    print "Client Disconnected-" + name
    connections.delete(constants.TABLE_QUEUE, name)

"""
Callback when message is sent to a socket
"""
def ws_message(message):
    """
    If a group already exists i.e A user is in queue, Then add the new user to the same Group
    If no group exists then create a Group, Add user to the group and tell him to wait until someone else joins the group
    """
    if constants.CONNECTED in message.content['text']:
        name = utils.get_name(message.content['text'].split("-")[1]) # Get name of the user connected to socket
        # When user gets connected store his channel id
        constants.CONNECTED_USERS[str(message.reply_channel)] = name
        print constants.CONNECTED_USERS 
        # Check if some other user is in queue
        users_in_queue = connections.fetch(constants.TABLE_QUEUE)
        # If other user is in queue means he is already in a Group, Add this user in the same group and Start the Game 
        if users_in_queue:
            for key in users_in_queue:
                if key != name:
                    group_key = users_in_queue[key]["key"]
                    # Add this user to the Group in which user_in_queue is waiting
                    Group(group_key).add(message.reply_channel)
                    #Remove the user_in_queue from Queue
                    connections.delete(constants.TABLE_QUEUE, key)
                    #Create a group with both the Users as child
                    group = {name:"{}", key:"{}"}
                    connections.insert(constants.TABLE_GROUP, group_key, group) 
                    #Send the message to both to Start the Game
                    utils.start_game(group_key)
                else:
                    Group(users_in_queue[key]["key"]).add(message.reply_channel)
                break
        else:
            client = {
                "name": name,
                "channel": str(message.reply_channel),
                "key": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                }
            Group(client['key']).add(message.reply_channel)
            connections.insert(constants.TABLE_QUEUE, client['name'], client)
    
    #Logging of answers submited by users 
    elif constants.LOG in message.content['text']:
        # Persist users answers in case server is not running
        utils.store_user_answers(message.content['text'].split("-")[1])
        # Log user activity
        connections.push(constants.TABLE_LOG, message.content['text'])

    # When one user want to leave the group, notify the other user also
    elif constants.LEAVE_GROUP in message.content['text']:
        reply = constants.LEAVE_GROUP 
        send_message_to_group(message.content['text'].split("-")[1], reply)

def send_message_to_group(key, message):
    print key, message
    Group(key).send({"text" : message})