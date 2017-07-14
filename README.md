# Artigo
 An ESP game used for tagging

# Game Rules

1. You need at least two players paired to play this game.
2. Each player may not know whom they are paired with.
3. Each paired player is shown the same question.
4. Each question would have a primary image and a set of secondary images to match to the primary image
5. Both paired players gain one point only when they choose the same set of secondary images

# HOW TO RUN - 

1. pip install virtualenv 
2. virtualenv project
3. cd project
4. source bin/activate
5. git clone https://github.com/sarthakmeh03/Artigo.git
6. cd Artigo
7. pip install -r requirements.txt
8. python manage.py runserver
9. Open localhost:8000/login in your browser

# ASSUMPTIONS

1. If Player A and Player B are paired together, If Player A answers 3 questions and log out of the game then Player B game will also quit.
