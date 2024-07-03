# Generated by Django 5.0.6 on 2024-06-25 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.BigIntegerField(blank=True, db_column='ITEM', null=True)),
                ('proveedor', models.TextField(blank=True, db_column='PROVEEDOR', null=True)),
                ('descripción', models.TextField(blank=True, db_column='DESCRIPCIÓN', null=True)),
                ('sede', models.TextField(blank=True, db_column='SEDE', null=True)),
                ('mayo', models.BigIntegerField(blank=True, db_column='MAYO', null=True)),
                ('junio', models.BigIntegerField(blank=True, db_column='JUNIO', null=True)),
                ('julio', models.BigIntegerField(blank=True, db_column='JULIO', null=True)),
                ('agosto', models.BigIntegerField(blank=True, db_column='AGOSTO', null=True)),
                ('septiembre', models.BigIntegerField(blank=True, db_column='SEPTIEMBRE', null=True)),
                ('octubre', models.BigIntegerField(blank=True, db_column='OCTUBRE', null=True)),
                ('noviembre', models.BigIntegerField(blank=True, db_column='NOVIEMBRE', null=True)),
                ('diciembre', models.BigIntegerField(blank=True, db_column='DICIEMBRE', null=True)),
                ('enero', models.BigIntegerField(blank=True, db_column='ENERO', null=True)),
                ('febrero', models.BigIntegerField(blank=True, db_column='FEBRERO', null=True)),
                ('marzo', models.BigIntegerField(blank=True, db_column='MARZO', null=True)),
                ('abril', models.BigIntegerField(blank=True, db_column='ABRIL', null=True)),
                ('total', models.BigIntegerField(blank=True, db_column='TOTAL', null=True)),
                ('promedio', models.FloatField(blank=True, db_column='PROMEDIO', null=True)),
            ],
            options={
                'db_table': 'productos',
                'managed': False,
            },
        ),
    ]
