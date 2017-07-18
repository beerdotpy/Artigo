import constants, connections, consumers
import ast
import json
import random

# Get name from email
def get_name(email):
    return email.split("@")[0]

"""
When both the users have entered the game, Start the game for both of them
"""
def start_game(key):
    questions = []
    # Pick random 5 questions from the whole list 
    data = random.sample((dict(connections.fetch(constants.TABLE_QUESTION))), constants.NO_OF_QUESTION_IN_TASK)
    for d in data:
        questions.append(str(d))
    print questions
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
        questions_answered = set(answers[0].items()) & set(answers[1].items())
        update_attempt(questions_answered)
        score = len(set(answers[0].items()) & set(answers[1].items()))
        update_users_score(names, score)
        message = constants.TASK_COMPLETE + "-" + str(score) 
        consumers.send_message_to_group(key, message)

"""
Whenever 2 users submits same answer for a question,
Update the redundancy to 2 and whatever answer both user has answered to also 2 
"""
def update_attempt(question_answers):
    for q in question_answers:
        data = connections.fetch_one(constants.TABLE_QUESTION, q[0])
        
        data["redundancy"] += 2
        if str(q[1]) == '1':
            data["a"] += 2
        elif str(q[1]) == '2':
            data["b"] += 2
        else:
            data["c"] += 2
        connections.insert(constants.TABLE_QUESTION, q[0], data)
        if data["redundancy"] == constants.REDUNDANCE:
            check_for_consensus(data, q[0])

"""
Whenever a question has reached its max redundancy,
The answer with equal or greater than (REDUNDANCE/2) value will be its actual answer 
"""
def check_for_consensus(data, question):
    result = {}
    
    if data["a"] >= (constants.REDUNDANCE)/2:
        result = {"question": question, "actual_answer": "a"}
    elif data["b"] >= (constants.REDUNDANCE)/2:
        result = {"question": question, "actual_answer": "b"}
    else:
        result = {"question": question, "actual_answer": "c"}
    connections.insert(constants.TABLE_RESULT, question, result)
    connections.delete(constants.TABLE_QUESTION, question)

def update_users_score(names, score):
    print score
    player1 = connections.fetch_one(constants.TABLE_USER, names[0])
    print player1
    player1["score"] += score
    connections.insert(constants.TABLE_USER, names[0], player1)
    player2 = connections.fetch_one(constants.TABLE_USER, names[1])
    player2["score"] += score
    connections.insert(constants.TABLE_USER, names[1], player2)



    