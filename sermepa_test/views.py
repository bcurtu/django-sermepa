# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

import random

from sermepa.forms import SermepaPaymentForm
from sermepa.signals import payment_was_successful, payment_was_error, signature_error
from sermepa.models import SermepaIdTPV

def form(request, trans_type='0'):
    site = Site.objects.get_current()
    amount = int(5.50 * 100) #El precio es en céntimos de euro

    sermepa_dict = {
        "Ds_Merchant_Titular": 'John Doe',
        "Ds_Merchant_MerchantData": 12345, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
        "Ds_Merchant_MerchantName": 'ACME',
        "Ds_Merchant_ProductDescription": 'petardos',
        "Ds_Merchant_Amount": amount,
        "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
        "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
        "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
        "Ds_Merchant_MerchantURL": "http://%s%s" % (site.domain, reverse('sermepa_ipn')),
        "Ds_Merchant_UrlOK": "http://%s%s" % (site.domain, reverse('end')),
        "Ds_Merchant_UrlKO": "http://%s%s" % (site.domain, reverse('end')),
    }        

    if trans_type == '0': #Compra puntual
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'L': #Compra recurrente por fichero. Cobro inicial
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'M': #Compra recurrente por fichero. Cobros sucesivos
        order = suscripcion.idtpv #Primer idtpv, 10 dígitos
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0': #Compra recurrente por Referencia. Cobro inicial
        order = 'REQUIRED'
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0': #Compra recurrente por Referencia. Cobros sucesivos
        order = suscripcion.idreferencia #Primer idtpv, 10 dígitos
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '3': #Devolución
        order = suscripcion.idreferencia #Primer idtpv, 10 dígitos
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
            "Ds_Merchant_AuthorisationCode": pedido.Ds_AuthorisationCode, #Este valor sale
            # de la SermepaResponse obtenida del cobro que se quiere devolver.
        })

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
