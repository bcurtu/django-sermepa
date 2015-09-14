==============
django-sermepa
==============

Django sermepa es una aplicación muy al estilo de django-paypal para usar el TPV Virtual de Redsys/Sermepa, el TPV más usado en España.

Permite generar cobros puntuales, recurrentes por fichero o por referencia, y devoluciones.

La app tiene una vista que escucha las notificaciones del TPV (se debe pedir su activación a tu banco) y lanza signals para que sean procesadas por tu aplicación de cobros, para cambiar de estado el pedido, enviar emails de notificación...

Nuevo en la versión 1.1.2: **¡Compatible con python 2.7 y python 3.x!**
Nuevo en la versión 1.1.3: Support django 1.4 + (tested in 1.4, 1.5, 1.6, 1.7)

Para utilizarlo sigue los siguientes pasos

1. Instala el proyecto usando pip o bájate las fuentes de github:
 
 1.1 Intalación con pip::

  pip install django-sermepa

 1.2 Usando las fuentes, bájate el proyecto y copia la carpeta sermepa en tu entorno o proyecto.

2. Añadelo a INSTALLED_APPS del settings.py

 .. code:: python

    INSTALLED_APPS += ('sermepa',)
 ..

3. Ojo, hay nuevos modelos: syncdb o migrations (no incluídas, depende de tu versiòn de django)

4. Añade los siguientes settings::

    SERMEPA_URL_PRO = 'https://sis.redsys.es/sis/realizarPago'
    SERMEPA_URL_TEST = 'https://sis-t.redsys.es:25443/sis/realizarPago'
    SERMEPA_MERCHANT_CODE = '327234688' #comercio de test
    SERMEPA_TERMINAL = '002'
    SERMEPA_SECRET_KEY = 'qwertyasdf0123456789'
    SERMEPA_BUTTON_IMG = '/site_media/_img/targets.jpg'
    SERMEPA_CURRENCY = '978' #Euros

 Deberás modificar SERMEPA_MERCHANT_CODE, SERMEPA_SECRET_KEY, SERMEPA_BUTTON_IMG, SERMEPA_TERMINAL

5. Añade la ruta de la respuesta de Sermepa a tus urls:

 .. code:: python

     (r'^sermepa/', include('sermepa.urls')),
 ..
     
6. Programa los listeners de las signals de OK, KO y si quieres de error:
 
 6.1 El listener recibe un objecto de tipo `SermepaResponse <https://github.com/bcurtu/django-sermepa/blob/master/sermepa/models.py>`_
 con toda la información de la operación del TPV. Puedes usar un listener que procese todas los casos, o uno por cada caso (OK y KO)

 .. code:: python

    def payment_ok(sender, **kwargs):
        '''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
        para asociarlo a tu Pedido o Carrito'''
        pedido = Pedido.objects.get(id=sender.Ds_MerchantData)
        pedido.estado = 'cobrado'
        pedido.Ds_AuthorisationCode = sender.Ds_AuthorisationCode #Guardar este valor en caso
        # de poder hacer devoluciones, es necesario.
        pedido.save()
        send_email_success(pedido)

    def payment_ko(sender, **kwargs):
        '''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
        para asociarlo a tu Pedido o Carrito''
        pass        

    def sermepa_ipn_error(sender, **kwargs):
        '''Esta señal salta cuando el POST data recibido está mal firmado. Solo pasa en caso de intentos de cracking.
        sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
        para asociarlo a tu Pedido o Carrito''
        pass
 ..

 6.2 Asocia el listener a las señales, en algún punto que se cargue al iniciar el proyecto, por ejemplo en el models.py

 .. code:: python

    from sermepa.signals import payment_was_successful
    from sermepa.signals import payment_was_error
    from sermepa.signals import signature_error

    payment_was_successful.connect(payment_ok)
    payment_was_error.connect(payment_ko)
    signature_error.connect(sermepa_ipn_error)
 ..

 
