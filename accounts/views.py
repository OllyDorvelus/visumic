from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
#from profiles.models import Userprofile
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, DetailView, ListView, FormView
from .forms import UserLoginForm, UserForm, UserEditForm, UserRegisterForm
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from videos.models import VideoModel
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib import messages
from videos.forms import ShareEditForm
from accounts.tasks import add
add.delay(3,2)

from django.core.exceptions import ValidationError

User = get_user_model()



class UserRegisterFormView(View):
    template_name = 'accounts/registermodal.html'
    form_class = UserRegisterForm
    #success_url = '/'


    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:home')
        return render(request, 'accounts/registermodal.html', {})



    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            #new_user = form.save(commit=False)

            # clearned (normalized) data
            if request.is_ajax:
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                new_user = User.objects.create(username=username, email=email)
                new_user.set_password(password)
                new_user.save()
                login(self.request, new_user)

            #userprofile = Userprofile(user=user)
            #userprofile.save()

            #returns User objects if credentials are correct

                user = authenticate(username=username, password=password)

                if user is not None:

                    if user.is_active:
                        login(request, user)
                        return redirect('accounts:home')
       # return render(request, "home/base.html", {})
        else:
            if request.is_ajax:
               # print(form.is_valid())   #form contains data and errors
                #print(form.errors)
                print(form.errors.as_json())
                errors = form.errors.as_json()
               # errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return HttpResponse(errors, content_type='application/json')
            return JsonResponse(success=False, data=errors)
            return render(request, self.template_name, {'form': form, 'errors': errors})

    def get_context_data(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = super(UserRegisterFormView, self).get_context_data(request, *args, **kwargs)
        context['errors'] = form.errors.as_json()
        # if form.is_valid():
        #     context['valid'] = True
        return context


class UserLoginFormView(View):
    form_class = UserLoginForm
    template_name = "base.html"

    def get(self, request):
        # if not request.user.is_authenticated:
        #     form = self.form_class(None)
        #     return render(request, self.template_name, {'form': form})
        # else:
        #     return redirect("accounts:home")
        if self.request.user.is_authenticated:
            return redirect('accounts:home')
        return render(request, 'accounts/loginmodal.html', {})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username2']
        password = request.POST['password']

        if request.is_ajax:
            try:
                user = User.objects.get(username__iexact=username)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                #return HttpResponseRedirect(request.POST.get('next', reverse('accounts:home')))
                #return HttpResponseRedirect(self.request.GET.get('next'))
                return redirect("accounts:home")

            else:
                if not user or not user.is_active:
                    errors = form.errors.as_json()
                    return HttpResponse(errors, content_type='application/json')
                    return HttpResponseRedirect(self.request.GET.get('next'))
                    #return redirect("accounts:login")

class UserDetailView(DetailView):
    template_name = "accounts/profile_detail.html"
    queryset = User.objects.all()
    context_object_name = 'User'

    def get_object(self):

        user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return user

    def get_context_data(self, *args, **kwargs):
        #user = super(UserDetailView, self).get_object(self, *args, **kwargs)
        user = UserDetailView.get_object(self)
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        context['all_videos'] = VideoModel.objects.filter(user=user)
        return context

class UserDetailFollowerView(DetailView):
    template_name = "accounts/profile_detail_followers.html"
    queryset = User.objects.all()
    context_object_name = "User"

    def get_object(self):
        user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return user

class UserDetailFollowingView(DetailView):
    template_name = "accounts/profile_detail_following.html"
    queryset = User.objects.all()
    context_object_name = "User"

    def get_object(self):
        user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return user

class UserDetailPlayListView(DetailView):
    template_name = "accounts/profile_detail_playlist.html"
    queryset = User.objects.all()
    context_object_name = "User"

    def get_object(self):
        user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return user


class UserDetailLikedView(DeleteView):
    template_name = "accounts/profile_detail_liked.html"
    queryset = User.objects.all()
    context_object_name = "User"

    def get_object(self):
        user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return user

class UserDetailSharedView(DetailView):
    template_name = "accounts/profile_detail_shared.html"
    queryset = User.objects.all()
    context_object_name = "User"

    def get_object(self):
        user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return user

class ProfileListView(ListView):
    template_name = 'accounts/profile_list.html'
    context_object_name = 'all_profiles'
    # paginate_by = 10

    def get_queryset(self):
        return UserProfile.objects.all()

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Publisher.objects.all())
    #     return super(PublisherDetail, self).get(request, *args, **kwargs)


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    template_name = "accounts/profile_edit.html"
    model = UserProfile
    fields = ['first_name', 'last_name', 'user_img', 'bio', 'profile_banner']
    context_object_name = 'someuser'





    def get_object(self, *args, **kwargs):
        #user = get_object_or_404(User, username__iexact=self.kwargs.get("username")):
            user = UserProfile.objects.get(user=self.request.user.pk)
            return user


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:home")
        else:
            return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileUpdateView, self).get_context_data(**kwargs)
    #     context['second_model'] = UserEditForm#whatever you would like
    #     return context
    # def form_valid(self, form):
    #
    #     return self.render_to_response(self.get_context_data(form=form))
class UserUpdateView(UpdateView, LoginRequiredMixin):
    template_name = "accounts/account_edit.html"
    model = User
    # fields = ['username', 'email']
    form_class = UserEditForm
    #context_object_name = "someaccount"


    def get_object(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:home")
        else:
            return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('accounts:account_update')

    def form_valid(self, form, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Profile Updated!')
        return super(UserUpdateView, self).form_valid(form, *args, **kwargs)








def home(request):
    return render(request, "index.html", {})

def social(request):
    share_edit_form = ShareEditForm
    share_edit_url = reverse_lazy("accounts:home")
    context = {'share_edit_form': share_edit_form, 'share_edit_url': share_edit_url}
    return render(request, "social.html", context)


# class Social(View):
#     template_name = 'social.html'
#
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'social.html', {})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next'))
   # return redirect('accounts:home')



class UserFormView(FormView):
    form_class = UserRegisterForm
    template_name = 'base.html'

    # display blank form
    def get(self, request):
        if not request.user.is_authenticated:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('accounts:home')

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserFormView, self).form_valid(form)

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clearned (normalized) data

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # userprofile = UserProfile(user=user)
            # userprofile.save()

            #returns User objects if credentials are correct

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect("accounts:home")

        return render(request, self.template_name, {'form': form})