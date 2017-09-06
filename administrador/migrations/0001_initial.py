# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 01:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CentroDeSalud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=30)),
                ('operadora', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'centros_de_salud',
            },
        ),
        migrations.CreateModel(
            name='Comunidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=30)),
                ('operadora', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'comunidades',
            },
        ),
        migrations.CreateModel(
            name='LlaveValor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('llave', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'llave_valor',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'municipios',
            },
        ),
        migrations.CreateModel(
            name='PuestoDeSalud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=30)),
                ('operadora', models.CharField(max_length=30)),
                ('centro_de_salud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.CentroDeSalud')),
            ],
            options={
                'db_table': 'puestos_de_salud',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'region',
            },
        ),
        migrations.AddField(
            model_name='municipio',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Region'),
        ),
        migrations.AddField(
            model_name='comunidad',
            name='puesto_de_salud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.PuestoDeSalud'),
        ),
        migrations.AddField(
            model_name='centrodesalud',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Municipio'),
        ),
    ]