7. Utiliza el form de `SermepaPaymentForm <https://github.com/bcurtu/django-sermepa/blob/master/sermepa/forms.py>`_ para inicializar el botón de pago. 

 El botón de pago será un formulario POST a la url del TPV, firmado con tu clave secreta, que deberá pasar toda la información de la operación: modalidad de pago, importe (en céntimos), URLs de notificación, OK y KO, descripción, datos del comercio, identificador de tu pedido, identificador de la operación...
 
 Existen diferentes modalidades de pago:

 1. Las compras puntuales, el Ds_Merchant_TransactionType='0' y el Ds_Merchant_Order debe ser un string siempre único y de 10 caracteres.

 2. Las suscripciones o pagos recurrentes. Existen 2 tipos, por fichero o por referencia.

  2.1 Por fichero, tienen un límite de 12 meses o 12 cobros. 

   2.1.1 El primer cobro el Ds_Merchant_TransactionType='L' y el Ds_Merchant_Order debe ser siempre único. 
    
    El tpv responde con el mismo valor pasado en la variable Ds_Order más 2 dígitos adicionales indicando el número de transacción (la primera es 00)

   2.1.2 Los cobros sucesivos se debe pasar el Ds_Merchant_TransactionType='M' y el primer Ds_Merchant_Order

  2.2 Por referencia, no tiene límite de tiempo ni de cobros. Este sistema soporta cobros de 0€ para activaciones y cambios de tarjetas.

   2.2.1 El primer cobro el Ds_Merchant_TransactionType='0' y el Ds_Merchant_Order='REQUIRED'

    El tpv responde con un nuevo parámetro Ds_Merchant_Identifier, que hay que almacenar (idreferencia)

   2.2.2 Los cobros sucesivos son Ds_Merchant_TransactionType='0' y el Ds_Merchant_Order=idreferencia (el valor que nos han pasado en el primero cobro)

 **Mira el código del ejemplo** (`sermepa_test/views.py <https://github.com/bcurtu/django-sermepa/blob/master/sermepa_test/views.py>`_) para más info:

  .. code:: python

    def form(request, trans_type='0'):
        site = Site.objects.get_current()
        amount = int(5.50 * 100) #El precio es en céntimos de euro

        sermepa_dict = {
            "Ds_Merchant_Titular": 'John Doe',
            "Ds_Merchant_MerchantData": 12345, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": 'ACME',
            "Ds_Merchant_ProductDescription": 'petardos',
            "Ds_Merchant_Amount": amount,
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL": "http://%s%s" % (site.domain, reverse('sermepa_ipn')),
            "Ds_Merchant_UrlOK": "http://%s%s" % (site.domain, reverse('end')),
            "Ds_Merchant_UrlKO": "http://%s%s" % (site.domain, reverse('end')),
            "Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }        
        form = SermepaPaymentForm(initial=sermepa_dict)
        
        return HttpResponse(render_to_response('form.html', {'form': form, 'debug': settings.DEBUG}))

..

  y el form.html:

    .. code:: html

        <html>
        <body>
            {% if debug %}
                {{ form.sandbox }}
            {% else %}
                {{ form.render }}
            {% endif %}
        </body>
        </html>

..

8.  El TPV enviará una respuesta (SermepaResponse) con la información que se le ha enviado más nuevos datos relacionados con el pago. A destacar:

 - Ds_MerchantData es el mismo valor enviado en el formulario en el campo Ds_Merchant_MerchantData. Debería contener el identificador de tu Pedido o Carrito
 - Ds_Merchant_Identifier: la referencia para cobros recurrentes sucesivos si se utiliza el pago por referencia.
 - Ds_ExpiryDate: Fecha de expiración de la tarjeta
 - Ds_Card_Number: Número asteriscado de la tarjeta
 - Ds_AuthorisationCode: Código de la operación autorizada, para poder hacer una devolución posterior.



 
9. Prueba el formulario de compra puntual en http://localhost:8000/ o http://localhost:8000/L/ ...
 
 