from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'index.html'


class LoggedInPage(TemplateView):
    template_name = 'logged-in.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'