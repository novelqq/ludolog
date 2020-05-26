from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

GAME_ORGANIZATION = (
    ('W', 'Want to play'),
    ('C', 'Currently playing'),
    ('F', 'Finished Playing'),
    ('D', 'Dropped'),
    ('H', 'Hundred Complete'),
    ('O', 'On hold')
)
# class Game(models.Model):
#     game_id = models.IntegerField()
#     name = models.CharField(max_length=255)


# class Collection(models.Model):
    
#     games = models.ManyToManyField(Game)
#     user = models.ForeignKey(User, related_name='collection', on_delete=models.CASCADE)
    
class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    game_id = models.IntegerField(default=None)
    review = models.TextField(max_length=1000)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    user = models.ForeignKey(User, related_name='logs', on_delete=models.CASCADE)
    status = models.CharField(max_length=6, choices=GAME_ORGANIZATION, default='W')

    def __str__(self):
        return str([("Date: ", self.date), ("Game ID: ", self.game_id), ("Review: ", self.review),
                    ("Score:", self.score), ("User:", self.user), ("Status:", self.status)])