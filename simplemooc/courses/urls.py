from django.conf.urls import patterns, include, url

urlpatterns = patterns('simplemooc.courses.views',
    url(r'^$','courses',name='index'),
    #url(r'^(?P<pk>\d+)/$', 'details', name='details'),
    url(r'^(?P<slug>[\w_-]+)/$','details',name='details'),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$','enrollment',name='enrollment'),
    url(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', 'undo_enrollment', name='undo_enrollment'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/$', 'annoucements', name='annoucements'),

    )