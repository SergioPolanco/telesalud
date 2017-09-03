# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Region, CentroDeSalud, Municipio, Comunidad, LlaveValor
from django import forms
# Register your models here.

    
admin.site.register(Region)
admin.site.register(CentroDeSalud)
admin.site.register(Municipio)
admin.site.register(Comunidad)
admin.site.register(LlaveValor)

