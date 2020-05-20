from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
import requests

def home(request):
    return render(request, 'home.html')

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
