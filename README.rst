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
	SERMEPA_MERCHANT_CODE = '327234688' #comercio de test
	SERMEPA_TERMINAL = '002'
	SERMEPA_SECRET_KEY = 'qwertyasdf0123456789'
	SERMEPA_BUTTON_IMG = '/site_media/_img/targets.jpg'
	SERMEPA_CURRENCY = '978' #Euros

	Deberás modificar SERMEPA_MERCHANT_CODE, SERMEPA_SECRET_KEY, SERMEPA_BUTTON_IMG, SERMEPA_TERMINAL

5. Añade la ruta de la respuesta de Sermepa a tus urls::

	 (r'^sermepa/', include('sermepa.urls')),
	 
6. Programa las señales de OK, KO y si quieres de error::
 
	from sermepa.signals import payment_was_successful, payment_was_error, signature_error
	def payment_ok(sender, **kwargs):
		'''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
		para asociarlo a tu Pedido o Carrito''
		pedido = Pedido.objects.get(id=sender.Ds_MerchantData)
		pedido.estado = 'cobrado'
		pedido.save()
		send_email_success(pedido)
		...
		'''

	def payment_ko(sender, **kwargs):
		'''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
		para asociarlo a tu Pedido o Carrito''
		pass

	def sermepa_ipn_error(sender, **kwargs):
		'''Esta señal salta cuando el POST data recibido está mal firmado. Solo pasa en caso de intentos de cracking.
		sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
		para asociarlo a tu Pedido o Carrito''
		pass

	payment_was_successful.connect(payment_ok)
	payment_was_error.connect(payment_ko)
	signature_error.connect(sermepa_ipn_error)
 
7. Utiliza el form de SermepaPaymentForm para inicializar el botón de pago, al estilo Paypal. 
 
 Mira el código del ejemplo (sermepa_test/views.py) para más info:

 Existen diferentes modalidades de pago:
 1.- Las compras puntuales, el Ds_Merchant_TransactionType='0' y el Ds_Merchant_Order debe ser siempre único y de 10 cifras.
 2.- Ls suscripciones o pagos recurrentes. Existen 2 tipos, por fichero o por referencia.
 2.1- Por fichero, tienen un límite de 12 meses o 12 cobros. 
 2.1.1 El primer cobro el Ds_Merchant_TransactionType='L' y el Ds_Merchant_Order debe ser siempre único.
 El tpv responde con el mismo valor pasado en la variable Ds_Order más 2 dígitos adicionales indicando el número de transacción (la primera es 00)
 2.1.2 Los cobros sucesivos se debe pasar el Ds_Merchant_TransactionType='M' y el primer Ds_Merchant_Order

 2.2- Por referencia, no tiene límite de tiempo ni de cobros. Este sistema soporta cobros de 0€ para activaciones y cambios de tarjetas.
 2.2.1 El primer cobro el Ds_Merchant_TransactionType='0' y el Ds_Merchant_Order='REQUIRED'
 El tpv responde con un nuevo parámetro Ds_Merchant_Identifier, que hay que almacenar (idreferencia)
 2.2.2 Los cobros sucesivos son Ds_Merchant_TransactionType='0' y el Ds_Merchant_Order=idreferencia (el valor que nos han pasado en el primero cobro)


 
8. Prueba el formulario de compra puntual en http://localhost:8000/

9. Relájate, sírvete un mojito y espera a hacerte rico.
 