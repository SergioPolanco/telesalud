# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests 
import json
import pandas as pd
from StringIO import StringIO
import xlsxwriter
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from temba_client.v2 import TembaClient
from django.core.urlresolvers import reverse
from django.core.files import File
from unicef_app.connect_to_rapidpro import connect_to_client, TOKEN_BRIGADISTA, TOKEN_EMBARAZADA
from .models import Region, CentroDeSalud, Municipio, Comunidad, LlaveValor, PuestoDeSalud
import collections
from unicef_app import settings
# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')

###################################################################
@login_required
def agregar_embarazada(request):
    comunidades = Comunidad.objects.all()
    contexto = {
        "comunidades": comunidades
    }
    return render(request, 'admin/agregar_embarazada.html', context = contexto)

@login_required
def modificar_embarazada(request):
    client = connect_to_client()
    lista_de_embarazadas = client.get_contacts(group=TOKEN_EMBARAZADA)
    query_list = [embarazada.name for embarazada in lista_de_embarazadas.all() if "alvarez" in embarazada.fields["apellido"].lower() ]
    comunidades = Comunidad.objects.all()
    comunidades = [{ "id": comunidad.id, "text": comunidad.nombre} for comunidad in comunidades ]
    contexto = {
        'lista_de_embarazadas': lista_de_embarazadas.all(),
        "comunidades": json.dumps(comunidades)
    }
    return render(request, 'admin/modificar_embarazada.html', context = contexto)

@login_required
def vista_filtrar_embarazada(request):
    print(request.method)
    comunidades = Comunidad.objects.all()
    municipios = Municipio.objects.all()
    centros_de_salud = CentroDeSalud.objects.all()
    regiones = Region.objects.all()
    puestos_de_salud = PuestoDeSalud.objects.all()
    if request.method == "GET":
        
        contexto = {
            "comunidades": comunidades,
            "municipios": municipios,
            "centros_de_salud": centros_de_salud,
            "regiones": regiones,
            "puestos_de_salud": puestos_de_salud
        }
        return render(request, 'admin/filtrar_embarazada.html', context=contexto)
    else:
        lista_de_embarazadas = filtrar(request.POST)
        contexto = {
            "comunidades": comunidades,
            "municipios": municipios,
            "centros_de_salud": centros_de_salud,
            "regiones": regiones,
            "puestos_de_salud": puestos_de_salud,
            'lista_de_embarazadas': lista_de_embarazadas
        }
        return render(request, 'admin/filtrar_embarazada.html', context = contexto)
        
@login_required
def exportar_embarazadas_a_excel(request):
    if request.method == "POST":
        print("linea 80")
        data = [embarazada.fields for embarazada in filtrar(request.POST)]
        print("linea 82")
        data = [
            retornar_data_ordenada({
                "Nombre": embarazada["nombre"],
                "Apellido": embarazada["apellido"],
                "Edad": embarazada["edad"],
                "Cedula": embarazada["cedula"],
                "Celular": embarazada["celular_personal"],
                "Centro de Salud": embarazada["centro_de_salud"],
                "Comunidad": embarazada["comunidad"],
                "Region": embarazada["region"],
                "Municipio": embarazada["municipio"],
                "Discapacidad": "Ninguna" if embarazada["discapacidad"] == "ninguna" else embarazada["discapacidad"],
                "Empresa Telefonica": embarazada["empresa_telefonica"],
                "Escolaridad": embarazada["escolaridad"],
                "Nivel de Escolaridad": retornar_nivel_de_escolaridad(embarazada["escolaridad"], embarazada["valor_de_la_escolaridad"]),
                "Etnia": embarazada["etnia"],
                "Numero de Embarazos": embarazada["numero_de_embarazos"],
                "Semana de Embarazo": embarazada["semana_de_embarazo"]
            })
            for embarazada in data
        ]
        print("linea 104")
        sio = StringIO()
        print("entro al post de exportar")
        PandasDataFrame = pd.DataFrame(data)
        PandasWriter = pd.ExcelWriter(sio, engine='xlsxwriter')
        PandasDataFrame.to_excel(PandasWriter, sheet_name="Embarazadas", index=False)
        PandasWriter.save()
        
        sio.seek(0)
        workbook = sio.getvalue()
        
        response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=reporte.xlsx' 
        return response

