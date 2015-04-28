# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.db.models import Max

import hashlib

OPER_AUTORIZATION = '0'
OPER_REFUND = '3'
OPER_SUSCRIPTION = 'L'
OPER_CUOTA_OLD = '6'
OPER_CUOTA = 'M'
OPER_DEFERRED_AUTORIZATION = 'O'
OPER_DEFERRED_CONFIRMATION = 'P'
OPER_DEFERRED_CANCEL = 'Q'

class SermepaIDPTVManager(models.Manager):
    def new_idtpv(self):
        new_idtpv = '%d' % (int(self.all().aggregate(Max('idtpv')).get('idtpv__max') or '1000000000'[:10])+1)
        self.create(idtpv=new_idtpv)
        return new_idtpv

class SermepaIdTPV(models.Model):
    idtpv = models.CharField(max_length=12)
    objects = SermepaIDPTVManager()

    def __unicode__(self):
        return self.idtpv
        
class SermepaResponse(models.Model):
    
    creation_date = models.DateTimeField(auto_now_add=True)
    
    Ds_Date = models.DateField()
    Ds_Hour = models.TimeField()
    Ds_SecurePayment = models.IntegerField()
    Ds_MerchantData = models.CharField(max_length=1024)
    Ds_Card_Country = models.IntegerField(null=True, blank=True)
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
    Ds_TransactionType = models.CharField(max_length=1)
    Ds_Merchant_Identifier = models.CharField(max_length=40, null=True, blank=True)
    Ds_ExpiryDate = models.CharField(max_length=4, null=True, blank=True)
    Ds_Merchant_Group = models.CharField(max_length=9, null=True, blank=True)
    Ds_Card_Number = models.CharField(max_length=40, null=True, blank=True)

    def check_signature(self):
        SECRET_KEY = settings.SERMEPA_SECRET_KEY
             
        key = '%s%s%s%s%s%s' % (self.Ds_Amount, 
                                self.Ds_Order, 
                                self.Ds_MerchantCode, 
                                self.Ds_Currency, 
                                self.Ds_Response, 
                                SECRET_KEY,)
        sha1 = hashlib.sha1(key.encode('utf-8'))
        return sha1.hexdigest().upper() == self.Ds_Signature
    check_signature.boolean = True        
