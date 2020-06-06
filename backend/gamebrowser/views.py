from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LogForm, SignUpForm
from django.http import Http404
from django.contrib.auth.models import User
import requests
from http.client import HTTPConnection
from django.core.paginator import Paginator
from django.views.generic import ListView

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
    # games = requests.get('https://api-v3.igdb.com/games', 
    #         params={'fields': 'name, rating, cover.*', 'search': 'super mario', 'limit': 20},
    #         headers={'user-key': '03093c78ab27aa2fb5752d2b7b9167e4'}).json()
    # data =
    limit = 50
    page = request.GET.get('page', 1)
    games = requests.post('https://api-v3.igdb.com/games', 
                    data='fields name, aggregated_rating, cover.*; where aggregated_rating > 0' \
                    ' & aggregated_rating_count > 10; sort aggregated_rating desc; limit'+ str(limit)+'; offset '+str(limit*(int(page)-1))+';',
                    headers={'user-key': '03093c78ab27aa2fb5752d2b7b9167e4'}).json()
    for game in games:
        if 'aggregated_rating' not in game:
            game['aggregated_rating'] = 0
        game['aggregated_rating'] = round(game['aggregated_rating'], 2)

    print('LENGTH OF GAMES:', len(games))
    # p = Paginator(games, 2)
    # games = p.page(page)
    # print(games.has_next)

    return render(request, 'game_list.html', {'games': games, 'page': int(page)})

# def search_results(request, query):
#     # search = request.GET.get('q')
#     games = requests.post('https://api-v3.igdb.com/games', 
#                     data='fields name, aggregated_rating, cover.*; search "' + query + '"' \
#                     'sort aggregated_rating desc; limit 20;',
#                     headers={'user-key': '03093c78ab27aa2fb5752d2b7b9167e4'}).json()
#     return render(request, 'search_results.html', {'games': games})

class SearchResultsView(ListView):
    template_name = 'search_results.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        self.query = query
        print("Query: ", query)
        games = requests.post('https://api-v3.igdb.com/games', 
                            data='fields name, aggregated_rating, cover.*; search "' + query + '"; ' \
                            'limit 100;',
                            headers={'user-key': '03093c78ab27aa2fb5752d2b7b9167e4'}).json()
        print('AAAAAAAAAAA fields name, aggregated_rating, cover.*; search "' + query + '"; ' \
                            'sort aggregated_rating desc; limit 20;')
        print(games)
        return games

    def get(self, request):
        context = locals()
        games = self.get_queryset()
        page = request.GET.get('page', 1)
        p = Paginator(games, 10)
        games = p.page(page)
        print(games.has_next)
        context['games'] = games
        context['query'] = self.query
        return render(self.request, self.template_name, context)

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