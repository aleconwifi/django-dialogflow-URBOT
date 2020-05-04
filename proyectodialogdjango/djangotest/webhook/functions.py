
import json
import urllib
import requests
import datetime
from re import sub

def replace_asteriks_to_html_format_tag(input_text: str, tag_name: str):
    """Returns the input_text with the asteriks replaced with the html format tag"""
    return sub(r"(\*){1,2}(?=[A-Za-z])|(?<=[a-z])(\*){1,2}",
    lambda m: f"<{tag_name}>" if m.group(1) else f"</{tag_name}>", input_text)
# Driver


def peticionPOST(pregunta):
    payload = {"question":pregunta}
    response = requests.post(f"https://urbot.azurewebsites.net/qnamaker/knowledgebases/801d369e-aac9-4252-90c5-79ce07207970/generateAnswer", json=payload,
    headers={
   "Authorization": "EndpointKey 1f73b6fa-5bbc-43d6-b973-13b8a0879e4b",
    "Content-Type": "application/json"
    }
    )
    resdic = response.json()
    lista =resdic['answers'][0]
    #print (lista['questions'][0])
    #print (lista['answer'])
    #print ("Estos son los promps", type(lista['context']['prompts'][0])) 
    listabotones = []
    listanombres = []
    listaa = []
    listToStr=""
    if (len(lista['context']['prompts']) == 0):
        print('La lista esta vacia')
    else:
        print('NO ESTA VACIA')
        vector = lista['context']['prompts']
        for i in vector:
            listanombres.append(i['displayText'])
        for i in vector:
            listabotones.append([{
                    "text": i['displayText'],
                    "callback_data": i['displayText']
                  }])
        for i in range(len(listanombres)):
          listaa.append("{}\n".format(listanombres[i]))
          listToStr = ' '.join([str(elem) for elem in listaa]) 
        listToStr = "*Pregúntame por alguno de estos términos relacionados: * \n" + listToStr
        print(listToStr)
    return lista['answer'], listabotones, listToStr

def send_email(asunto, html):
    return requests.post(
        "https://api.mailgun.net/v3/mg.vikua.com/messages",
        auth=("api", "key-362b924e925edb7fb84910005a739692"),
        data={"from": "URBOT CORREO <postmaster@mg.vikua.com>",
              "to": "alemvangrieken@gmail.com",
              "subject": asunto,
              "text": "Correo desde django",
              "html": html})

def parametros(req):
    modulo = None
    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M:%S")
    result = req.get("queryResult")
    funcionalidad = result.get("queryText")
    contexto = result.get("outputContexts")
    diccionario = contexto[0]
    print("Contexto 0",diccionario['parameters']['nombre'])
    if (diccionario['parameters']['nombre']['person']['name']):
        nombre = diccionario['parameters']['nombre']['person']['name'] 
    else: 
        nombre = diccionario['parameters']['nombre']
    correo = diccionario['parameters']['correo']
    if req.get("queryResult").get("action") == "sugerencia_modulo_URBO":
        modulo = diccionario['parameters']['modulo']
        return nombre, correo, funcionalidad, modulo, now
    if req.get("queryResult").get("action") == "inconveniente.inconveniente-custom":
        modulo = diccionario['parameters']['modulosurbo1']
        return nombre, correo, funcionalidad, modulo, now
    if req.get("queryResult").get("action") == "sinapsisfalla":
        sinapsis = diccionario['parameters']['sinap']
        return nombre, correo, funcionalidad, sinapsis, now
    else:
        return nombre, correo, funcionalidad, now
