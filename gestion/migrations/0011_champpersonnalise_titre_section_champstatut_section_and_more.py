# Generated by Django 5.2.3 on 2025-06-18 20:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0010_usagerri2s_alter_usagerpro_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='champpersonnalise',
            name='titre_section',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='champstatut',
            name='section',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='champstatut',
            name='type_champ',
            field=models.CharField(default='text', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champstatut',
            name='valeurs_possibles',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='usagerpro',
            name='date_creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='usagerpro',
            name='prenom',
            field=models.CharField(default='text', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usagerpro',
            name='profession',
            field=models.CharField(default='text', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usagerpro',
            name='remarques',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='usagerpro',
            name='structure',
            field=models.CharField(default='text', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usagerpro',
            name='telephone',
            field=models.CharField(default='text', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='champpersonnalise',
            name='valeurs_possibles',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='champstatut',
            name='nom_champ',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='usagerpro',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
    ]
