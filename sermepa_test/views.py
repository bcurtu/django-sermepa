# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

import random

from sermepa.forms import SermepaPaymentForm
from sermepa.signals import payment_was_successful, payment_was_error, signature_error

def form(request):
    site = Site.objects.get_current()
    merchant_url =  "http://%s%s" % (site.domain, reverse('sermepa_ipn'))
    amount = int(5.50 * 100)
    order = '%d' % random.randint(1000,9999999)
    currency = 978
    trans_type = 0
    terminal = 1

    sermepa_dict = {
        "Ds_Merchant_Titular": 'Bosco Curtu',
        "Ds_Merchant_MerchantData": 'custom info',
        "Ds_Merchant_MerchantName": 'ACME',
        "Ds_Merchant_ProductDescription": 'petardos',
        "Ds_Merchant_Amount": amount,
        "Ds_Merchant_TransactionType": trans_type,
        "Ds_Merchant_Terminal": terminal,
        "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
        "Ds_Merchant_Order": order,
        "Ds_Merchant_Currency": currency,
        "Ds_Merchant_MerchantURL": merchant_url,
        "Ds_Merchant_UrlOK": "http://%s%s" % (site.domain, reverse('end')),
        "Ds_Merchant_UrlKO": "http://%s%s" % (site.domain, reverse('end')),
    }        
    form = SermepaPaymentForm(initial=sermepa_dict)
    
    return HttpResponse(render_to_response('form.html', {'form': form, 'debug': settings.DEBUG}))
    
def end(request):
    return HttpResponse(render_to_response('end.html', {}))
    
def payment_ok(sender, **kwargs):
    pass

def payment_ko(sender, **kwargs):
    pass

def sermepa_ipn_error(sender, **kwargs):
    pass

payment_was_successful.connect(payment_ok)
payment_was_error.connect(payment_ko)
signature_error.connect(sermepa_ipn_error)