def retornar_data_ordenada(data):
    print("entro a data ordenada")
    data_ordenada = collections.OrderedDict()
    data_ordenada["Nombre"] = data["Nombre"]
    data_ordenada["Apellido"] = data["Apellido"]
    data_ordenada["Edad"] = data["Edad"]
    data_ordenada["Cedula"] = data["Cedula"]
    data_ordenada["Celular"] = data["Celular"]
    data_ordenada["Empresa Telefonica"] = data["Empresa Telefonica"]
    data_ordenada["Region"] = data["Region"]
    data_ordenada["Centro De Salud"] = data["Centro de Salud"]
    data_ordenada["Municipio"] = data["Municipio"]
    data_ordenada["Comunidad"] = data["Comunidad"]
    data_ordenada["Discapacidad"] = data["Discapacidad"]
    data_ordenada["Escolaridad"] = data["Escolaridad"]
    data_ordenada["Nivel de Escolaridad"] = data["Nivel de Escolaridad"]
    data_ordenada["Etnia"] = data["Etnia"]
    data_ordenada["Numero de Embarazos"] = data["Numero de Embarazos"]
    data_ordenada["Semana de Embarazo"] = data["Semana de Embarazo"]
    return data_ordenada


def retornar_nivel_de_escolaridad(escolaridad, nivel_de_escolaridad):
    print("Nivel de escolaridad")
    if escolaridad == "primaria" or escolaridad == "secundaria":
        valor_escolaridad = LlaveValor.objects.get(llave=nivel_de_escolaridad)
        return valor_escolaridad.valor
    else:
        return nivel_de_escolaridad
        
