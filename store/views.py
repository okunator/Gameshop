from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from store.models import Game, Genre
from django.http import Http404
from .import forms
from django.conf import settings
User = settings.AUTH_USER_MODEL
# from braces.views import SelectRelatedMixin #this is required for models foreignKeys
import time
from hashlib import md5

class AddGame(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
    fields = ('name','genre','description', 'url', 'price', 'coverpicture')
    model = Game
    success_message = "%(name)s has been created"

    def test_func(self):
        return self.request.user.is_developer

    # before committing the form save the ownership changes to database
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.developer = self.request.user #the developer of the game is the one who submits the form
        self.object.save()
        self.object.owners.add(self.request.user) #add the user to owners of the game
        self.object.save()
        self.request.user.my_games.add(self.object)
        self.request.user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Game
    fields = ['name', 'price', 'description', 'genre', 'coverpicture']
    template_name_suffix = '_update_form'
    raise_exception = True
    success_message = "%(name)s has been updated"

    #protect the view from users that arent the developer of the game
    def test_func(self):
        if self.get_object().developer == self.request.user:
            return True
        return False

    def get_success_url(self):
        return reverse('home')

class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Game
    raise_exception = True

    # user needs to be the developer of the game
    def test_func(self):
        if self.get_object().developer == self.request.user:
            return True
        return False

    def get_success_url(self):
        return reverse('home')

class GameDetailView(generic.DetailView):
    model = Game
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BuyView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Game
    template_name = 'store/game_buy.html'
    fields = []
    raise_exception = True

    # protect the view from users that don't have permission to get there
    def test_func(self):
        # user already owns the game
        if self.get_object().developer == self.request.user:
            return False
        # user has bought the game already
        elif self.get_object().owners.all().filter(username__iexact = self.request.user.username).exists():
            return False
        # other authenticated users have permission to buy the game if their logged in
        return True

    # payment data handling in the view according to the instructions
    def get_context_data(self, *args, **kwargs):
        pid = self.request.user.username + "_" + str(self.get_object().id) + "_" + str(time.time())
        amount = self.get_object().price
        sid = 'wsdokumakeotso'
        secret_key = '470a3830bed492b6291a26d65cd2b0cb'
        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
        checksumstr2 = "pid=%s&sid=%s&amount=%s&token=%s" % (pid, sid, amount, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        context = super(BuyView, self).get_context_data(*args, **kwargs)
        context['game'] = self.get_object()
        context['User'] = self.request.user
        context['amount'] = amount
        context['pid'] = pid
        context['sid'] = sid
        context['secret_key'] = secret_key
        context['success_url'] = 'https://indiegames.herokuapp.com/buy/paymentsuccess'
        context['error_url'] = 'https://indiegames.herokuapp.com/buy/paymentstopped'
        context['cancel_url'] = 'https://indiegames.herokuapp.com/buy/paymentstopped'
        context['checksumstr'] = checksumstr
        context['checksumstr2'] = checksumstr2
        context['checksum'] = checksum

        # print(context)
        return context

class PaymentSuccessTemplateView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'store/payment_success.html'
    raise_exception = True

    def test_func(self):
        pid = self.request.GET['pid'].split('_')
        game_id = int(pid[1])
        game = get_object_or_404(Game, id=game_id)
        print(game.owners.all())

        # user is trying to use someboy elses payment succesful URL
        if self.request.user.username != pid[0]:
            return False

        #user already owns the game
        if game.owners.all().filter(username__iexact=self.request.user.username).exists():
            return False

        # now we can do the database changes
        self.request.user.my_games.add(game)
        game.owners.add(self.request.user)
        game.games_sold += 1
        game.save()

        return True

    def get_context_data(self, *args, **kwargs):
        pid = self.request.GET['pid'].split('_')
        game_id = int(pid[1])
        game = get_object_or_404(Game, id=game_id)
        context = super(PaymentSuccessTemplateView, self).get_context_data(*args, **kwargs)
        context['game']=game
        return context


class PaymentCancelTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'store/payment_cancel.html'

    def get_context_data(self, *args, **kwargs):
        result = self.request.GET['result']
        checksum = self.request.GET['checksum']
        context = super(PaymentCancelTemplateView, self).get_context_data(*args, **kwargs)
        if result == 'cancel':
            context['payment_cancel'] = result
        elif result == 'error':
            context['payment_error'] = result
        print(context)
        return context

class ProfileListView(LoginRequiredMixin, generic.ListView):
    model = Game
    template_name = 'store/profile_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileListView, self).get_context_data(*args, **kwargs)
        return context
