from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

import hashlib

from .models import SermepaResponse

class SermepaPaymentForm(forms.Form):

    Ds_Merchant_Currency = forms.IntegerField(widget=forms.HiddenInput())
    Ds_Merchant_Titular = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_MerchantName = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_ProductDescription = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_MerchantData = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_MerchantURL = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_TransactionType = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_Amount = forms.IntegerField(widget=forms.HiddenInput())
    Ds_Merchant_MerchantSignature = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_Terminal = forms.IntegerField(widget=forms.HiddenInput())
    Ds_Merchant_MerchantCode = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_AuthorisationCode = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_Order = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_UrlOK = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_UrlKO = forms.CharField(widget=forms.HiddenInput())
    Ds_Merchant_Identifier = forms.CharField(widget=forms.HiddenInput(), required=False)
    Ds_Merchant_Group = forms.CharField(widget=forms.HiddenInput(), required=False)
    Ds_Merchant_DirectPayment = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(SermepaPaymentForm, self).__init__(*args, **kwargs)

        SECRET_KEY = settings.SERMEPA_SECRET_KEY

        key = '%s%s%s%s%s%s%s%s%s%s' % (self.initial['Ds_Merchant_Amount'], 
                                  self.initial['Ds_Merchant_Order'], 
                                  self.initial['Ds_Merchant_MerchantCode'], 
                                  self.initial['Ds_Merchant_Currency'],
                                  self.initial['Ds_Merchant_TransactionType'], 
                                  self.initial['Ds_Merchant_MerchantURL'],
                                  self.initial.get('Ds_Merchant_Identifier') or '',
                                  self.initial.get('Ds_Merchant_Group') or '',
                                  self.initial.get('Ds_Merchant_DirectPayment') or '',
                                  SECRET_KEY,)
        sha1 = hashlib.sha1(key.encode('utf-8'))
        self.initial['Ds_Merchant_MerchantSignature'] = sha1.hexdigest().upper()
        
    def render(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="image" src="%s" border="0" name="submit" alt="Comprar ahora" />
        </form>""" % (settings.SERMEPA_URL_PRO, self.as_p(), settings.SERMEPA_BUTTON_IMG))
        
    def sandbox(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="image" src="%s" border="0" name="submit" alt="Comprar ahora" />
        </form>""" % (settings.SERMEPA_URL_TEST, self.as_p(), settings.SERMEPA_BUTTON_IMG))
        
class SermepaResponseForm(forms.ModelForm):
    Ds_Date = forms.DateField(required=False, input_formats=('%d/%m/%Y',))
    Ds_Hour = forms.TimeField(required=False, input_formats=('%H:%M',))

    class Meta:
        model = SermepaResponse
    
