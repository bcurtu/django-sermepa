=============
django-sermepa
=============

Django sermepa es una aplicación muy al estilo de django-paypal para usar el TPV Virtual de Redsys/Sermepa, el TPV más usado en España

Para utilizarlo sigue los siguientes pasos

1. Copia la carpeta sermeta a tu proyecto
2. Añadelo a INSTALLED_APPS
3. Ojo, hay nuevos modelos: syncdb o migrations

4. Añade los siguientes settings::

	SERMEPA_URL_PRO = 'https://sis.redsys.es/sis/realizarPago'
	SERMEPA_URL_TEST = 'https://sis-t.redsys.es:25443/sis/realizarPago'
	SERMEPA_MERCHANT_CODE = '327234688' #test
	SERMEPA_TERMINAL = '002'
	SERMEPA_SECRET_KEY = 'qwertyasdf0123456789'
	SERMEPA_BUTTON_IMG = '/site_media/_img/targets.jpg'
	SERMEPA_CURRENCY = '978'

	Deberás modificar SERMEPA_MERCHANT_CODE, SERMEPA_SECRET_KEY, SERMEPA_BUTTON_IMG, SERMEPA_TERMINAL

5. Añade la ruta de la respuesta de Sermepa a tus urls::

	 (r'^sermepa/', include('sermepa.urls')),
	 
6. Programa las señales de OK, KO y si quieres de error::
 
	from sermepa.signals import payment_was_successful, payment_was_error, signature_error
	def payment_ok(sender, **kwargs):
		'''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
		para asociarlo a tu Pedido o Carrito''
		pass

	def payment_ko(sender, **kwargs):
		'''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
		para asociarlo a tu Pedido o Carrito''
		pass

	def sermepa_ipn_error(sender, **kwargs):
		'''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
		para asociarlo a tu Pedido o Carrito''
		pass

	payment_was_successful.connect(payment_ok)
	payment_was_error.connect(payment_ko)
	signature_error.connect(sermepa_ipn_error)
 
7. Utiliza el form de SermepaPaymentForm para inicializar el botón de pago, al estilo Paypal. 
 Mira el código del ejemplo (sermepa_test/views.py) para más info
 
8. Relájate, sírvete un mojito y espera a hacerte rico.
 