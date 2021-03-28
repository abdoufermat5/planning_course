from django.db import models


# Create your models here.
class Etudiant(models.Model):
	nom = models.CharField(max_length=50)
	prenom = models.CharField(max_length=50)
	sexe = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')],
	                        default='Femme')
	telephone = models.CharField(max_length=12)
	email = models.EmailField()
	
	def __str__(self):
		return self.prenom + ' ' + self.nom


class Cours(models.Model):
	nom = models.CharField(max_length=50, blank=True)
	professeur = models.CharField(max_length=255)
	nombre_seances = models.PositiveIntegerField(default=100)
	
	def __str__(self):
		return self.nom


class Progression(models.Model):
	cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
	etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
	etat_avancement = models.PositiveIntegerField(default=0)


class Calendrier(models.Model):
	jours = models.CharField(max_length=15,
	                         choices=[('Lundi', 'Lundi'),
	                                  ('Mardi', 'Mardi'),
	                                  ('Mercredi', 'Mercredi'),
	                                  ('Jeudi', 'Jeudi'),
	                                  ('Vendredi', 'Vendredi'),
	                                  ('Samedi', 'Samedi'),
	                                  ('Dimanche', 'Dimanche')],
	                         default='Lundi',
	                         blank=True)
	
	def __str__(self):
		return self.jours


class Schedule(models.Model):
	etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
	calendrier = models.ForeignKey(Calendrier, on_delete=models.CASCADE)
	nx = models.PositiveIntegerField(null=True)
	semaine = models.PositiveSmallIntegerField(null=True)
