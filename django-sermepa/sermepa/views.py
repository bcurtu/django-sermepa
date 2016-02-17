# -*- coding: utf-8 -*-
from django.http import HttpResponse
import dateutil.parser
from django.views.decorators.csrf import csrf_exempt

from sermepa.signals import payment_was_successful, refund_was_successful
from sermepa.signals import payment_was_error, signature_error
from sermepa.forms import SermepaResponseForm
from sermepa.models import OPER_REFUND, SermepaResponse
from sermepa.utils import decode_parameters, redsys_check_response

@csrf_exempt
def sermepa_ipn(request):
    form = SermepaResponseForm(request.POST)
    if form.is_valid():

        # Get parameters from decoded Ds_MerchantParameters object
        merchant_parameters = decode_parameters(form.cleaned_data['Ds_MerchantParameters'])
        sermepa_resp = SermepaResponse()

        if 'Ds_Date' in merchant_parameters:
            sermepa_resp.Ds_Date = dateutil.parser.parse((merchant_parameters['Ds_Date']).replace('%2F','/'), dayfirst=True)
        if 'Ds_Hour' in merchant_parameters:
            sermepa_resp.Ds_Hour = dateutil.parser.parse((merchant_parameters['Ds_Hour']).replace('%3A',':'))
        if 'Ds_Amount' in merchant_parameters:
            sermepa_resp.Ds_Amount = merchant_parameters['Ds_Amount']
        if 'Ds_Currency' in merchant_parameters:
            sermepa_resp.Ds_Currency = merchant_parameters['Ds_Currency']
        if 'Ds_Order' in merchant_parameters:
            sermepa_resp.Ds_Order = merchant_parameters['Ds_Order']
        if 'Ds_MerchantCode' in merchant_parameters:
            sermepa_resp.Ds_MerchantCode = merchant_parameters['Ds_MerchantCode']
        if 'Ds_Terminal' in merchant_parameters:
            sermepa_resp.Ds_Terminal = merchant_parameters['Ds_Terminal']
        if 'Ds_Response' in merchant_parameters:
            sermepa_resp.Ds_Response = merchant_parameters['Ds_Response']
        if 'Ds_TransactionType' in merchant_parameters:
            sermepa_resp.Ds_TransactionType = merchant_parameters['Ds_TransactionType']
        if 'Ds_SecurePayment' in merchant_parameters:
            sermepa_resp.Ds_SecurePayment = merchant_parameters['Ds_SecurePayment']
        if 'Ds_MerchantData' in merchant_parameters:
            sermepa_resp.Ds_MerchantData = merchant_parameters['Ds_MerchantData']
        if 'Ds_Card_Country' in merchant_parameters:
            sermepa_resp.Ds_Card_Country = merchant_parameters['Ds_Card_Country']
        if 'Ds_AuthorisationCode' in merchant_parameters:
            sermepa_resp.Ds_AuthorisationCode = merchant_parameters['Ds_AuthorisationCode']
        if 'Ds_ConsumerLanguage' in merchant_parameters:
            sermepa_resp.Ds_ConsumerLanguage = merchant_parameters['Ds_ConsumerLanguage']
        if 'Ds_Merchant_Identifier' in merchant_parameters:
            sermepa_resp.Ds_Merchant_Identifier = merchant_parameters['Ds_Merchant_Identifier']
        if 'Ds_ExpiryDate' in merchant_parameters:
            sermepa_resp.Ds_ExpiryDate = merchant_parameters['Ds_ExpiryDate']

        sermepa_resp.save()

        # Check signature
        valid_signature = redsys_check_response(form.cleaned_data['Ds_Signature'], form.cleaned_data['Ds_MerchantParameters'], )
        if valid_signature:
            if int(sermepa_resp.Ds_Response) < 100:
                payment_was_successful.send(sender=sermepa_resp) #signal
            elif sermepa_resp.Ds_Response == '0900' and\
                 sermepa_resp.Ds_TransactionType==OPER_REFUND:
                    refund_was_successful.send(sender=sermepa_resp)  #signal
            else:
                payment_was_error.send(sender=sermepa_resp) #signal
        else:
            signature_error.send(sender=sermepa_resp) #signal
    return HttpResponse()


