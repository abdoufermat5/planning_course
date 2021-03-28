# Generated by Django 3.1.7 on 2021-03-28 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnQuran', '0004_auto_20210328_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendrier',
            name='end',
        ),
        migrations.RemoveField(
            model_name='calendrier',
            name='start',
        ),
        migrations.AlterField(
            model_name='calendrier',
            name='jours',
            field=models.CharField(blank=True, choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'), ('Dimanche', 'Dimanche')], default='Lundi', max_length=15),
        ),
    ]
