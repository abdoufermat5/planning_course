from math import ceil

from django.shortcuts import render, redirect
import random

from django.urls import reverse

from .models import *
from datetime import datetime


def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))


# Create your views here.
def accueil(request):
    l = Etudiant.objects.all()
    res = []
    try:
        
        etudiants = Schedule.objects.filter(nx=datetime.weekday(datetime.now()))
        res = random.sample(list(etudiants), 2)
    except:
        pass
    return render(request, 'learnQuran/index.html', context={ 'stud': res, 'liste_etudiant': l })


def get_calendar(request):
    calend = Schedule.objects.all()
    s = ['Lundi', 'Mardi','Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
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
        globals.append([sem+1, calendrier])
    return render(request, 'learnQuran/calendar.html', {'global': globals, 'content': calend})


def add_calendar(request):
    semaine = [0, 1, 2, 3, 4]
    l = Etudiant.objects.all()
    calendars = Calendrier.objects.all()
    
    for sem in semaine:
        n = Schedule.objects.all().count() // 2
        for c in calendars:
            for i in range(2):
                e = random.sample(list(l), 1)
                while Schedule.objects.filter(etudiant=e[0], semaine=n//7).count() >= 2:
                    e = random.sample(list(l), 1)
                if Schedule.objects.filter(etudiant=e[0], semaine=n//7).count() <= 2:
                    if Schedule.objects.filter(etudiant=e[0], calendrier=c, nx=n).count() == 0:
                        n_sched = Schedule(etudiant=e[0], calendrier=c, nx=n, semaine=n // 7)
                        n_sched.save()
            n += 1
    return redirect('learnQuran:calendar')


def add_student(request, context={}):
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
    context = {'message': message, 'liste_etudiant': liste_etudiant}
    response = add_student(request, context)
    return response


def deleteAll(request):
    Etudiant.objects.all().delete()
    Calendrier.objects.all().delete()
    Schedule.objects.all().delete()
    Progression.objects.all().delete()
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
    context = {'message': messaged, 'liste_etudiant': liste_etudiant}
    response = add_student(request, context)
    return response


def delete_calendar(request):
    Schedule.objects.all().delete()
    return redirect('learnQuran:calendar')