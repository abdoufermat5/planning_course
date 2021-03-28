from django.contrib import admin
from .models import *


class EtudiantAdmin(admin.ModelAdmin):
	list_display = ('nom', 'prenom', 'sexe', 'email', 'telephone')


class CoursAdmin(admin.ModelAdmin):
	list_display = ('nom', 'professeur', 'nombre_seances')


class ProgressionAdmin(admin.ModelAdmin):
	list_display = ('etudiant', 'cours', 'etat_avancement')


class CalendrierAdmin(admin.ModelAdmin):
	list_display = ('jours',)


class ScheduleAdmin(admin.ModelAdmin):
	list_display = ('etudiant', 'calendrier', 'semaine', 'nx')


admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(Cours, CoursAdmin)
admin.site.register(Progression, ProgressionAdmin)
admin.site.register(Calendrier, CalendrierAdmin)
admin.site.register(Schedule ,ScheduleAdmin)
# Register your models here.
