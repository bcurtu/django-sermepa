from django.conf.urls import patterns, url

urlpatterns = patterns('sermepa.views',
    url(
        regex=r'^$',
        view='sermepa_ipn',
        name='sermepa_ipn',
    ),
)