def filtrar(argumentos):
    client = connect_to_client()
    lista_de_embarazadas = client.get_contacts(group=TOKEN_EMBARAZADA).all()
    print(list(lista_de_embarazadas))
    print(argumentos)
    if argumentos.get("region"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["region"].lower() == x.fields["region"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("municipio"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["municipio"].lower() == x.fields["municipio"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("centro_salud"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["centro_salud"].lower() == x.fields["centro_de_salud"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("comunidad"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["comunidad"].lower() == x.fields["comunidad"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("puestos_de_salud"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["puestos_de_salud"].lower() in x.fields["puesto_de_salud"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("nombres"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["nombres"].lower() in x.fields["nombre"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("apellidos"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["apellidos"].lower() in x.fields["apellido"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("cedula"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["cedula"].lower() == x.fields["cedula"].lower(),
                lista_de_embarazadas
        )
    
    if argumentos.get("etnia"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["etnia"].lower() == x.fields["etnia"].lower(),
                lista_de_embarazadas
        )
    
    if argumentos.get("cedula"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["cedula"].lower() == x.fields["cedula"].lower(),
                lista_de_embarazadas
        )
    
    if argumentos.get("semana_embarazo_desde") and argumentos.get("semana_embarazo_hasta"):
        semanas_de_embarazo_desde = argumentos.get("semana_embarazo_desde")
        semanas_de_embarazo_hasta = argumentos.get("semana_embarazo_hasta")
        print(semanas_de_embarazo_desde)
        print(semanas_de_embarazo_hasta)
        lista_de_embarazadas = filter(
                lambda x: semanas_de_embarazo_desde <= x.fields["semana_de_embarazo"] <= semanas_de_embarazo_hasta,
                lista_de_embarazadas
        )
    elif argumentos.get("semana_embarazo_desde") and not argumentos.get("semana_embarazo_hasta"):
        semanas_de_embarazo_desde = argumentos.get("semana_embarazo_desde")
        semanas_de_embarazo_hasta = argumentos.get("semana_embarazo_desde")
        lista_de_embarazadas = filter(
                lambda x: semanas_de_embarazo_desde <= x.fields["semana_de_embarazo"] <= semanas_de_embarazo_hasta,
                lista_de_embarazadas
        )
    elif not argumentos.get("semana_embarazo_desde") and argumentos.get("semana_embarazo_hasta"):
        semanas_de_embarazo_desde = argumentos.get("semana_embarazo_hasta")
        semanas_de_embarazo_hasta = argumentos.get("semana_embarazo_hasta")
        lista_de_embarazadas = filter(
                lambda x: semanas_de_embarazo_desde <= x.fields["semana_de_embarazo"] <= semanas_de_embarazo_hasta,
                lista_de_embarazadas
        )
    
    if argumentos.get("edad_desde") and argumentos.get("edad_hasta"):
        edad_desde = argumentos.get("edad_desde")
        edad_hasta = argumentos.get("edad_hasta")
        lista_de_embarazadas = filter(
                lambda x:  edad_desde <= x.fields["edad"] <= edad_hasta,
                lista_de_embarazadas
        )
    elif argumentos.get("edad_desde") and not argumentos.get("edad_hasta"):
        edad_desde = argumentos.get("edad_desde")
        edad_hasta = argumentos.get("edad_desde")
        lista_de_embarazadas = filter(
                lambda x:  edad_desde <= x.fields["edad"] <= edad_hasta,
                lista_de_embarazadas
        )
    elif not argumentos.get("edad_desde") and argumentos.get("edad_hasta"):
        edad_desde = argumentos.get("edad_hasta")
        edad_hasta = argumentos.get("edad_hasta")
        lista_de_embarazadas = filter(
                lambda x:  edad_desde <= x.fields["edad"] <= edad_hasta,
                lista_de_embarazadas
        )
    
    if argumentos.get("discapacidad") != 'ninguna':
        print("entro a discapacidad")
        lista_de_embarazadas = filter(
                lambda x: argumentos["discapacidad"].lower() == x.fields["discapacidad"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("escolaridad"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["escolaridad"].lower() == x.fields["escolaridad"].lower(),
                lista_de_embarazadas
        )
    if argumentos.get("numero_de_embarazos"):
        lista_de_embarazadas = filter(
                lambda x: argumentos["numero_de_embarazos"].lower() == x.fields["numero_de_embarazos"].lower(),
                lista_de_embarazadas
        )
    print(list(lista_de_embarazadas))
    return lista_de_embarazadas
        
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
            comunidad = request.POST.get('comunidad')
            escolaridad = request.POST.get('escolaridad')
            valor_escolaridad = request.POST.get('valor_escolaridad')
            discapacidad = request.POST.get('discapacidad')
            numero_de_embarazos = request.POST.get('numero_de_embarazos')
            celular = request.POST.get('celular')
            empresa_telefonica = request.POST.get('empresa_telefonica')
            
            comunidad = Comunidad.objects.get(id=comunidad)
            puesto_de_salud = PuestoDeSalud.objects.get(nombre=comunidad.puesto_de_salud)
            centro_de_salud = CentroDeSalud.objects.get(nombre=puesto_de_salud.centro_de_salud)
            municipio = Municipio.objects.get(nombre=centro_de_salud.municipio)
            region = Region.objects.get(nombre=municipio.region)
            
            data= {
                "name": nombres + " " + apellidos,
                "groups": [TOKEN_EMBARAZADA],
                "urns": [],
                "fields": {
                    'nombre': nombres,
                    'apellido': apellidos,
                    'edad': edad,
                    'etnia': etnia,
                    'semana_de_embarazo': semana_embarazo,
                    'region': region.nombre,
                    'municipio': municipio.nombre,
                    'centro_de_salud': centro_de_salud.nombre,
                    'comunidad': comunidad.nombre,
                    'cedula': cedula,
                    'numero_de_embarazos': numero_de_embarazos,
                    'escolaridad': escolaridad,
                    'valor_de_la_escolaridad': valor_escolaridad,
                    'discapacidad': discapacidad,
                    'celular_personal': celular,
                    'empresa_telefonica': empresa_telefonica,
                    'puesto_de_salud': puesto_de_salud.nombre
                }
            }

            client.create_contact(name=data["name"], language=None, urns=None, fields=data["fields"], groups=data["groups"])
            message = {'status':True, 'mensaje': 'Excelente! Datos ingresados satisfactoriamente.'}
            #message = {'status':False,'mensaje': 'Ha ocurrido un error'}
                
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
            elif request.POST.get('discapacidad') is not None:
                fields.update({'discapacidad': request.POST.get('discapacidad')})
            elif request.POST.get('numero_de_embarazos') is not None:
                fields.update({'etnia': request.POST.get('numero_de_embarazos')})
            elif request.POST.get('empresa_telefonica') is not None:
                fields.update({'empresa_telefonica': request.POST.get('empresa_telefonica')})
            elif request.POST.get('escolaridad') is not None:
                fields.update({'escolaridad': request.POST.get('escolaridad')})
            elif request.POST.get('primaria') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('primaria')})
            elif request.POST.get('secundaria') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('secundaria')})
            elif request.POST.get('tecnico') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('tecnico')})
            elif request.POST.get('universidad') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('universidad')})
            elif request.POST.get('valor_otro') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('valor_otro')})
            elif request.POST.get('celular') is not None:
                fields.update({'celular_personal': request.POST.get('celular')})
            elif request.POST.get('comunidad') is not None:
                comunidad = Comunidad.objects.get(id=request.POST.get('comunidad'))
                puesto_de_salud = PuestoDeSalud.objects.get(nombre=comunidad.puesto_de_salud)
                centro_de_salud = CentroDeSalud.objects.get(nombre=puesto_de_salud.centro_de_salud)
                municipio = Municipio.objects.get(nombre=centro_de_salud.municipio)
                region = Region.objects.get(nombre=municipio.region)

                fields.update({'comunidad': comunidad.nombre})
                fields.update({'municipio': municipio.nombre})
                fields.update({'centro_de_salud': centro_de_salud.nombre})
                fields.update({'region': region.nombre})
                fields.update({'puesto_de_salud': puesto_de_salud.nombre})
            
            try:
                client.update_contact(e_id, language=None, urns=None, fields=fields)
                message = {'status':True, 'mensaje': 'Excelente! Datos ingresados satisfactoriamente.'}
            except expression as identifier:
                message = {'status':False,'mensaje': 'Ha ocurrido un error'}
                
            return HttpResponse(json.dumps(message), content_type =  "application/json")
            
##########################################################################################################################
@login_required
def agregar_brigadista(request):
    comunidades = Comunidad.objects.all()
    contexto = {
        "comunidades": comunidades
    }
    return render(request, 'admin/agregar_brigadista.html', context=contexto)
@login_required
def modificar_brigadista(request):
    client = connect_to_client()
    lista_de_brigadistas = client.get_contacts(group=TOKEN_BRIGADISTA)
    comunidades = Comunidad.objects.all()
    comunidades = [{ "id": comunidad.id, "text": comunidad.nombre} for comunidad in comunidades ]
    contexto = {
        'lista_de_brigadistas': lista_de_brigadistas.all(),
        'comunidades': json.dumps(comunidades)
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
            comunidad = request.POST.get('comunidad')
            sexo = request.POST.get('sexo')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            ocupacion = request.POST.get('ocupacion')
            funcion_sistema_salud = request.POST.get('funcion_sistema_salud')
            anios_sistema_salud = request.POST.get('anios_sistema_salud')
            celular_personal = request.POST.get('celular_personal')
            celular_asignado = request.POST.get('celular_asignado')
            escolaridad = request.POST.get('escolaridad')
            valor_escolaridad = request.POST.get('valor_escolaridad')

            comunidad = Comunidad.objects.get(id=comunidad)
            puesto_de_salud = PuestoDeSalud.objects.get(nombre=comunidad.puesto_de_salud)
            centro_de_salud = CentroDeSalud.objects.get(nombre=puesto_de_salud.centro_de_salud)
            municipio = Municipio.objects.get(nombre=centro_de_salud.municipio)
            region = Region.objects.get(nombre=municipio.region)
            
            data= {
                "name": nombres + " "  + apellidos,
                "groups": [TOKEN_BRIGADISTA],
                "fields": {
                    'nombre': nombres,
                    'apellido': apellidos,
                    'etnia': etnia,
                    'region': region.nombre,
                    'municipio': municipio.nombre,
                    'centro_de_salud': centro_de_salud.nombre,
                    'comunidad': comunidad.nombre,
                    'cedula': cedula,
                    'sexo': sexo,
                    'fecha_de_nacimiento': fecha_nacimiento,
                    'escolaridad': escolaridad,
                    'valor_de_la_escolaridad': valor_escolaridad,
                    'ocupacion': ocupacion,
                    'funcion_en_el_sistema_de_salud': funcion_sistema_salud,
                    'anios_en_el_sistema_de_salud': anios_sistema_salud,
                    'celular_personal': celular_personal,
                    'celular_asignado': celular_asignado,
                    'puesto_de_salud': puesto_de_salud.nombre
                }
            }
            try:
                client.create_contact(name=data["name"], language=None, urns=["tel:+505"+celular_asignado], fields=data["fields"], groups=data["groups"])
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
            elif request.POST.get('sexo') is not None:
                fields.update({'sexo': request.POST.get('sexo')})
            elif request.POST.get('fecha_nacimiento') is not None:
                fields.update({'fecha_de_nacimiento': request.POST.get('fecha_nacimiento')})
            elif request.POST.get('escolaridad') is not None:
                fields.update({'escolaridad': request.POST.get('escolaridad')})
            elif request.POST.get('primaria') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('primaria')})
            elif request.POST.get('secundaria') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('secundaria')})
            elif request.POST.get('tecnico') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('tecnico')})
            elif request.POST.get('universidad') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('universidad')})
            elif request.POST.get('valor_otro') is not None:
                fields.update({'valor_de_la_escolaridad': request.POST.get('valor_otro')})
            elif request.POST.get('comunidad') is not None:
                comunidad = Comunidad.objects.get(id=request.POST.get('comunidad'))
                puesto_de_salud = PuestoDeSalud.objects.get(nombre=comunidad.puesto_de_salud)
                centro_de_salud = CentroDeSalud.objects.get(nombre=puesto_de_salud.centro_de_salud)
                municipio = Municipio.objects.get(nombre=centro_de_salud.municipio)
                region = Region.objects.get(nombre=municipio.region)
                
                fields.update({'comunidad': comunidad.nombre})
                fields.update({'municipio': municipio.nombre})
                fields.update({'centro_de_salud': centro_de_salud.nombre})
                fields.update({'region': region.nombre})
                fields.update({'puesto_de_salud': puesto_de_salud.nombre})
      
            try:
                client.update_contact(b_id, language=None, urns=None, fields=fields)
                message = {'status':True, 'mensaje': 'Excelente! Datos ingresados satisfactoriamente.'}
            except expression as identifier:
                message = {'status':False,'mensaje': 'Ha ocurrido un error'}
                
            return HttpResponse(json.dumps(message), content_type =  "application/json")

