# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from sermepa.signals import *
from sermepa.forms import SermepaResponseForm

@csrf_exempt
@require_POST
def sermepa_ipn(request):
    form = SermepaResponseForm(request.POST)
    if form.is_valid():
        sermepa_resp = form.save()
        if sermepa_resp.check_signature():
            if int(sermepa_resp.Ds_Response) < 100:
                payment_was_successful.send(sender=sermepa_resp)
            else:
                payment_was_error.send(sender=sermepa_resp)
        else:
            signature_error.send(sender=sermepa_resp)
    return HttpResponse()
