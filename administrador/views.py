# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
import requests 
import json
from django.http import HttpResponse
from temba_client.v2 import TembaClient
from django.core.urlresolvers import reverse
from unicef_app.connect_to_rapidpro import connect_to_client, obtener_token_brigadistas, obtener_token_embarazadas
# Create your views here.

def dashboard(request):
    return render(request, 'admin/dashboard.html')

###################################################################

def agregar_embarazada(request):
    return render(request, 'admin/agregar_embarazada.html')


def modificar_embarazada(request):
    client = connect_to_client()
    lista_de_embarazadas = client.get_contacts(group=obtener_token_embarazadas())
    contexto = {
        'lista_de_embarazadas': lista_de_embarazadas.all()
    }
    return render(request, 'admin/modificar_embarazada.html', context = contexto)

class ajax_agregar_embarazada(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            
            client = connect_to_client()

            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            cedula = request.POST.get('cedula')
            semana_embarazo = request.POST.get('semana_embarazo')
            edad = request.POST.get('edad')
            etnia = request.POST.get('etnia')
            region = request.POST.get('region')
            municipio = request.POST.get('municipio')
            comunidad = request.POST.get('comunidad')
            centro_salud = request.POST.get('centro_salud')
            data= {
                "name": nombres + " " + apellidos,
                "groups": [obtener_token_embarazadas()],
                "urns": [],
                "fields": {
                    'nombre': nombres,
                    'apellido': apellidos,
                    'edad': edad,
                    'etnia': etnia,
                    'semana_de_embarazo': semana_embarazo,
                    'region': region,
                    'municipio': municipio,
                    'centro_de_salud': centro_salud,
                    'comunidad': comunidad,
                    'cedula': cedula
                }
            }
            try:
                client.create_contact(name=data["name"], language=None, urns=None, fields=data["fields"], groups=data["groups"])
                message = {'status':True, 'mensaje': 'Excelente! Datos ingresados satisfactoriamente.'}
            except expression as identifier:
                message = {'status':False,'mensaje': 'Ha ocurrido un error'}
                
            return HttpResponse(json.dumps(message), content_type =  "application/json")

class ajax_actualizar_embarazadas(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            client = connect_to_client()
            e_id = request.POST.get('e_id')
            
            fields = {}
            if request.POST.get('nombre') is not None:
                fields.update({'nombre': request.POST.get('nombre')})
            elif request.POST.get('apellido') is not None:
                fields.update({'apellido': request.POST.get('apellido')})
            elif request.POST.get('edad') is not None:
                fields.update({'edad': request.POST.get('edad')})
            elif request.POST.get('cedula') is not None:
                fields.update({'cedula': request.POST.get('cedula')})
            elif request.POST.get('semana_embarazo') is not None:
                fields.update({'semana_de_embarazo': request.POST.get('semana_embarazo')})
            elif request.POST.get('etnia') is not None:
                fields.update({'etnia': request.POST.get('etnia')})
            
            try:
                client.update_contact(e_id, language=None, urns=None, fields=fields)
                message = {'status':True, 'mensaje': 'Excelente! Datos ingresados satisfactoriamente.'}
            except expression as identifier:
                message = {'status':False,'mensaje': 'Ha ocurrido un error'}
                
            return HttpResponse(json.dumps(message), content_type =  "application/json")
            
##########################################################################################################################

def agregar_brigadista(request):
    return render(request, 'admin/agregar_brigadista.html')

def modificar_brigadista(request):
    client = connect_to_client()
    lista_de_brigadistas = client.get_contacts(group=obtener_token_brigadistas())
    print(lista_de_brigadistas.all())
    contexto = {
        'lista_de_brigadistas': lista_de_brigadistas.all()
    }
    return render(request, 'admin/modificar_brigadista.html', context = contexto)

class ajax_agregar_brigadista(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            client = connect_to_client()
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            cedula = request.POST.get('cedula')
            etnia = request.POST.get('etnia')
            region = request.POST.get('region')
            municipio = request.POST.get('municipio')
            comunidad = request.POST.get('comunidad')
            centro_salud = request.POST.get('centro_salud')
            sector = request.POST.get('sector')
            sexo = request.POST.get('sexo')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            escolaridad = request.POST.get('escolaridad')
            ocupacion = request.POST.get('ocupacion')
            funcion_sistema_salud = request.POST.get('funcion_sistema_salud')
            anios_sistema_salud = request.POST.get('anios_sistema_salud')
            celular_personal = request.POST.get('celular_personal')
            celular_asignado = request.POST.get('celular_asignado')
            data= {
                "name": nombres + " "  + apellidos,
                "groups": [obtener_token_brigadistas()],
                "urns": [],
                "fields": {
                    'nombre': nombres,
                    'apellido': apellidos,
                    'etnia': etnia,
                    'region': region,
                    'municipio': municipio,
                    'centro_de_salud': centro_salud,
                    'comunidad': comunidad,
                    'cedula': cedula,
                    'sector': sector,
                    'sexo': sexo,
                    'fecha_de_nacimiento': fecha_nacimiento,
                    'escolaridad': escolaridad,
                    'ocupacion': ocupacion,
                    'funcion_en_el_sistema_de_salud': funcion_sistema_salud,
                    'anios_en_el_sistema_de_salud': anios_sistema_salud,
                    'celular_personal': celular_personal,
                    'celular_asignado': celular_asignado
                }
            }
            print("136")
            try:
                client.create_contact(name=data["name"], language=None, urns=None, fields=data["fields"], groups=data["groups"])
                message = {'status':True, 'mensaje': 'Excelente! Datos ingresados satisfactoriamente.'}
            except expression as identifier:
                message = {'status':False,'mensaje': 'Ha ocurrido un error'}
                
            return HttpResponse(json.dumps(message), content_type =  "application/json")
            

class ajax_actualizar_brigadista(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            client = connect_to_client()
            b_id = request.POST.get('b_id')
            nombre = request.POST.get('nombre')
            
            fields = {}
            if request.POST.get('nombre') is not None:
                fields.update({'nombre': nombre})
            elif request.POST.get('apellido') is not None:
                fields.update({'apellido': request.POST.get('apellido')})
            elif request.POST.get('ocupacion') is not None:
                fields.update({'ocupacion': request.POST.get('ocupacion')})
            elif request.POST.get('cedula') is not None:
                fields.update({'cedula': request.POST.get('cedula')})
            elif request.POST.get('escolaridad') is not None:
                fields.update({'escolaridad': request.POST.get('escolaridad')})
            elif request.POST.get('funcion_sistema') is not None:
                fields.update({'funcion_en_el_sistema_de_salud': request.POST.get('funcion_sistema')})
            elif request.POST.get('anios_sistema') is not None:
                fields.update({'anios_en_el_sistema_de_salud': request.POST.get('anios_sistema')})
            elif request.POST.get('celular_asignado') is not None:
                fields.update({'celular_asignado': request.POST.get('celular_asignado')})
            elif request.POST.get('celular_personal') is not None:
                fields.update({'celular_personal': request.POST.get('celular_personal')})
            elif request.POST.get('etnia') is not None:
                fields.update({'etnia': request.POST.get('etnia')})
            
            try:
                client.update_contact(b_id, language=None, urns=None, fields=fields)
                message = {'status':True, 'mensaje': 'Excelente! Datos ingresados satisfactoriamente.'}
            except expression as identifier:
                message = {'status':False,'mensaje': 'Ha ocurrido un error'}
                
            return HttpResponse(json.dumps(message), content_type =  "application/json")

##########################################################################################################

def monitoreo_durante_embarazo(request, id):
    client = connect_to_client()
    #client.create_broadcast(text="asdvsadva", contacts=["53eaed2e-6f76-4c11-b3b5-f2ea9ec139cc"])
    
    embarazada = client.get_contacts(uuid=id)
    contexto = {
        'embarazada': embarazada.first()
    }
    return render(request, 'admin/monitoreo_embarazo.html', context=contexto)

class monitoreo_durante_embarazo_post(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            print("entro al post")
            client = connect_to_client()
            respuestas = [
                request.POST.get('res_radio_1'),
                request.POST.get('res_radio_2'),
                request.POST.get('res_radio_3'),
                request.POST.get('res_radio_4'),
                request.POST.get('res_radio_5'),
                request.POST.get('res_radio_6'),
                request.POST.get('res_radio_7')
            
            ]
            
            if any(respuesta == "si" for respuesta in respuestas):
                nombre_embarazada = request.POST.get('nombre_embarazada')
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " tiene problemas con el embarazo.", contacts=["53eaed2e-6f76-4c11-b3b5-f2ea9ec139cc"])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")


##########################################################################################################

def monitoreo_salida_comunidad(request, id):
    client = connect_to_client()
    embarazada = client.get_contacts(uuid=id)
    contexto = {
        'embarazada': embarazada.first()
    }
    return render(request, 'admin/monitoreo_salida_comunidad.html', context=contexto)

    
class monitoreo_salida_comunidad_post(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            client = connect_to_client()
            respuesta = request.POST.get('res_radio_1')
            print(request.POST)
            nombre_embarazada = request.POST.get('nombre_embarazada')
            if respuesta == "no":
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " no se presento al centro de salud.", contacts=["53eaed2e-6f76-4c11-b3b5-f2ea9ec139cc"])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            return HttpResponse(json.dumps(message), content_type =  "application/json")

##########################################################################################################

def monitoreo_durante_parto(request, id):
    client = connect_to_client()
    embarazada = client.get_contacts(uuid=id)
    contexto = {
        'embarazada': embarazada.first()
    }
    return render(request, 'admin/monitoreo_durante_parto.html', context=contexto)

class monitoreo_durante_parto_post(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            print("entro al post")
            client = connect_to_client()
            respuestas = [
                request.POST.get('res_radio_1'),
                request.POST.get('res_radio_2'),
                request.POST.get('res_radio_3'),
                request.POST.get('res_radio_4'),
                request.POST.get('res_radio_5'),
                request.POST.get('res_radio_6')
            
            ]
            
            if any(respuesta == "si" for respuesta in respuestas):
                nombre_embarazada = request.POST.get('nombre_embarazada')
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " tiene problemas con el parto.", contacts=["53eaed2e-6f76-4c11-b3b5-f2ea9ec139cc"])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")


##########################################################################################################

def monitoreo_postparto_madre(request, id):
    client = connect_to_client()
    embarazada = client.get_contacts(uuid=id)
    contexto = {
        'embarazada': embarazada.first()
    }
    return render(request, 'admin/monitoreo_postparto_madre.html', context=contexto)
    
class monitoreo_postparto_madre_post(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            print("entro al post")
            client = connect_to_client()
            respuestas = [
                request.POST.get('res_radio_1'),
                request.POST.get('res_radio_2'),
                request.POST.get('res_radio_3'),
                request.POST.get('res_radio_4'),
                request.POST.get('res_radio_5'),
                request.POST.get('res_radio_6')
            
            ]
            
            if any(respuesta == "si" for respuesta in respuestas):
                nombre_embarazada = request.POST.get('nombre_embarazada')
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " tiene problemas postparto.", contacts=["53eaed2e-6f76-4c11-b3b5-f2ea9ec139cc"])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")

##########################################################################################################

def monitoreo_postparto_hijo(request, id):
    client = connect_to_client()
    embarazada = client.get_contacts(uuid=id)
    contexto = {
        'embarazada': embarazada.first()
    }
    return render(request, 'admin/monitoreo_postparto_hijo.html', context=contexto)
    

class monitoreo_postparto_hijo_post(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            print("entro al post")
            client = connect_to_client()
            respuestas = [
                request.POST.get('res_radio_1'),
                request.POST.get('res_radio_2'),
                request.POST.get('res_radio_3'),
                request.POST.get('res_radio_4'),
                request.POST.get('res_radio_5'),
                request.POST.get('res_radio_6'),
                request.POST.get('res_radio_7'),
                request.POST.get('res_radio_8'),
                request.POST.get('res_radio_9')
            
            ]
            
            if any(respuesta == "si" for respuesta in respuestas):
                nombre_embarazada = request.POST.get('nombre_embarazada')
                client.create_broadcast(text="El hijo de la embarazada con nombre " + nombre_embarazada + " tiene problemas postparto.", contacts=["53eaed2e-6f76-4c11-b3b5-f2ea9ec139cc"])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")
