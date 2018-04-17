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

def lehrer_plan_detail_pk(request):
    try:
        mypk = request.user.id
        s = models.LehrerStundenplan.objects.filter(lehrer__id=mypk).first()
        return render(request, 'accounts/lehrer_stundenplan_detail.html', {'object':s})
    except:
        return render(request, 'accounts/kein_stundenplan.html')

class RaumCreate(CreateView, LoginRequiredMixin):
    model = models.Raum
    fields = ['bezeichnung', 'beschreibung']
    success_url = reverse_lazy('accounts:uebersicht')

class RaumDelete(DeleteView, LoginRequiredMixin):
    model = models.Raum
    success_url = reverse_lazy('accounts:uebersicht')

class RaumUpdate(UpdateView, LoginRequiredMixin):
    model = models.Raum
    template_name = 'accounts/raum_update.html'
    fields = ['bezeichnung', 'beschreibung']
    success_url = reverse_lazy('accounts:raum_list')

class RaumDetail(DetailView, LoginRequiredMixin):
    model = models.Raum

def raum_liste(request):
    raeume = models.Raum.objects.all()
    mypattern = request.POST.get('search')
    if mypattern:
        raeume = models.Raum.objects.filter(beschreibung__contains=mypattern)
    return render(request, 'accounts/raum_list.html', {'objects':raeume})

class LehrerZeileDelete(DeleteView, LoginRequiredMixin):
    model = models.LehrerZeile
    success_url = reverse_lazy('accounts:lehrer_plan_detail')

class LehrerZeileUpdate(UpdateView, LoginRequiredMixin):
    model = models.LehrerZeile
    fields = ['beginn', 'ende', 'mo', 'di', 'mi', 'do', 'fr']
    success_url = reverse_lazy('accounts:lehrer_plan_detail')
    def form_valid(self, form):
        b = form.cleaned_data['beginn']
        e = form.cleaned_data['ende']
        if b or e:
            if b and e:
                return super().form_valid(form)
            elif b:
                form.add_error("ende","Ende wird benötigt.")
                return self.form_invalid(form)
            else:
                form.add_error("beginn","Beginn wird benötigt.")
                return self.form_invalid(form)
        return super().form_valid(form)

def lehrer_zeile_add(request):
    mypk = request.user.id
    s = models.LehrerStundenplan.objects.filter(lehrer__id=mypk).first()
    s.lehrerzeile_set.create()
    return redirect('accounts:lehrer_plan_detail')

class LehrerPlanDelete(DeleteView, LoginRequiredMixin):
    model = models.LehrerStundenplan
    success_url = reverse_lazy('accounts:uebersicht')

class LehrerPlanCreate(CreateView, LoginRequiredMixin):
    model = models.LehrerStundenplan
    fields = ['name', 'lehrer', ]
    template_name = 'accounts/lehrerstundenplan_form.html'
    success_url = reverse_lazy('accounts:lehrer_plan_detail')

class ZeileDelete(DeleteView, LoginRequiredMixin):
    model = models.Zeile
    success_url = reverse_lazy('accounts:klassenuebersicht')

