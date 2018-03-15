from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"login/$", views.mylogin,name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r'index_schueler/$', views.IndexS.as_view(), name="index_schueler"),
    url(r'index_lehrer/$', views.IndexL.as_view(), name="index_lehrer"),
    url(r'new/$', views.EngVocCreate.as_view(), name="new_eng"),
    url(r'test_going/$', views.test_view,name='mytest'),
    url(r'test_question/$', views.Testqu.as_view(),name='testqu'),
    url(r'new_schueler/$', views.signup, name='newschueler'),
    url(r'verwaltung/$', views.uebersicht, name='uebersicht'),
    url(r'kurs/(?P<pk>\d+)/$', views.KursDetailView.as_view(), name='kursdetail'),
    url(r'klassen/$', views.KlassenListView.as_view(), name='klassenuebersicht'),
    url(r'klassen/erstellen/$', views.KlasseCreateView.as_view(), name='newklasse'),
    url(r'nummer/(?P<pk>\d+)/$', views.KlassenDetailView.as_view(), name='schueleruebersicht'),
    url(r'schueler/(?P<pk>\d+)/$', views.SchuelerUpdateView.as_view(), name='schuelerchange'),
    url(r'profile/lehrer/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='schuelerprofil'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_lehrer_profile, name='lehrerprofil'),
    url(r'profile/change_password/$', auth_views.password_change,{'template_name':'accounts/change_password.html', 'post_change_redirect':'accounts:password_change_done'}, name='changepwd'),
    url(r'profile/password_change_done/$', auth_views.password_change_done, {'template_name': 'accounts/password_change_done.html'},name='password_change_done'),
    url(r'password_reset/$', auth_views.password_reset,{'subject_template_name':'accounts/password_reset_subject.txt','email_template_name':'accounts/password_reset_email.html','post_reset_redirect':'accounts:password_reset_done'}, name='password_reset'),
    url(r'password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm,{'post_reset_redirect':'accounts:password_reset_complete'}, name='password_reset_confirm'),
    url(r'reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'schueler/delete/(?P<pk>\d+)/$', views.SchuelerDelete.as_view(), name='schueler_del'),
    url(r'kurs/delete/(?P<pk>\d+)/$', views.KursDelete.as_view(), name='kurs_del'),
    url(r'kurs/erstellen/$', views.KursCreate.as_view(), name='newkurs'),
]
