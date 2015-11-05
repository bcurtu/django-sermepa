# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from Crypto.Cipher import DES3
import hashlib, json, base64, hmac
from .models import SermepaResponse

class SermepaPaymentForm(forms.Form):
    Ds_SignatureVersion = forms.IntegerField(widget=forms.HiddenInput())
    Ds_MerchantParameters = forms.IntegerField(widget=forms.HiddenInput())
    Ds_Signature = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        merchant_parameters = kwargs.pop('merchant_parameters', None)
        super(SermepaPaymentForm, self).__init__(*args, **kwargs)

        if merchant_parameters:
            SECRET_KEY = settings.SERMEPA_SECRET_KEY
            SIGNATURE_VERSION =settings.SERMEPA_SIGNATURE_VERSION


            """
                Se genera una clave específica por operación. Para obtener la
                clave derivada a utilizar en una operación se debe realizar un
                cifrado 3DES entre la clave del comercio y el valor del número de
                pedido de la operación (Ds_Merchant_Order).
            """
            pycrypto = DES3.new(base64.standard_b64decode(SECRET_KEY), DES3.MODE_CBC, IV=b'\x00\x00\x00\x00\x00\x00\x00\x00')
            order = merchant_parameters['DS_MERCHANT_ORDER']
            test = order.ljust(8,b"\x00")
            pycrypto_order = pycrypto.encrypt(test)


            """
                Datos iniciales. Creamos un json y los codificamos en base64 eliminando retornos de carro
            """ 
            parameters = (json.dumps(merchant_parameters)).encode()
            Ds_MerchantParameters = ''.join(unicode(base64.encodestring(parameters), 'utf-8').splitlines())


            """
                Se calcula el HMAC SHA256 del valor del parámetro
                Ds_MerchantParameters y la clave obtenida en el paso anterior.
                El resultado obtenido se codifica en BASE 64, y el resultado de la
                codificación será el valor del parámetro Ds_Signature, tal y
                como se puede observar en el ejemplo de formulario mostrado al
                inicio del apartado 3.
            """
            hmac_value = hmac.new(pycrypto_order, Ds_MerchantParameters, hashlib.sha256).digest()
            Ds_Signature = base64.b64encode(hmac_value)

    
            """
                Estos serían los tres parámetros a enviar a Redsys
            """
            self.initial['Ds_SignatureVersion'] = SIGNATURE_VERSION
            self.initial['Ds_MerchantParameters'] = Ds_MerchantParameters
            self.initial['Ds_Signature'] = Ds_Signature

    def render(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="submit" name="submit" alt="Comprar ahora" value="Comprar ahora"/>
        </form>""" % (settings.SERMEPA_URL_PRO, self.as_p()))

    def sandbox(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="submit" name="submit" alt="Comprar ahora" value="Comprar ahora"/>
        </form>""" % (settings.SERMEPA_URL_TEST, self.as_p()))

class SermepaResponseForm(forms.ModelForm):
    Ds_Date = forms.DateField(required=False, input_formats=('%d/%m/%Y',))
    Ds_Hour = forms.TimeField(required=False, input_formats=('%H:%M',))

    class Meta:
        model = SermepaResponse
        exclude = ()

