from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .functions import peticionPOST, send_email, parametros, replace_asteriks_to_html_format_tag

import json
import urllib
import requests




def home(request):
    return HttpResponse('Prueba de conexion')

@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    # return a fulfillment message
 
    if action == "input.prueba":
        result = req.get("queryResult")
        pregunta = result.get("queryText")
        parameters = result.get("parameters")
        terminos  = parameters.get("terminos")
        print("este es terminos", terminos)
        respuesta, listabotones, listanombres = peticionPOST(terminos)
        speech = ("Buscando en mi base de datos de documentos conseguí: \n" + respuesta + "\n\n")
        print("Response:")
        #print(speech)
        result = {}
        if len(listabotones)==0:
          result = {
          "text": {
            "text": [
              speech
            ]
          },
          "platform": "TELEGRAM"
        },{
          "payload": {
            "telegram": {
              "reply_markup": {
                "inline_keyboard": listabotones
              },
              "text": "Si quieres saber otro término, solo pregúntame "
            }
          },
          "platform": "TELEGRAM"
        },{
          "text": {
            "text": [
              replace_asteriks_to_html_format_tag(speech, "b") + "\n Si quieres saber otro término, solo pregúntame"
            ]
          }
        }
        else:
          result = {
          "text": {
            "text": [
              speech
            ]
          },
          "platform": "TELEGRAM"
        },{
          "payload": {
            "telegram": {
              "reply_markup": {
                "inline_keyboard": listabotones
              },
              "text": "Términos relacionados:"
            }
          },
          "platform": "TELEGRAM"

        },{
        "text": {
          "text": [
            "Puedes seleccionar los términos relacionados o preguntarme otro término"
          ]
        },
        "platform": "TELEGRAM"
      },{
          "text": {
            "text": [
               replace_asteriks_to_html_format_tag(speech, "b") + "\n" + listanombres
            ]
          }
        }
        return JsonResponse(  fulfillmentText = {'fulfillmentMessages':result })
        
    elif action == "input.modelos":
      
        result = req.get("queryResult")
        pregunta = result.get("queryText")
        #parameters = result.get("parameters")
        #terminos  = parameters.get("terminos")
        #print("este es terminos", terminos)
        respuesta, listabotones, listanombres = peticionPOST(pregunta)
        speech = ("Buscando en mi base de datos de documentos conseguí: \n" + respuesta + "\n\n")
        print("Response:")
        #print(speech)
        result = {}
        if len(listabotones)==0:
          result = {
          "text": {
            "text": [
              speech
            ]
          },
          "platform": "TELEGRAM"
        },{
          "payload": {
            "telegram": {
              "reply_markup": {
                "inline_keyboard": listabotones
              },
              "text": "Si quieres saber otro término, solo pregúntame "
            }
          },
          "platform": "TELEGRAM"
        },{
          "text": {
            "text": [
              replace_asteriks_to_html_format_tag(speech, "b") + "\n Si quieres saber otro término, solo pregúntame"
            ]
          }
        }
        else:
          result = {
          "text": {
            "text": [
              speech
            ]
          },
          "platform": "TELEGRAM"
        },{
          "payload": {
            "telegram": {
              "reply_markup": {
                "inline_keyboard": listabotones
              },
              "text": "Términos relacionados:"
            }
          },
          "platform": "TELEGRAM"

        },{
        "text": {
          "text": [
            "Puedes seleccionar los términos relacionados o preguntarme otro término"
          ]
        },
        "platform": "TELEGRAM"
      },{
          "text": {
            "text": [
               replace_asteriks_to_html_format_tag(speech, "b") + "\n" + listanombres
            ]
          }
        }
        return JsonResponse(  fulfillmentText = {'fulfillmentMessages':result })

    elif action == "input.OtraPregunta":
        result = req.get("queryResult")
        pregunta = result.get("queryText")
        parameters = result.get("parameters")
        terminosi  = parameters.get("terminosi")
        print("este es terminosi", terminosi)
        respuesta, listabotones, listanombres = peticionPOST(terminosi)
        speech = ("Buscando en mi base de datos de documentos conseguí: \n" + respuesta + "\n\n" )
        print("Response:")
        #print(speech)

        result = {}
        if len(listabotones)==0:
          result = {
          "text": {
            "text": [
              speech
            ]
          },
          "platform": "TELEGRAM"
        },{
          "payload": {
            "telegram": {
              "reply_markup": {
                "inline_keyboard": listabotones
              },
              "text": "Si quieres saber otro término, solo pregúntame "
            }
          },
          "platform": "TELEGRAM"
        },{
          "text": {
            "text": [
               replace_asteriks_to_html_format_tag(speech, "b") + "\n Si quieres saber otro término, solo pregúntame"
            ]
          }
        }
        else:

          result = {
          "text": {
            "text": [
              speech
            ]
          },
          "platform": "TELEGRAM"
        },{
          "payload": {
            "telegram": {
              "reply_markup": {
                "inline_keyboard": listabotones
              },
              "text": "Términos relacionados:"
            }
          },
          "platform": "TELEGRAM"

        },{
        "text": {
          "text": [
            "Puedes seleccionar los términos relacionados o preguntarme otro término"
          ]
        },
        "platform": "TELEGRAM"
      },{
          "text": {
            "text": [
              replace_asteriks_to_html_format_tag(speech, "b") + "\n" + listanombres
            ]
          }
        }
        return JsonResponse( {'fulfillmentMessages':result })
        #SUGERENCIAS    
    elif action == "sugerencia_atencion_al_usuario":
        nombre, correo, funcionalidad, now = parametros(req)
        send_email("Reporte de URBOT: Recomendación por {}".format(nombre), '<h1 style="color: #5e9ca0;"><span style="color: #808000;">¡{0}, ha usado URBOT y ha realizado la siguiente acción!</span></h1> <h2 style="color: #2e6c80;">Recomendación de mejorar la Atención al Usuario:</h2> <p>El usuario de nombre <strong>{0}</strong> y correo <strong>{1}</strong>, ha realizado una recomendación para mejorar la atención al usuario a las <strong>{3}</strong>, en donde explica :</p> <blockquote><strong> <p>{2}</p></strong> </blockquote> <p>&nbsp;</p> <p><strong>&nbsp;<img src="https://res.cloudinary.com/vikua/image/upload/v1581651986/samples/URBO/urbotsolo_w0naqo.png" alt="" width="157" height="250" /></strong></p> <p><strong>Atentamente</strong></p> <p><strong>&iexcl;URBOT!</strong></p>'.format(nombre, correo, funcionalidad, now))
    elif action == "sugerencia_modulo_URBO":
        nombre, correo, funcionalidad, modulo, now = parametros(req)
        send_email("Reporte de URBOT: Recomendación por {}".format(nombre), '<h1 style="color: #5e9ca0;"><span style="color: #808000;">¡{0}, ha usado URBOT y ha realizado la siguiente acción!</span></h1> <h2 style="color: #2e6c80;">Recomendación de funcionalidad:</h2> <p>El usuario de nombre <strong>{0}</strong> y correo <strong>{1}</strong>, ha realizado una recomendación&nbsp;al <strong>módulo de {2}</strong> a las <strong>{4}</strong>, en donde propone <strong>modificar</strong> en URBO:</p> <blockquote><strong> <p>{3}</p></strong> </blockquote> <p>&nbsp;</p> <p><strong>&nbsp;<img src="https://res.cloudinary.com/vikua/image/upload/v1581651986/samples/URBO/urbotsolo_w0naqo.png" alt="" width="157" height="250" /></strong></p> <p><strong>Atentamente</strong></p> <p><strong>&iexcl;URBOT!</strong></p>'.format(nombre, correo, modulo, funcionalidad, now))
        #REPORTAR FALLAS
    elif action == "inconveniente.inconveniente-custom":
        nombre, correo,problema, modulo, now = parametros(req)
        send_email("Reporte de URBOT: Reporte de Falla por {}".format(nombre), '<html><h1 style="color: #5e9ca0;"><span style="color: #808000;">¡{0}, ha usado URBOT y ha realizado la siguiente acción!</span></h1> <h2 style="color: #2e6c80;">Reporte de falla de módulo de {2} :</h2> <p>El usuario de nombre <strong>{0}</strong>, correo <strong>{1}</strong> </strong>, ha realizado el reporte de una falla en el <strong>módulo de {2}</strong> a las <strong>{4}</strong>, presentando el siguiente problema:</p> <blockquote><strong> <p>{3}</p></strong> </blockquote> <p>&nbsp;</p> <p><strong>&nbsp;<img src="https://res.cloudinary.com/vikua/image/upload/v1581651986/samples/URBO/urbotsolo_w0naqo.png" alt="" width="157" height="250" /></strong></p> <p><strong>Atentamente</strong></p> <p><strong>&iexcl;URBOT!</strong></p></html>'.format(nombre, correo, modulo, problema, now))
    elif action == "sinapsisfalla":
        nombre, correo,falla, sinapsis, now= parametros(req)
        send_email("Reporte de URBOT: Reporte de Falla por {}".format(nombre), '<html><h1 style="color: #5e9ca0;"><span style="color: #808000;">¡{0}, ha usado URBOT y ha realizado la siguiente acción!</span></h1> <h2 style="color: #2e6c80;">Reporte de falla del sinapsis de la unidad número {2} :</h2> <p>El usuario de nombre <strong>{0}</strong>, correo <strong>{1}</strong> </strong>, ha realizado el reporte de una falla del sinapsis <strong>de la unidad número {2}</strong>, presentando según él, el siguiente problema:</p> <blockquote><strong> <p>{3}</p></strong> </blockquote> <p>&nbsp;</p> <p><strong>&nbsp;<img src="https://res.cloudinary.com/vikua/image/upload/v1581651986/samples/URBO/urbotsolo_w0naqo.png" alt="" width="157" height="250" /></strong></p> <p><strong>Atentamente</strong></p> <p><strong>&iexcl;URBOT!</strong></p></html>'.format(nombre, correo, sinapsis, falla, now ))
        #SESION EN VIVO
    elif action == "sesion_en_vivo_para":
        nombre, correo, now = parametros(req)
        send_email("Reporte de URBOT: Recomendación por {}".format(nombre), '<html><h1 style="color: #5e9ca0;"><span style="color: #808000;">¡{0}, ha usado URBOT y ha realizado la siguiente acción!</span></h1> <h2 style="color: #2e6c80;">Solictud de sesión en vivo :</h2> <p>El usuario de nombre <strong>{0}</strong>, correo <strong>{1}</strong>, ha realizado una solicitud de sesión en vivo a las <strong>{2}</strong></p> <p>&nbsp;</p> <p><strong>&nbsp;<img src="https://res.cloudinary.com/vikua/image/upload/v1581651986/samples/URBO/urbotsolo_w0naqo.png" alt="" width="157" height="250" /></strong></p> <p><strong>Atentamente</strong></p> <p><strong>&iexcl;URBOT!</strong></p></html>'.format(nombre, correo, now))
    elif action == '':
        print("la acccion no tiene webhook")
        return None
