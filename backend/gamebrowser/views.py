from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LogForm, SignUpForm
from django.http import Http404
from django.contrib.auth.models import User
import requests

def home(request):
    return render(request, 'home.html')

def game(request, pk):
    game = requests.get('https://api-v3.igdb.com/games/' + str(pk), 
            params={'fields': 'name, rating, cover.*, summary, rating, aggregated_rating, similar_games.*'}, 
            headers={'user-key': '03093c78ab27aa2fb5752d2b7b9167e4'}).json()
    try:
        return render(request, 'game.html', {'game' : game[0]})
    except:
        # raise Http404("Game not found")
        return render(request, 'not_found.html')

def game_list(request):
    games = requests.get('https://api-v3.igdb.com/games', 
            params={'fields': 'name, rating, cover.*', 'search': 'super mario', 'limit': 20},
            headers={'user-key': '03093c78ab27aa2fb5752d2b7b9167e4'}).json()
    for game in games:
        if 'rating' not in game:
            game['rating'] = 0
    games.sort(key=lambda x: x['rating'], reverse=True)

    return render(request, 'game_list.html', {'games': games})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def login_page(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request)

@login_required
def log(request, pk):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.game_id = pk
            log.save()
            return redirect('game', pk=pk)
    else:
        form = LogForm()
    return render(request, 'log.html', {'form': form})


def collection(request, username):
    user = User.objects.all().get(username=username)
    return render(request, 'collection.html', {'user': user})

