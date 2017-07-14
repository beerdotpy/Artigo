import constants, connections, consumers
import ast
import json

# Get name from email
def get_name(email):
    return email.split("@")[0]

"""
When both the users have entered the game, Start the game for both of them
"""
def start_game(key):
    questions = {}
    data = dict(connections.fetch(constants.TABLE_QUESTION))
    for d in data:
        questions[str(d)] = data[d]
    message = constants.START_GAME + "-" + key + "-" + str(questions) 
    consumers.send_message_to_group(key, message) 

"""
Whenever user submits an answer store it in the Database, When he has answered all 5 questions evaluate the score
"""
def store_user_answers(text):
    data = json.loads(text)
    player = get_name(data["user"])
    group = dict(connections.fetch_one(constants.TABLE_GROUP, data["group_key"]))
    temp = ast.literal_eval(group[player])
    # Store user answer in Group table
    temp.update({data["question"] : data["answer"]})
    group[player] = str(temp)
    connections.insert(constants.TABLE_GROUP, data["group_key"], group)
    # If user has submited all answers, calculate scores
    if len(temp.keys()) == 5: evaluate_score(data["group_key"])

"""
Calculate score, if both players have given same answer Award 1 point to both the players
"""
def evaluate_score(key):
    answers = []
    names = []
    data = dict(connections.fetch_one(constants.TABLE_GROUP, key))
    for d in data:
        str_to_dict = ast.literal_eval(data[d])
        if len(str_to_dict.keys()) == constants.NO_OF_QUESTION_IN_TASK:
            answers.append(str_to_dict)
            names.append(d)
    # Wait for both the users to submit
    if len(answers) == 2: 
        score = len(set(answers[0].items()) & set(answers[1].items()))
        update_users_score(names, score)
        message = constants.TASK_COMPLETE + "-" + str(score) 
        consumers.send_message_to_group(key, message)

def update_users_score(names, score):
    print score
    player1 = connections.fetch_one(constants.TABLE_USER, names[0])
    print player1
    player1["score"] += score
    connections.insert(constants.TABLE_USER, names[0], player1)
    player2 = connections.fetch_one(constants.TABLE_USER, names[1])
    player2["score"] += score
    connections.insert(constants.TABLE_USER, names[1], player2)



    