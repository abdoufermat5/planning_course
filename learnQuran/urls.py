from . import views
from django.urls import path


app_name = 'learnQuran'
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('calendrier', views.get_calendar, name='calendar'),
    path('calendrier_delete', views.delete_calendar, name='delete_calendrier'),
    path('add_calendar', views.add_calendar, name='add_calendar'),
    path('add', views.add_student, name='add'),
    path('add_student', views.add, name='add_student'),
    path('delete', views.deleteAll, name='delete'),
    path('delete_one/<int:id>', views.delete_one, name='delete_one'),
]