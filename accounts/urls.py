from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"school_login/$", views.mylogin,name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r'index_schueler/$', views.IndexS.as_view(), name="index_schueler"),
    url(r'index_lehrer/$', views.IndexL.as_view(), name="index_lehrer"),
    url(r'new/$', views.EngVocCreate.as_view(), name="new_eng"),
    url(r'test_going/$', views.test_view,name='mytest'),
    url(r'test_question/$', views.Testqu.as_view(),name='testqu'),
    url(r'new_schueler/$', views.signup, name='newschueler'),
    url(r'klassen/$', views.KlassenListView.as_view(), name='klassenuebersicht'),
    # url(r'/(?P<pk>\d+)/klassen/$', views.KlassenDetailView.as_view(), name='schueleruebersicht'),
]
