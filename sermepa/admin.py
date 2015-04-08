# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import SermepaResponse, SermepaIdTPV

class SermepaResponseAdmin(admin.ModelAdmin):
    search_fields = ['Ds_Order',]
    list_display = ('creation_date','Ds_Order','Ds_Amount',
        'Ds_Response', 'Ds_TransactionType', 'check_signature')
    list_filter = ('creation_date',)

admin.site.register(SermepaResponse,SermepaResponseAdmin)
admin.site.register(SermepaIdTPV,)
