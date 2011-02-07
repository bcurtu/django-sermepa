# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

import hashlib

class SermepaResponse(models.Model):
    
    creation_date = models.DateTimeField(auto_now_add=True)
    
    Ds_Date = models.DateField()
    Ds_Hour = models.TimeField()
    Ds_SecurePayment = models.IntegerField()
    Ds_MerchantData = models.CharField(max_length=1024, null=True, blank=True)
    Ds_Card_Country = models.IntegerField()
    Ds_Card_Type = models.CharField(max_length=1, null=True, blank=True)
    Ds_Terminal = models.IntegerField()
    Ds_MerchantCode = models.CharField(max_length=9)
    Ds_ConsumerLanguage = models.IntegerField()
    Ds_Response = models.CharField(max_length=4)
    Ds_Order = models.CharField(max_length=12)
    Ds_Currency = models.IntegerField()
    Ds_Amount = models.IntegerField()
    Ds_Signature = models.CharField(max_length=256)
    Ds_AuthorisationCode = models.CharField(max_length=256)
    Ds_TransactionType = models.IntegerField()

    def check_signature(self):
        key = '%s%s%s%s%s%s' % (self.Ds_Amount, 
                                self.Ds_Order, 
                                self.Ds_MerchantCode, 
                                self.Ds_Currency, 
                                self.Ds_Response, 
                                settings.SERMEPA_SECRET_KEY,)
        sha1 = hashlib.sha1(key)
        return sha1.hexdigest().upper() == self.Ds_Signature
    check_signature.boolean = True        
