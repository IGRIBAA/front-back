# Generated by Django 5.2.3 on 2025-06-13 11:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0003_alter_aidant_telephone'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom du champ')),
                ('field_type', models.CharField(choices=[('text', 'Texte'), ('date', 'Date'), ('number', 'Nombre'), ('file', 'Fichier'), ('select', 'Liste déroulante')], default='text', max_length=50, verbose_name='Type de champ')),
                ('value', models.JSONField(blank=True, null=True, verbose_name='Valeur')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentationCohorte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom de la cohorte')),
                ('start_date', models.DateField(verbose_name='Date de début de la cohorte')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Date de fin de la cohorte')),
            ],
        ),
        migrations.CreateModel(
            name='CustomFieldOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Option')),
                ('custom_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='gestion.customfield')),
            ],
        ),
        migrations.CreateModel(
            name='NewExperimentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name="Nom de l'expérimentation")),
                ('partner_company', models.CharField(max_length=255, verbose_name='Entreprise partenaire')),
                ('start_date', models.DateField(verbose_name='Date de début')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Date de fin (prévue ou effective)')),
                ('contact_name', models.CharField(max_length=255, verbose_name='Nom du contact')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('contact_phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', message='Le numéro doit contenir exactement 10 chiffres.')], verbose_name='Téléphone')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Remarques')),
                ('beneficiaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_experimentations', to='gestion.beneficiaire')),
                ('cohorts', models.ManyToManyField(to='gestion.experimentationcohorte', verbose_name='Cohortes')),
                ('custom_fields', models.ManyToManyField(blank=True, to='gestion.customfield', verbose_name='Champs personnalisés')),
            ],
        ),
    ]
