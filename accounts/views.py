from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template import RequestContext
from .forms import UserForm, EngForm, SchuelerForm
from . import models
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.utils import timezone
from random import randint
from django.contrib.auth.models import User
from django.contrib import messages #

def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/user_profile.html', {"user":user})

class SchuelerUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'klasse']
    template_name = 'accounts/user_update_form.html'
    success_url = reverse_lazy('accounts:klassenuebersicht')

class KlassenDetailView(DetailView):
    model = models.Klassen
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        data['benutzer'] = User.objects.filter(klasse__id=pk)
        return data

class KlasseCreateView(CreateView):
    model = models.Klassen
    fields = ['bezeichnung', 'lehrer', ]
    success_url = reverse_lazy('accounts:klassenuebersicht')

class KlassenListView(ListView):
    model = models.Klassen

def signup(request):
    if request.method == 'POST':
        form = SchuelerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SchuelerForm()
    return render(request, 'accounts/schueler_form.html', {'form': form})

class EngVocCreate(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/eng_voc_form.html'
    def get(self, request, *args, **kwargs):
        engvoc_form = EngForm()
        EngFormSet = inlineformset_factory(models.Engvoc, models.Ger, fields=('text',), extra=5)
        formset = EngFormSet()
        context = {'form': engvoc_form, 'formset': formset}
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        engvoc_form = EngForm(data=request.POST)
        EngFormSet = inlineformset_factory(models.Engvoc, models.Ger, fields=('text',), extra=5)
        try:
            formset = EngFormSet(data=request.POST, instance=engvoc_form.instance)
        except:
            formset = None
        if formset and engvoc_form.is_valid() and formset.is_valid():
            engvoc = engvoc_form.save()
            eng_des = formset.save(commit=False)
            for eng_de in eng_des:
                eng_de.voc = engvoc
                eng_de.save()
            return HttpResponseRedirect('/accounts/new')
        context = {'form': engvoc_form, 'formset': formset}
        return self.render_to_response(context)

def mylogin(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.groups.filter(name='Lehrer').exists():
                    login(request, user)
                    return HttpResponseRedirect('index_lehrer')
                else:
                    login(request, user)
                    return HttpResponseRedirect('index_schueler')
            else:
                return HttpResponse("Ihr account ist nicht aktiv.")
        else:
            form = UserForm
            return render(request, 'accounts/login_schueler.html', {'form':form}, context)
    else:
        form = UserForm
        return render(request, 'accounts/login_schueler.html', {'form':form}, context)

class IndexS(TemplateView, LoginRequiredMixin):
    template_name = 'index_schueler.html'

class IndexL(TemplateView, LoginRequiredMixin):
    template_name = 'index_lehrer.html'

class Testqu(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/t_time.html'

def test_view(request):
    voc = models.Engvoc.objects.filter(ndatum__gte=timezone.now().date())
    if request.method == 'POST':
        if voc:
            n = randint(0,len(voc)-1)
            return render(request,'accounts/mytest.html',{'voc':models.Engvoc.objects.filter(ndatum__gte=timezone.now().date()).first()})
        else:
            return HttpResponse("Es muss nichts geprüft werden.")
    else:
        if voc:
            myvoc = []
            for i in voc:
                l = [i.eng,]
                for j in i.ger_set.all():
                    l.append(j.text)
                while len(l)<6:
                    l.append('')
                l.append(i.ndatum)
                myvoc.append(l)
            print(myvoc)
            return render(request,'accounts/mytest.html',{'voc':models.Engvoc.objects.filter(ndatum__gte=timezone.now().date())})
        else:
            return HttpResponse("Es muss nichts geprüft werden.")
