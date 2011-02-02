from django.conf.urls.defaults import *

urlpatterns = patterns('sermepa.views',
    url(
        regex=r'^sermepa/ipn/$',
        view='sermepa_ipn',
        name='sermepa_ipn',
    ),         
)
