from django.shortcuts import render,redirect, HttpResponseRedirect, get_object_or_404
from .forms import  EditProfileForm, ChangeBasicInfo, ChangePasswordForm
from django.contrib.auth import login, logout,authenticate, update_session_auth_hash
from .models import UserProfile
from django.views.generic import View
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from patient.models import Patient
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#Login
class Login(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        form = LoginForm()

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        form = LoginForm(request.POST or None)

        if request.POST and form.is_valid():
            user=form.login(request)

            if user:
                login(request, user)
                return HttpResponseRedirect('/')

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)



#Registration
class Registration(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = RegistrationForm()

        variables = {
            'form': form,
        }
        return render(request, self.template_name, variables)

    def post(self, request):
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            user = form.registration(request)
            user.save()
            login(request, user)
            return HttpResponseRedirect('/')

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)




def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')

    else:
        form = EditProfileForm(instance=request.user)

    args = {'form': form}
    return render(request, 'accounts/edit_profile.html', args)




def edit_info(request):
    if request.method == 'POST':
        form = ChangeBasicInfo(request.POST,  request.FILES, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = ChangeBasicInfo(instance=UserProfile.objects.get(user=request.user))

    args = {'form': form}
    return render(request, 'accounts/edit_info.html', args)




def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)

        if form.is_valid():

            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')

    else:
        form = ChangePasswordForm(user=request.user)

    args = {'form': form}
    return render(request, 'accounts/change_password.html', args)




def logout_view(request):
    logout(request)
    return redirect("home")


def profile(request, username):
    user = get_object_or_404(User, username=username)
    userprofile = UserProfile.objects.get(user=user)
    stories = Patient.objects.filter(user=user)

    query = request.GET.get("q")
    if query:
        stories = stories.filter(
                    Q(disease_name__icontains=query)|
                    Q(content__icontains=query)|
                    Q(doctor_name__icontains=query)|
                    Q(publish__icontains=query)
                    ).distinct()

    paginator = Paginator(stories, 2)
    page = request.GET.get('page')
    try:
            queryset = paginator.page(page)
    except PageNotAnInteger:
            queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'userprofile': userprofile,
        'objects': queryset,
    }

    return render(request, 'accounts/profile.html', context)

