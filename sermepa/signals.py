"""
Note that sometimes you will get duplicate signals emitted, depending on configuration of your systems. 
If you do encounter this, you will need to add the "dispatch_uid" to your connect handlers:
http://code.djangoproject.com/wiki/Signals#Helppost_saveseemstobeemittedtwiceforeachsave

"""
from django.dispatch import Signal

# Sent when a payment is successfully processed.
payment_was_successful = Signal()

# Sent when a refund is successful
refund_was_successful = Signal()

deferred_confirmation_was_successful = Signal()

deferred_cancelation_was_successful = Signal()

# Sent when a payment is error.
payment_was_error = Signal()

# Sent when a signature is not valid
signature_error = Signal()
