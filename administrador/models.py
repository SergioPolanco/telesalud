# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from unicef_app.connect_to_rapidpro import connect_to_client, TOKEN_PUESTOS_DE_SALUD, TOKEN_EMBARAZADA

# Create your models here.

class Region(models.Model):
    class Meta():
        db_table = "region"
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'
    
    nombre = models.CharField(max_length = 100, null = False)
    def __unicode__(self):
        return self.nombre
    
class Municipio(models.Model):
    class Meta():
        db_table = "municipios"
    
    nombre = models.CharField(max_length = 200, null = False)
    region = models.ForeignKey(Region)
    def __unicode__(self):
        return self.nombre
        
class CentroDeSalud(models.Model):
    class Meta():
        db_table = "centros_de_salud"
        verbose_name = 'Centro de Salud'
        verbose_name_plural = 'Centros de Salud'
    
    nombre = models.CharField(max_length = 200, null = False)
    telefono = models.CharField(max_length = 30, null = False)
    operadora = models.CharField(max_length = 30, null = False)
    municipio = models.ForeignKey(Municipio)
    
    def __unicode__(self):
        return self.nombre

class PuestoDeSalud(models.Model):
    class Meta():
        db_table = "puestos_de_salud"
        verbose_name = 'Puesto de Salud'
        verbose_name_plural = 'Puestos de Salud'
    
    nombre = models.CharField(max_length = 200, null = False)
    telefono = models.CharField(max_length = 30, null = False)
    operadora = models.CharField(max_length = 30, null = False)
    centro_de_salud = models.ForeignKey(CentroDeSalud)
    
    def __unicode__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        client = connect_to_client()
        data= {
            "name": self.nombre,
            "groups": [TOKEN_PUESTOS_DE_SALUD],
            "urns": [],
            "fields": {
                'nombre': self.nombre,
                'celular_personal': self.telefono,
                'empresa_telefonica': self.operadora,
            }
        }
        client.create_contact(name=data["name"], language=None, urns=["tel:+505"+self.telefono], fields=data["fields"], groups=data["groups"])
        return super(PuestoDeSalud, self).save(*args, **kwargs)

class Comunidad(models.Model):
    class Meta():
        db_table = "comunidades"
        verbose_name = 'Comunidad'
        verbose_name_plural = 'Comunidades'
    
    nombre = models.CharField(max_length = 200, null = False)
    telefono = models.CharField(max_length = 30, null = False)
    operadora = models.CharField(max_length = 30, null = False)
    puesto_de_salud = models.ForeignKey(PuestoDeSalud)
    
    def __unicode__(self):
        return self.nombre


class LlaveValor(models.Model):
    class Meta():
        db_table = "llave_valor"
        verbose_name = 'Llave Valor'
        verbose_name_plural = 'Llaves Valores'
    
    llave = models.CharField(max_length=100, null=False)
    valor = models.CharField(max_length=200, null=False)
    
    def __unicode__(self):
        return self.llave + ": " + self.valor