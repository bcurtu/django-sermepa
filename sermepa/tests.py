# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils.encoding import smart_unicode

from sermepa.models import SermepaResponse

class SermepaTest(TestCase):
        
    def test_sermepa_ipn(self):
        data ={'Ds_AuthorisationCode': u'532895', 
                u'Ds_Date': u'26/01/2011', 
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
        c = Client()
        resp = c.post(reverse('sermepa_ipn'), data)
        self.assertEqual(resp.status_code, 200)
        
        sermepa_responses = SermepaResponse.objects.all()
        self.assertEqual(sermepa_responses.count(), 1)
        sermepa_response = sermepa_responses[0]
        self.assertTrue(sermepa_response.check_signature())

                