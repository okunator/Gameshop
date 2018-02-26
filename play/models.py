from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from store.models import Game
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Score(models.Model):
    game = models.ForeignKey(Game, related_name="high_scores")
    player = models.ForeignKey(User, related_name="user_scores")
    score = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.game.name + ", " + str(self.score)

    class Meta:
        ordering = ['score']

class GameSave(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    saveData = models.TextField(null=True, blank=True)
    saveDate = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.game.name + ", " + self.user.username

    class Meta:
        unique_together = ("game", "user")
