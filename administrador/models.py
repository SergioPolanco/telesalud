# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Region(models.Model):
    class Meta():
        db_table = "region"
    
    nombre = models.CharField(max_length = 100, null = False)
    def __unicode__(self):
        return self.nombre
        
class CentroDeSalud(models.Model):
    class Meta():
        db_table = "centros_de_salud"
    
    nombre = models.CharField(max_length = 200, null = False)
    telefono = models.CharField(max_length = 30, null = False)
    operadora = models.CharField(max_length = 30, null = False)
    region = models.ForeignKey(Region)
    
    def __unicode__(self):
        return self.nombre


class Municipio(models.Model):
    class Meta():
        db_table = "municipios"
    
    nombre = models.CharField(max_length = 200, null = False)
    telefono = models.CharField(max_length = 30, null = False)
    operadora = models.CharField(max_length = 30, null = False)
    centro_de_salud = models.ForeignKey(CentroDeSalud)
    
    def __unicode__(self):
        return self.nombre

class Comunidad(models.Model):
    class Meta():
        db_table = "comunidades"
    
    nombre = models.CharField(max_length = 200, null = False)
    telefono = models.CharField(max_length = 30, null = False)
    operadora = models.CharField(max_length = 30, null = False)
    municipio = models.ForeignKey(Municipio)
    
    def __unicode__(self):
        return self.nombre


class LlaveValor(models.Model):
    class Meta():
        db_table = "llave_valor"
    
    llave = models.CharField(max_length=100, null=False)
    valor = models.CharField(max_length=200, null=False)
    
    def __unicode__(self):
        return self.llave + ": " + self.valor