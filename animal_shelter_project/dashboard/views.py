import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend before importing pyplot
import matplotlib.pyplot as plt
from django.shortcuts import render
from animal_shelter_app.models import Application, Pet
from user_managment_app.models import Shelter
from collections import Counter
import datetime
import numpy as np
import calendar

def dashboard_view(request):
    applications = Application.objects.all()
    pets = Pet.objects.all()

    #Diagram 1:

    months_adopt = []
    months_add = []
    species = []

    for app in applications:
        species.append(app.pet.species)
        month_integer = app.created_at.month
        months_adopt.append(month_integer)

    for p in pets:
        month_integer = p.published_at.month
        months_add.append(month_integer)

    count_adopt = Counter(months_adopt)
    count_add = Counter(months_add)

    print(count_adopt)

    months = [_ for _ in range(1, 13)]
    m_adopt_list = sorted(list(count_adopt.keys()))
    m_add_list = sorted(list(count_adopt.keys()))
    adopt_per_ponth = ()
    add_per_ponth = ()
    count_add_adopt = {}


    for mnth in months:
        if mnth in m_adopt_list:
            adopt_per_ponth += (count_adopt[mnth],)
        else:
            adopt_per_ponth += (0,)

    for mnth in months:
        if mnth in m_add_list:
            add_per_ponth += (count_add[mnth],)
        else:
            add_per_ponth += (0,)

    count_add_adopt = {
    'adopt_per_month': adopt_per_ponth,
    'add_per_month': add_per_ponth
}

    width = 0.6 

    fig, ax = plt.subplots()
    bottom = np.zeros(len(months))

    for k, v in count_add_adopt.items():
        p = ax.bar(months, v, width, label=k, bottom=bottom)
        bottom += v

    ax.bar_label(p, label_type='center')

    ax.set_title('Number of pets by adding and adoption')
    ax.legend()

    plt.savefig('static/dashboard/adoption_chart.png')  
    plt.close()

    # Diagram 2:

    count_species = Counter(species)

    s = [] #species
    q = [] #quantity

    for sp, qt in count_species.items():
        s.append(sp)
        q.append(qt)

    print(count_species)

    plt.figure(figsize=(10, 6))
    plt.pie(q, labels=s, autopct='%.1f%%', startangle=140)
    plt.title('Adopted spieces')
    plt.tight_layout()
    plt.savefig('static/dashboard/species_chart.png')  
    plt.close()


    return render(request, 'dashboard.html')