##########################################################################################################
@login_required
def monitoreo_durante_embarazo(request, id):
    client = connect_to_client()
    embarazada = client.get_contacts(uuid=id)
    contexto = {
        'embarazada': embarazada.first()
    }
    return render(request, 'admin/monitoreo_embarazo.html', context=contexto)

def enviar_mensaje_de_emergencia(comunidad):
    client = connect_to_client()
    comunidad = Comunidad.objects.get(nombre=comunidad)
    puesto_de_salud = PuestoDeSalud.objects.get(nombre=comunidad.puesto_de_salud)
    puesto_de_salud_rapid_pro = client.get_contacts(urn="tel:+505"+puesto_de_salud.telefono).first()
    return puesto_de_salud_rapid_pro.uuid
    
class monitoreo_durante_embarazo_post(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
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
                comunidad = request.POST.get('comunidad')
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " tiene problemas con el embarazo.", contacts=[enviar_mensaje_de_emergencia(comunidad)])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")


##########################################################################################################
@login_required
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
            nombre_embarazada = request.POST.get('nombre_embarazada')
            comunidad = request.POST.get('comunidad')
            if respuesta == "no":
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " no se presento al centro de salud.", contacts=[enviar_mensaje_de_emergencia(comunidad)])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            return HttpResponse(json.dumps(message), content_type =  "application/json")

