from rasa_nlu.model import Interpreter
import json
from pathlib import Path
import telebot
from datetime import datetime
from random import randint
from PIL import Image, ImageDraw
import os 

model_directory = 'models/nlu/default/model_20190308-114122'
nlu_interpreter = Interpreter.load(model_directory)

#capitals_json = Path("capitals.json").read_text()
#capitals = json.loads(capitals_json)

def parse_message(text,chatid=None):
    tb=telebot.TeleBot("751175863:AAHOSFTBn8opjtUDuzwarKQwq4eNsUWEgsg")
    data = nlu_interpreter.parse(text)
    intent_name = data["intent"]["name"]
    confidence = data["intent"]["confidence"]
    entities = data["entities"]

    print(f"- Model detected intent: {intent_name} ({confidence})")

    if confidence > 0.4:
        print("RESULTADO")
        print(intent_name)
        print(entities)
        return intent_name, entities
    else:
        tb.send_message(chatid,"Podrias repetirlo por favor")
        return "Podrias repetirlo por favor", []

def handle_message(text,chatid=None,name=None):

    intent_name, entities = parse_message(text,chatid)
    response = answer_question(intent_name,entities,chatid,name)
    # Respond to the user
    print(response)
def handle_voice(voice,chatid=None):
    tb=telebot.TeleBot("751175863:AAHOSFTBn8opjtUDuzwarKQwq4eNsUWEgsg")
    tb.send_message(chatid,"Aun no se implementa el audio")

def answer_question(intent_name, entities,chatid=None,name=None):
    tb=telebot.TeleBot("751175863:AAHOSFTBn8opjtUDuzwarKQwq4eNsUWEgsg")
    #if chatid in cadenas:
    response = "Podrias repetirlo por favor"
    try:
        if intent_name == "nombre":
            response = "Mi nombre es Hitsy Security , en que te puedo ayudar"
            tb.send_message(chatid,response)
        elif intent_name == "funciones":
            response = "Entre mis funciones se encuentran:\n  *Reporte de asistencia\n  *Reporte de colaboradores \n  *Reporte de desconocidos\n  *Alertas desconocidos\n  *Aviso de llegada de colaborador"
            tb.send_message(chatid,response)
        elif intent_name == "edad":
            response = "Mi edad es de 4 meses :D"
            tb.send_message(chatid,response)
        elif intent_name == "saludo":
            response = greetingTime()+" "+name+" mi nombre es Hitsy Security y soy el chatbot vigilante de Global Hitss Perú 🤖"
            tb.send_message(chatid,response)
        elif intent_name == "busqueda":
            response = "Por supuesto dame las horas y el dia exacto"
            tb.send_message(chatid,response)
        elif intent_name == "funcion_buscar":
            response = "Enseguida lo busco"
            tb.send_message(chatid,response)
        elif intent_name == "caracteristica":
            response = "No me dieron esa caracteristica 🤖"
            tb.send_message(chatid,response)
        elif intent_name == "agradecimiento":
            response = "Gracias a mis creadores equipo Hitss_L@b"
            tb.send_message(chatid,response)
        elif intent_name == "capital_lookup":
            response = get_capital(entities)
            tb.send_message(chatid,response)
        elif intent_name == "saludo_formal":
            response = greetingTime()+" "+name+" mi nombre es Hitsy Security y soy el chatbot vigilante de Global Hitss Perú 🤖"
            tb.send_message(chatid,response)
        elif intent_name == "reporte_desconocido":
            response = "Estos son los resultados encontrados (En desarrollo) :"
            d=randint(1,900)
            print("RANDOM========================== %d"%d)
            imagen_desconocido=open("/home/marlon/Hitssy_Security/ClasificadorKNN/invitados/invitado%d.jpg" %d,"rb")
            tb.send_message(chatid,response)
            tb.send_photo(chatid,imagen_desconocido)
        elif intent_name == "buscar_ejemplo":
        	response = "Mis creadores aun estan implementando esa funcionalidad 🤖"
        	tb.send_message(chatid,response)
        elif intent_name == "reporte_conocido":
            response = "Estos son los resultados encontrados (En desarrollo):"
            d=randint(1,900)
            #dnis = os.listdir("/home/marlon/Hitssy_Security/ClasificadorKNN/train")
            #print(dnis)
            #imagen_desconocido=open("/home/marlon/Hitssy_Security/ClasificadorKNN/train/foto%d.jpg" %d,"rb")
            tb.send_message(chatid,response)
        elif intent_name == "reporte_asistencia":
            response = "Estos son los resultados encontrados (En desarrollo)"
            tb.send_message(chatid,response)
            file=open("/home/marlon/Hitssy_Security/ASISTENCIA.xlsx","rb")
            tb.send_document(chatid,file)
        elif intent_name == "despedida":
            response = "Cuidate "+name+" vuelve pronto "
            tb.send_message(chatid,response)
            #tb.send_photo(chatid,imagen_desconocido)
        #tb.send_message(chatid,response)
    except:
        response = "Esa funcionalidad aun esta en desarrollo 🤖"
        tb.send_message(chatid,response)
    return response

    #else:
        #response="La contraseña :D"
        #tb.send_message(chatid,response)

def get_capital(entities):
    if len(entities) == 0:
        response = "¿A que te refieres exactamente?"
    else:
        region = entities[0]["value"].title()
        if region in capitals:
            response = f"The capital of {region} is {capitals[region]}"
        else:
            response = f"I'm not sure what the capital of {region} is."

    return response
def cargar_desconocido():
    d=random(1,50)
    imagen_desconocido=Image.open("/home/marlon/Hitssy_Security/ClasificadorKNN/invitados/invitado%d" %d)
    return imagen_desconocido
def listener(messages):
    tb=telebot.TeleBot("751175863:AAHOSFTBn8opjtUDuzwarKQwq4eNsUWEgsg")
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        chatid = m.chat.id
        name = m.chat.first_name
        #print(name)
        if m.content_type == 'text':
            text = m.text
            print(text)
            handle_message(text,chatid,name)
            print(chatid)

        if m.content_type == 'voice':
            audio=m.voice
            handle_voice(audio,chatid)

def greetingTime():

    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Buenos días"
    elif 12 <= current_hour < 18:
        return "Buenas tardes"
    else:
        return "Buenas noches"

if __name__=="__main__":
    
    tb=telebot.TeleBot("751175863:AAHOSFTBn8opjtUDuzwarKQwq4eNsUWEgsg")
    tb.set_update_listener(listener)
    tb.polling()
    tb.polling(none_stop=True)
    tb.polling(interval=1)