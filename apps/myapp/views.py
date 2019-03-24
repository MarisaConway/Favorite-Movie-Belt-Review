from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    # print('inside register method in views')
    result = User.objects.reg_validator(request.POST)
    # print('back inside register in views')
    # print(result)
    if len(result) > 0:
        for key, value in result.items():
            # messages.error(request, value)
            messages.add_message(request, messages.ERROR, value)
        return redirect('/')
    else: # passed validations
        # create the user (add to database)
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], email = request.POST['email'], birthday = request.POST['birthday'], password=hash.decode())
        # print(user.id)
        # save their id in session
        request.session['userid'] = user.id
        # redirect to addmovie page/dashboard
        return redirect('/displaymovie')

def displaymovie(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['userid'])
        movies=user.favorites.all()
        unfavorites=[]
        allmovies=Movie.objects.all()
        for i in allmovies:
            if i not in movies:
                unfavorites.append(i)
        context = {
            'user': user,
            'movies': movies,
            'unfavorites': unfavorites
            
        }
        
        return render(request, 'displaymovie.html', context)

def addmovie(request):
    
    return render(request, 'addmovie.html')
def delete(request, id):
    m=Movie.objects.get(id=id)
    m.delete()
    return redirect('/displaymovie')
def favorite(request, id):
    user = User.objects.get(id = request.session['userid'])
    movie=Movie.objects.get(id=id)
    user.favorites.add(movie)
    return redirect('/displaymovie')
def unfavorite(request, id):
    user = User.objects.get(id = request.session['userid'])
    movie=Movie.objects.get(id=id)
    user.favorites.remove(movie)
    return redirect('/displaymovie')
def showmovie(request, id):
    context={
        "movie" : Movie.objects.get(id=id),
        "favorites": Movie.objects.get(id=id).favorites.all()
    }
    return render(request, "showmovie.html", context)

def processmovie(request):    
    result = Movie.objects.movie_validator(request.POST)
    print(result)
    if len(result) > 0:
        for key, value in result.items():
            # messages.error(request, value) alternate method to line below for errors
            messages.add_message(request, messages.ERROR, value)
        return redirect('/addmovie')
    else:
        movie = Movie.objects.create(title=request.POST['title'], year=request.POST['year'], addedby_id=request.session['userid'])
        user = User.objects.get(id = request.session['userid'])
        user.favorites.add(movie)
        return redirect('/displaymovie')
  
def login(request):
    result = User.objects.loginvalidator(request.POST)
    if len(result) > 0:
        for key, value in result.items():
            messages.add_message(request, messages.ERROR, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['userid'] = user.id
        return redirect('/displaymovie')

def logout(request):
    request.session.clear()
    return redirect ('/')

