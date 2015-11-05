from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^sermepa/', include('sermepa.urls')),
    url(
        regex   = r'^$',
        view    = 'sermepa_test.views.form',
        name    = 'form',
        ),
    url(
        regex   = r'^(?P<trans_type>[\w])/$',
        view    = 'sermepa_test.views.form',
        name    = 'otros_forms',
        ),
    url(
        regex   = r'^end$',
        view    = 'sermepa_test.views.end',
        name    = 'end',
        ),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
