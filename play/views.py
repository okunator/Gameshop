from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from store.models import Game, Genre
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .import forms
from django.conf import settings
from play.models import Score, GameSave
User = settings.AUTH_USER_MODEL


class PlayTemplateView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'play/play.html'

    # permissions
    def test_func(self):
        return True

    # context dict
    def get_context_data(self, *args, **kwargs):
        user=self.request.user

        # create a 2d-list of personal gamescores. One list for personal scores per game.
        personal_scores = user.user_scores.all().order_by('game')
        if personal_scores.exists():
            personal_scores_by_game_list = []
            personal_scores_per_game = []
            previous_game = [personal_scores.first().game]

            for score in personal_scores:

                if score.game == previous_game[0]:
                    personal_scores_per_game.append(score)
                elif score.game != previous_game[0]:
                    sorted_scores = sorted(personal_scores_per_game, key=lambda score: -score.score)
                    personal_scores_by_game_list.append(sorted_scores)
                    personal_scores_per_game=[]
                    previous_game[0]=score.game

            sorted_scores=sorted(personal_scores_per_game, key=lambda score: -score.score)
            personal_scores_by_game_list.append(sorted_scores)
        else:
            personal_scores_by_game_list = []

        # create context dict
        games=self.request.user.my_games.all()
        context = super(PlayTemplateView, self).get_context_data(*args, **kwargs)
        context['user']=user
        context['games']=games
        context['personalscores']=personal_scores_by_game_list
        print(context)
        return context

class PlayDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Game
    template_name = 'play/play_detail.html'
    raise_exception = True  # raises exeption if user doesnt pass test function

    # let's create a post method for the view so it supports POST-requests
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':

            # SCORE SUBMITTING FROM GAME TO SERVICE
            if self.request.POST['type'] == 'SCORE':
              score = int(self.request.POST['score'])
              game = int(self.request.POST['game'])
              user = int(self.request.POST['user'])
              newscore = Score(game_id=game, player_id=user, score=score)
              newscore.save()
              return HttpResponse("Score saved successfully!")

            # GAME SAVING FROM GAME TO SERVICE
            elif self.request.POST['type'] == 'SAVE':
              data = self.request.POST['data']
              game = int(self.request.POST['game'])
              user = int(self.request.POST['user'])

              if GameSave.objects.filter(game_id=game, user_id=user).exists():
                  GameSave.objects.filter(game_id=game, user_id=user).update(saveData=data)
                  return HttpResponse("save updated successfully!")

              else:
                  newsave = GameSave(game_id=game, user_id=user, saveData=data)
                  newsave.save()
                  return HttpResponse("file saved successfully!")

            # LOAD DATA FROM SERVER TO THE GAME
            elif self.request.POST['type'] == 'LOAD':
                game = int(self.request.POST['game'])
                user = int(self.request.POST['user'])

                if GameSave.objects.filter(game_id=game, user_id=user).exists():
                    result = get_object_or_404(GameSave, game_id=game, user_id=user)
                    print(result.saveData)
                    return HttpResponse(result.saveData)
                else:
                    return HttpResponse("")
    # permissions
    def test_func(self, *args, **kwargs):
        # user owns the game
        game = self.get_object()
        if game.owners.all().filter(username__iexact = self.request.user.username).exists():
            return True
        else:
            return False

    # context dict
    def get_context_data(self, *args, **kwargs):

        context = super(PlayDetailView, self).get_context_data(*args, **kwargs)
        context['user'] = self.request.user
        context['highscores'] = self.object.high_scores.order_by("-score")[:5]

        print(context)
        return context
