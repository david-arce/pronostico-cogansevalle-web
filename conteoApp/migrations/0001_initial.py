# Generated by Django 5.0.6 on 2024-11-27 19:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mcnproduct', models.CharField(blank=True, db_column='MCNPRODUCT', null=True)),
                ('marnombre', models.CharField(blank=True, db_column='MARNOMBRE', null=True)),
                ('pronombre', models.CharField(blank=True, db_column='PRONOMBRE', null=True)),
                ('mcnbodega', models.CharField(blank=True, db_column='MCNBODEGA', null=True)),
                ('docfecha', models.DateField(blank=True, db_column='DOCFECHA', null=True)),
            ],
            options={
                'db_table': 'venta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteo', models.IntegerField(blank=True, null=True)),
                ('fecha_asignacion', models.DateField(auto_now_add=True)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('diferencia', models.IntegerField(blank=True, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conteoApp.venta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tarea',
                'verbose_name_plural': 'Tareas',
                'db_table': 'tarea',
            },
        ),
    ]
