from .models import Patient
from .forms import StoryForm
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User



def about(request):

    return render(request, 'patient/about.html')


def story_list(request):
    user = request.user
    print(user)
    story = Patient.objects.get(user=user)

    query = request.GET.get("q") #for search
    if query:
        story = story.filter(
                Q(disease_name__icontains=query)|
                Q(doctor_name__icontains=query)|
                Q(content__icontains=query)|
                Q(publish__icontains=query)
                ).distinct()




    context = {'story': story}

    return render(request, 'patient/profile.html', context)



def story_create(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = StoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('/')
    else:
        form = StoryForm()
    context = { 'form': form }
    return render(request, 'patient/story_create.html', context)


def story_detail(request, slug=None):
    instance = get_object_or_404(Patient, slug=slug)

    context = {
        'instance': instance,
    }

    return render(request, 'patient/story_detail.html', context)



def story_update(request, slug=None):
    instance = get_object_or_404(Patient, slug=slug)
    form = StoryForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/")
    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, "patient/story_create.html", context)



def story_delete(request, slug=None):
    instance = get_object_or_404(Patient, slug=slug)
    instance.delete()
    return redirect("/")


