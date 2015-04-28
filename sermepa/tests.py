# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.utils import override_settings
from django.conf import settings

from sermepa.models import SermepaResponse, SermepaIdTPV
from sermepa.forms import SermepaPaymentForm

class SermepaTest(TestCase):
        
    # def test_sermepa_ipn(self):
    #     data ={'Ds_AuthorisationCode': u'532895', 
    #             u'Ds_Date': u'26/01/2011', 
    #             u'Ds_SecurePayment': u'1', 
    #             u'Ds_MerchantData': u'custom_code', 
    #             u'Ds_Card_Country': u'724', 
    #             u'Ds_Terminal': u'001', 
    #             u'Ds_MerchantCode': u'022711378', 
    #             u'Ds_ConsumerLanguage': u'1', 
    #             u'Ds_Response': u'0000', 
    #             u'Ds_Order': u'1825926', 
    #             u'Ds_Currency': u'978', 
    #             u'Ds_Amount': u'25', 
    #             u'Ds_Signature': u'D381D30F295819A7129CE0D6E76EA228D9AA88C1', 
    #             u'Ds_TransactionType': u'0', 
    #             u'Ds_Hour': u'16:25'}
    #     c = Client()
    #     resp = c.post(reverse('sermepa_ipn'), data)
    #     self.assertEqual(resp.status_code, 200)
        
    #     sermepa_responses = SermepaResponse.objects.all()
    #     self.assertEqual(sermepa_responses.count(), 1)
    #     sermepa_response = sermepa_responses[0]
    #     self.assertTrue(sermepa_response.check_signature())

    @override_settings(SERMEPA_SECRET_KEY = 'qwertyasdf0123456789')
    def test_sermepa_response(self):

        data ={'Ds_AuthorisationCode': u'532895', 
                u'Ds_Date': u'2011-12-12', 
                u'Ds_SecurePayment': u'1', 
                u'Ds_MerchantData': u'custom_code', 
                u'Ds_Card_Country': u'724', 
                u'Ds_Terminal': u'001', 
                u'Ds_MerchantCode': u'022711378', 
                u'Ds_ConsumerLanguage': u'1', 
                u'Ds_Response': u'0000', 
                u'Ds_Order': u'1825926', 
                u'Ds_Currency': u'978', 
                u'Ds_Amount': u'25', 
                u'Ds_Signature': u'D381D30F295819A7129CE0D6E76EA228D9AA88C1', 
                u'Ds_TransactionType': u'0', 
                u'Ds_Hour': u'16:25'}

        response = SermepaResponse.objects.create(**data)
        self.assertTrue(response.check_signature())

    def test_max_idtpv(self):
        new_idtpv = SermepaIdTPV.objects.new_idtpv()
        self.assertEqual(new_idtpv, '1000000001')
        new_idtpv = SermepaIdTPV.objects.new_idtpv()
        self.assertEqual(new_idtpv, '1000000002')

        idtpv = SermepaIdTPV.objects.create(idtpv='2000100065')
        new_idtpv = SermepaIdTPV.objects.new_idtpv()
        self.assertEqual(new_idtpv, '2000100066')
        self.assertEqual(SermepaIdTPV.objects.filter(idtpv='2000100066').count(),1)

    # @override_settings(SERMEPA_SECRET_KEY = 'qwertyasdf0123456789')
    # def test_sermepa_response_reference(self):

    #     data ={'Ds_AuthorisationCode': u'325302', 
    #             u'Ds_Date': u'2011-12-12', 
    #             u'Ds_SecurePayment': u'0', 
    #             u'Ds_MerchantData': u'Alfombrilla', 
    #             u'Ds_Card_Country': u'724', 
    #             u'Ds_Terminal': u'22', 
    #             u'Ds_MerchantCode': u'079940722', 
    #             u'Ds_ConsumerLanguage': u'1', 
    #             u'Ds_Response': u'0000', 
    #             u'Ds_Order': u'1305093030', 
    #             u'Ds_Currency': u'978', 
    #             u'Ds_Amount': u'200', 
    #             u'Ds_Signature': u'384BB9675FEE4D88358079FCCC16BC2940B6F7AF', 
    #             u'Ds_TransactionType': u'0', 
    #             u'Ds_Hour': u'16:25',
    #             u'Ds_ExpiryDate': u'4912',
    #             u'Ds_Merchant_Identifier': u'32539c31f319d3ad67de24ed8fc5ec92e2c4124a',
    #             }

    #     response = SermepaResponse.objects.create(**data)
    #     self.assertTrue(response.check_signature())

    @override_settings(SERMEPA_SECRET_KEY = 'qwertyasdf0123456789')
    def test_sermepa_form(self):
        data = {
            "Ds_Merchant_Titular": 'pepe',
            "Ds_Merchant_MerchantData": u'200010003000',
            "Ds_Merchant_MerchantName": 'my little book box',
            "Ds_Merchant_ProductDescription": 'mlbb',
            "Ds_Merchant_Amount": '200',
            "Ds_Merchant_TransactionType": '0',
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Order":u'200010003000',
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL": 'http://www.google.com/',
            "Ds_Merchant_UrlOK": 'http://www.google.com/',
            "Ds_Merchant_UrlKO": 'http://www.google.com/',          
        }

        form = SermepaPaymentForm(initial=data)
        self.assertEqual(form.initial.get('Ds_Merchant_MerchantSignature'), 'E05535DB514E6BECFB99CD88834D91A851744639')

    @override_settings(SERMEPA_SECRET_KEY = 'qwertyasdf0123456789')
    def test_sermepa_form_referencia(self):
        data = {
            "Ds_Merchant_Titular": 'pepe',
            "Ds_Merchant_MerchantData": u'200010003000',
            "Ds_Merchant_MerchantName": 'my little book box',
            "Ds_Merchant_ProductDescription": 'mlbb',
            "Ds_Merchant_Amount": '200',
            "Ds_Merchant_TransactionType": '0',
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Order":u'200010003000',
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL": 'http://www.google.com/',
            "Ds_Merchant_UrlOK": 'http://www.google.com/',
            "Ds_Merchant_UrlKO": 'http://www.google.com/',       
            "Ds_Merchant_Identifier": 'REQUIRED',   
        }

        form = SermepaPaymentForm(initial=data)
        self.assertEqual(form.initial.get('Ds_Merchant_MerchantSignature'), 'B96632D7907E414097BBD53B9886A223DB763ADE')
