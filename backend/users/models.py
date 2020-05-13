from django.db import models
from django.contrib.auth.models import AbstractUser

class LudoUser(AbstractUser):
    def __str__(self):
        return self.username

class Game(models.Model):
    game_id = models.IntegerField()
    name = models.CharField(max_length=255)

class Collection(models.Model):
    GAME_ORGANIZATION = (
        ('W', 'Want to play'),
        ('C', 'Currently playing'),
        ('F', 'Finished Playing'),
        ('D', 'Dropped'),
        ('H', 'Hundred Complete')
    )
    games = models.ManyToManyField(Game)
    user = models.ForeignKey(LudoUser, related_name='collection', on_delete=models.CASCADE)
    
class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, related_name='logs', on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    score = models.IntegerField()
    user = models.ForeignKey(LudoUser, related_name='logs', on_delete=models.CASCADE)
    

