# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from sermepa.signals import payment_was_successful, refund_was_successful
from sermepa.signals import payment_was_error, signature_error
from sermepa.forms import SermepaResponseForm
from sermepa.models import OPER_REFUND

@csrf_exempt
def sermepa_ipn(request):
    form = SermepaResponseForm(request.POST)
    if form.is_valid():
        sermepa_resp = form.save()
        if sermepa_resp.check_signature():
            if int(sermepa_resp.Ds_Response) < 100:
                payment_was_successful(sender=sermepa_resp) #signal
            elif sermepa_resp.Ds_Response == '0900' and\
                 sermepa_resp.Ds_TransactionType==OPER_REFUND:
                    refund_was_successful.send(sender=sermepa_resp)  #signal
            else:
                payment_was_error(sender=sermepa_resp) #signal
        else:
            signature_error.send(sender=sermepa_resp) #signal

    return HttpResponse()


