from django.shortcuts import render, get_object_or_404
from .models import Hospital, Doctor
from accounts.models import UserProfile
from django.contrib.auth.models import User

def hospital_list(request, id):
    instance = get_object_or_404(Hospital, id=id)
    doctors = instance.doctor.all()

    context = {
        'instance': instance,
        'list': list,
        'doctors': doctors,
    }
    for doctor in doctors:
        print(doctor.username)
    return render(request, 'hospitals/hospital_page.html', context)


def doctor(request):

    return render(request, 'hospitals/page.html')