class ZeileUpdate(UpdateView, LoginRequiredMixin):
    model = models.Zeile
    fields = ['beginn', 'ende', 'mo', 'moraum', 'di', 'diraum', 'mi', 'miraum', 'do', 'doraum', 'fr', 'frraum']
    success_url = reverse_lazy('accounts:klassenuebersicht')
    def form_valid(self, form):
        b = form.cleaned_data['beginn']
        e = form.cleaned_data['ende']
        if b or e:
            if b and e:
                line = form.instance
                line2 = models.Zeile.objects.get(id=line.id)
                if line2.moraum:
                    if line2.moraum.belegung_set:
                        try:
                            models.Belegung.objects.get(tag='mo', beginn=line2.beginn).delete()
                        except:
                            pass
                if line.moraum:
                    if line.moraum.belegung_set.all():
                        for i in line.moraum.belegung_set.all():
                            if (line.beginn >= i.beginn) and (line.beginn < i.ende):
                                form.add_error("moraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (line.ende > i.beginn) and (line.ende <= i.ende):
                                form.add_error("moraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (i.beginn >= line.beginn) and (i.beginn < line.ende) and (i.ende > line.beginn) and (i.ende <= line.ende):
                                form.add_error("moraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                    be1 = models.Belegung.objects.create(raum=form.instance.moraum, tag='mo', beginn=b, ende=e)
                if line2.diraum:
                    if line2.diraum.belegung_set:
                        try:
                            models.Belegung.objects.get(tag='di', beginn=line2.beginn).delete()
                        except:
                            pass
                if line.diraum:
                    if line.diraum.belegung_set.all():
                        for i in line.diraum.belegung_set.all():
                            if (line.beginn >= i.beginn) and (line.beginn < i.ende):
                                form.add_error("diraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (line.ende > i.beginn) and (line.ende <= i.ende):
                                form.add_error("diraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (i.beginn >= line.beginn) and (i.beginn < line.ende) and (i.ende > line.beginn) and (i.ende <= line.ende):
                                form.add_error("diraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                    be2 = models.Belegung.objects.create(raum=form.instance.diraum, tag='di', beginn=b, ende=e)
                if line2.miraum:
                    if line2.miraum.belegung_set:
                        try:
                            models.Belegung.objects.get(tag='mi', beginn=line2.beginn).delete()
                        except:
                            pass
                if line.miraum:
                    if line.miraum.belegung_set.all():
                        for i in line.miraum.belegung_set.all():
                            if (line.beginn >= i.beginn) and (line.beginn < i.ende):
                                form.add_error("miraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (line.ende > i.beginn) and (line.ende <= i.ende):
                                form.add_error("miraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (i.beginn >= line.beginn) and (i.beginn < line.ende) and (i.ende > line.beginn) and (i.ende <= line.ende):
                                form.add_error("miraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                    be3 = models.Belegung.objects.create(raum=form.instance.miraum, tag='mi', beginn=b, ende=e)
                if line2.doraum:
                    if line2.doraum.belegung_set:
                        try:
                            models.Belegung.objects.get(tag='do', beginn=line2.beginn).delete()
                        except:
                            pass
                if line.doraum:
                    if line.doraum.belegung_set.all():
                        for i in line.doraum.belegung_set.all():
                            if (line.beginn >= i.beginn) and (line.beginn < i.ende):
                                form.add_error("doraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (line.ende > i.beginn) and (line.ende <= i.ende):
                                form.add_error("doraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (i.beginn >= line.beginn) and (i.beginn < line.ende) and (i.ende > line.beginn) and (i.ende <= line.ende):
                                form.add_error("doraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                    be4 = models.Belegung.objects.create(raum=form.instance.doraum, tag='do', beginn=b, ende=e)
                if line2.frraum:
                    if line2.frraum.belegung_set:
                        try:
                            models.Belegung.objects.get(tag='fr', beginn=line2.beginn).delete()
                        except:
                            pass
                if line.frraum:
                    if line.frraum.belegung_set.all():
                        for i in line.frraum.belegung_set.all():
                            if (line.beginn >= i.beginn) and (line.beginn < i.ende):
                                form.add_error("frraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (line.ende > i.beginn) and (line.ende <= i.ende):
                                form.add_error("frraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                            elif (i.beginn >= line.beginn) and (i.beginn < line.ende) and (i.ende > line.beginn) and (i.ende <= line.ende):
                                form.add_error("frraum","Raum bereits belegt.")
                                return self.form_invalid(form)
                    be5 = models.Belegung.objects.create(raum=form.instance.frraum, tag='fr', beginn=b, ende=e)
                return super().form_valid(form)
            elif b:
                form.add_error("ende","Ende wird benötigt.")
                return self.form_invalid(form)
            else:
                form.add_error("beginn","Beginn wird benötigt.")
                return self.form_invalid(form)
        mor = form.cleaned_data['moraum']
        dir = form.cleaned_data['diraum']
        mir = form.cleaned_data['miraum']
        dor = form.cleaned_data['doraum']
        frr = form.cleaned_data['frraum']
        l = [mor, dir, mir, dor, frr]
        for i in l:
            if i and not b and not e:
                form.add_error("beginn","Zeitangaben werden benötigt, wenn ein Raum reserviert werden soll.")
                return self.form_invalid(form)
        return super().form_valid(form)

def zeile_add(request, pk):
    res = models.Stundenplan.objects.get(id=pk)
    res.zeile_set.create()
    return redirect('accounts:plan_detail', pk=pk)

class PlanDelete(DeleteView, LoginRequiredMixin):
    model = models.Stundenplan
    success_url = reverse_lazy('accounts:klassenuebersicht')

class PlanDetail(DetailView, LoginRequiredMixin):
    model = models.Stundenplan
    template_name = "accounts/stundenplan_detail.html"

class PlanCreate(CreateView, LoginRequiredMixin):
    model = models.Stundenplan
    fields = ['name', 'klasse', ]
    success_url = reverse_lazy('accounts:klassenuebersicht')

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

def get_user_details(request, pk):
    u = User.objects.get(id=pk)
    return render(request, 'accounts/user_detail.html', {"u":u})

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