##########################################################################################################
@login_required
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
                comunidad = request.POST.get('comunidad')
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " tiene problemas con el parto.", contacts=[enviar_mensaje_de_emergencia(comunidad)])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")


##########################################################################################################
@login_required
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
                comunidad = request.POST.get('comunidad')
                client.create_broadcast(text="La embarazada con nombre " + nombre_embarazada + " tiene problemas postparto.", contacts=[enviar_mensaje_de_emergencia(comunidad)])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")

##########################################################################################################
@login_required
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
                comunidad = request.POST.get('comunidad')
                client.create_broadcast(text="El hijo de la embarazada con nombre " + nombre_embarazada + " tiene problemas postparto.", contacts=[enviar_mensaje_de_emergencia(comunidad)])
                message = {'status':False,'mensaje': 'Se ha notificado al centro de salud'}
            else:
                message = {'status':True,'mensaje': 'Gracias!'}
            
            return HttpResponse(json.dumps(message), content_type =  "application/json")

#################################################################################################

@login_required
def respaldo(request):
    print(settings.DATABASES['default']['NAME'])
    return render(request, 'admin/respaldo.html')

@login_required
def descargar_respaldo(resquest):
    print("entro")
    db_path = settings.DATABASES['default']['NAME']
    dbfile = File(open(db_path, "rb"))
    response = HttpResponse(dbfile, content_type='application/x-sqlite3')
    response['Content-Disposition'] = 'attachment; filename=respaldo_telesalud.sqlite3'
    response['Content-Length'] = dbfile.size

    return response
