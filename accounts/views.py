from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template import RequestContext
from .forms import UserForm, EngForm, SchuelerForm, ThemaForm, ThemaFormZwei
from . import models
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.utils import timezone
from random import randint
from django.contrib.auth.models import User
from django.contrib import messages #
from django.core.mail import send_mail

class ZeileDelete(DeleteView, LoginRequiredMixin):
    model = models.Zeile
    success_url = reverse_lazy('accounts:klassenuebersicht')

class ZeileUpdate(UpdateView, LoginRequiredMixin):
    model = models.Zeile
    fields = ['beginn', 'ende', 'mo', 'di', 'mi', 'do', 'fr']
    success_url = reverse_lazy('accounts:klassenuebersicht')

def zeile_add(request, pk):
    res = models.Stundenplan.objects.get(id=pk)
    res.zeile_set.create()
    return redirect('accounts:klassenuebersicht')

class PlanDelete(DeleteView, LoginRequiredMixin):
    model = models.Stundenplan
    success_url = reverse_lazy('accounts:uebersicht')

class PlanDetail(DetailView, LoginRequiredMixin):
    model = models.Stundenplan
    template_name = "accounts/stundenplan_detail.html"

class PlanCreate(CreateView, LoginRequiredMixin):
    model = models.Stundenplan
    fields = ['name', 'klasse', ]
    success_url = reverse_lazy('accounts:uebersicht')

def all_klasse(request, pk):
    res = models.Kurs.objects.get(id=pk)
    k = User.objects.filter(klasse=res.klasse).exclude(groups__name='Lehrer')
    for i in k:
        myid = i.id
        betreffend = User.objects.get(id=myid)
        res.teilnehmer.add(betreffend)
    return redirect('accounts:uebersicht')

# .exclude(kurs.teilnehmer in kurs_set.all())
def plusschueler(request, pk, myid=None, act=0):
    kurs = models.Kurs.objects.get(pk=pk)
    if (act != 0) and myid:
        betreffend = User.objects.get(id=myid)
        kurs.teilnehmer.remove(betreffend)
    elif myid:
        betreffend = User.objects.get(id=myid)
        kurs.teilnehmer.add(betreffend)
    moeglich = User.objects.exclude(groups__name='Lehrer')
    mypattern = request.POST.get('search')
    if mypattern:
        moeglich = User.objects.exclude(groups__name='Lehrer').filter(username__contains=mypattern)
    # for i in kurs.teilnehmer.all():
    #     print(i)
    return render(request, 'accounts/plus_schueler.html', {'moeglich':moeglich, 'kurs':kurs})

class OhneKurs(ListView, LoginRequiredMixin):
    model = User
    template_name = 'accounts/okurs.html'
    queryset = User.objects.filter(Teilnehmer=None)

class OhneKlasse(ListView, LoginRequiredMixin):
    model = User
    queryset = User.objects.filter(klasse=None)
    template_name = 'accounts/oklasse.html'

class KlasseUpdate(UpdateView, LoginRequiredMixin):
    model = models.Klassen
    success_url = reverse_lazy('accounts:klassenuebersicht')
    fields = ['lehrer', 'stellvertreter', ]
    template_name = 'accounts/klassen_update.html'

class UserDetail(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'accounts/user_detail.html'

class KlasseDelete(DeleteView, LoginRequiredMixin):
    model = models.Klassen
    success_url = reverse_lazy('accounts:klassenuebersicht')

class ThemaUpdate(UpdateView, LoginRequiredMixin):
    form_class = ThemaFormZwei
    model = models.Thema
    template_name = 'accounts/thema_update.html'
    success_url = reverse_lazy('accounts:index_lehrer')

class ThemaDelete(DeleteView, LoginRequiredMixin):
    model = models.Thema
    success_url = reverse_lazy('accounts:index_lehrer')

class ThemaDetailSchueler(DetailView):
    model = models.Thema
    template_name = 'accounts/thema_detail_schueler.html'

class ThemaDetailOfficial(DetailView):
    model = models.Thema
    template_name = 'accounts/thema_detail_official.html'

class ThemaDetail(DetailView):
    model = models.Thema

class ThemaListOfficial(ListView):
    model = models.Thema
    queryset = models.Thema.objects.order_by('-erstellt')
    template_name = 'accounts/themen_official.html'

class ThemaListSchueler(ListView):
    model = models.Thema
    queryset = models.Thema.objects.order_by('-erstellt')
    template_name = 'accounts/themen_schueler.html'

class ThemaList(ListView):
    model = models.Thema
    queryset = models.Thema.objects.order_by('-erstellt')

class ThemaCreate(CreateView, LoginRequiredMixin):
    form_class = ThemaForm
    template_name = 'accounts/thema_form.html'
    success_url = reverse_lazy('accounts:index_lehrer')

class KursUpdate(UpdateView, LoginRequiredMixin):
    model = models.Kurs
    fields = ['lehrer', 'stellvertreter', 'klasse']
    template_name = 'accounts/kurs_update.html'
    success_url = reverse_lazy('accounts:uebersicht')

class KursCreate(CreateView, LoginRequiredMixin):
    model = models.Kurs
    fields = ['bezeichnung', 'lehrer', 'stellvertreter', 'klasse', ]
    success_url = reverse_lazy('accounts:uebersicht')

class KursDelete(DeleteView, LoginRequiredMixin):
    model = models.Kurs
    success_url = reverse_lazy('accounts:uebersicht')

class SchuelerDelete(DeleteView, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('accounts:uebersicht')
    template_name = 'accounts/user_confirm_delete.html'

class KursDetailView(DetailView, LoginRequiredMixin):
    model = models.Kurs

def get_lehrer_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/lehrer_profile.html', {"user":user})

def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/user_profile.html', {"user":user})

def uebersicht(request):
    kurse = models.Kurs.objects.all()
    mypattern = request.POST.get('search')
    if mypattern:
        kurse = models.Kurs.objects.filter(bezeichnung__contains=mypattern)
    return render(request, 'accounts/uebersicht.html', {'kurse':kurse})

class SchuelerUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    fields = ['username', 'email', 'klasse']
    template_name = 'accounts/user_update_form.html'
    success_url = reverse_lazy('accounts:klassenuebersicht')

class KlassenDetailView(DetailView, LoginRequiredMixin):
    model = models.Klassen
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        data['benutzer'] = User.objects.filter(klasse__id=pk)
        return data

class KlasseCreateView(CreateView, LoginRequiredMixin):
    model = models.Klassen
    fields = ['bezeichnung', 'lehrer', 'stellvertreter', ]
    success_url = reverse_lazy('accounts:klassenuebersicht')

class KlassenListView(ListView, LoginRequiredMixin):
    model = models.Klassen

def signup(request):
    if request.method == 'POST':
        form = SchuelerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            mail = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            link = 'http://127.0.0.1:8000/accounts/password_reset/'
            msg = 'Registrierung von %s (mit der E-Mail Adresse %s), Link zum Registrieren: %s' %(username, mail, link)
            send_mail('Registrierung',msg,'sina.andreas@gmail.com',[mail],fail_silently=True)
            return redirect('accounts:klassenuebersicht')
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

class IndexS(ListView, LoginRequiredMixin):
    template_name = 'index_schueler.html'
    model = models.Thema
    queryset = models.Thema.objects.order_by('-erstellt')[:3]

class IndexL(ListView, LoginRequiredMixin):
    template_name = 'index_lehrer.html'
    model = models.Thema
    queryset = models.Thema.objects.order_by('-erstellt')[:3]

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
