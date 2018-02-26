from django.views.generic import TemplateView, ListView
from store.models import Game, Genre

# class HomePage(TemplateView):
#     template_name = 'index.html'

class HomePageListView(ListView):
    model = Game
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class BasePage(TemplateView):
    template_name = 'base.html'
