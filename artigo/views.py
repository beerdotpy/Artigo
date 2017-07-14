from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
import connections, constants, utils

@csrf_exempt
def login(request):
    if "user" not in request.session:
        if request.POST:
            name =  utils.get_name(request.POST['email'])
            user = connections.fetch_one(constants.TABLE_USER, name)
            if user is None:        
                user = {
                    "email": request.POST['email'], 
                    "password": request.POST['password'],
                    "score": 0
                    }
                connections.insert(constants.TABLE_USER, name, user) # Insert record into DB
            request.session["user"] = user['email'] # Create session for user

            return HttpResponseRedirect(reverse('index')) 
        return render_to_response('login.html')  
    return HttpResponseRedirect(reverse('index')) 

def index(request):
    user = connections.fetch_one(constants.TABLE_USER, utils.get_name(request.session["user"]))
    return render (request,'index.html',{'email': request.session["user"], 'score': user["score"]}) 

def logout(request):
    if "user" in request.session:
        del request.session["user"]
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('login'))

def start_game(request):
    return render (request,'game.html',{'email': request.session["user"]})