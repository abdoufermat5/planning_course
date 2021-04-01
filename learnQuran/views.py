from math import ceil

from django.shortcuts import render, redirect
import random
from itertools import combinations

from .models import *
from datetime import datetime


def week_of_month(dt):
	""" Returns the week of the month for the specified date.
	"""
	
	first_day = dt.replace(day=1)
	
	dom = dt.day
	adjusted_dom = dom + first_day.weekday()
	
	return int(ceil(adjusted_dom / 7.0)) - 1


# Create your views here.
def accueil(request):
	first_day = datetime.weekday(datetime(2021, 4, 1))
	s = { 0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche' }
	if datetime.now() < datetime(2021, 4, 1):
		week = week_of_month(datetime(2021, 4, 1))
		weekday = s.get(datetime.weekday(datetime(2021, 4, 1)))
	else:
		week = week_of_month(datetime.now())
		
		weekday = s.get(datetime.weekday(datetime.now()))
	
	l = Etudiant.objects.all()
	res = []
	try:
		etudiants = Schedule.objects.filter(calendrier=Calendrier.objects.get(jours=weekday), semaine=week)
		res = random.sample(list(etudiants), 2)
	except:
		pass
	return render(request, 'learnQuran/index.html', context={ 'stud': res, 'liste_etudiant': l })


def get_calendar(request):
	calend = Schedule.objects.all()
	s = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
	first_day = datetime.weekday(datetime(2021, 4, 1))
	fisrt_sem = s[first_day:]
	semaine = [0, 1, 2, 3, 4]
	globals = []
	for sem in semaine:
		liste_1 = { }
		liste_2 = { }
		if sem == 0:
			for d in fisrt_sem:
				by_eek = [r for r in calend if r.calendrier.jours == d and r.semaine == sem]
				try:
					liste_1[d] = (by_eek[0])
					liste_2[d] = (by_eek[1])
				except:
					pass
		else:
			for d in s:
				by_eek = [r for r in calend if r.calendrier.jours == d and r.semaine == sem]
				try:
					liste_1[d] = (by_eek[0])
					liste_2[d] = (by_eek[1])
				except:
					pass
		calendrier = [liste_1, liste_2]
		globals.append([sem + 1, calendrier])
	return render(request, 'learnQuran/calendar.html', { 'global': globals, 'content': calend })


def add_calendar(request):
	semaine = [0, 1, 2, 3, 4]
	l = Etudiant.objects.all()
	calendars = Calendrier.objects.all()
	Schedule.objects.all().delete()
	if calendars.count() == 0:
		s = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
		r = []
		for x in s:
			r.append(Calendrier(jours=x))
		Calendrier.objects.bulk_create(r)
	for sem in semaine:
		e = list(combinations(l, 2))
		random.shuffle(e)
		n = Schedule.objects.all().count() // 2
		for jours in calendars:
			new_pair = []
			hasard = random.choice(e)
			while Schedule.objects.filter(etudiant=hasard[0], semaine=sem).count() >= 2 or Schedule.objects.filter(
					etudiant=hasard[1], semaine=sem).count() >= 2:
				hasard = random.choice(e)
			for elt in hasard:
				new_pair.append(Schedule(calendrier=jours, etudiant=elt, nx=n, semaine=sem))
			Schedule.objects.bulk_create(new_pair)
			n += 1
	
	# for c in calendars:
	#     cond = False
	#     res = []
	#
	# while not cond:
	#     if len(e) > 0:
	#         r = list(e.pop())
	#     else:
	#         e = list(combinations(l, 2))
	#         random.shuffle(e)
	#         r = list(e.pop())
	#     for elt in r:
	#         if Schedule.objects.filter(etudiant=elt, semaine=n // 7).count() >= 2\
	#                 or Schedule.objects.filter(etudiant=elt, semaine=n // 7, nx=n).count() == 2:
	#             cond = False
	#             break
	#         else:
	#             res.append(Schedule(etudiant=elt, calendrier=c, nx=n, semaine=n // 7))
	#             cond = True
	# Schedule.objects.bulk_create(res)
	# n += 1
	return redirect('learnQuran:calendar')


def add_student(request, context={ }):
	liste_etudiant = Etudiant.objects.all()
	context['liste_etudiant'] = liste_etudiant
	return render(request, 'learnQuran/add.html', context)


def add(request):
	n_stud = Etudiant(prenom=request.POST['first_name'],
	                  nom=request.POST['last_name'],
	                  sexe=request.POST['sexe'])
	if request.POST['phone']:
		n_stud.telephone = request.POST['phone']
	if request.POST['email']:
		n_stud.email = request.POST['email']
	n_stud.save()
	message = 'étudiant ajouté avec succès'
	liste_etudiant = Etudiant.objects.all()
	context = { 'message': message, 'liste_etudiant': liste_etudiant }
	response = add_student(request, context)
	return response


def deleteAll(request):
	Etudiant.objects.all().delete()
	Schedule.objects.all().delete()
	l = Etudiant.objects.all()
	res = []
	try:
		res = random.sample(list(l), 2)
	except:
		pass
	return render(request, 'learnQuran/index.html', context={ 'stud': res, 'all': l })


def delete_one(request, id):
	et = Etudiant.objects.get(id=id)
	et.delete()
	liste_etudiant = Etudiant.objects.all()
	messaged = 'supprimé avec succès'
	context = { 'message': messaged, 'liste_etudiant': liste_etudiant }
	response = add_student(request, context)
	return response


def delete_calendar(request):
	Schedule.objects.all().delete()
	return redirect('learnQuran:calendar')
