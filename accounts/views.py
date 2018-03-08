from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template import RequestContext
from .forms import UserForm, EngForm
from . import models
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.utils import timezone
from random import randint

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
