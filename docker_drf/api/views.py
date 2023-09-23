from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import LoginForm, AddImageForm
from django.views.generic import ListView
from .models import Image, CustomUser
from django.utils.timezone import now


class IndexHome(ListView):
    model = Image
    template_name = 'api/index.html'
    context_object_name = 'images'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(active=True, published=True).select_related('user_id')
        return queryset


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    if not cd['remember_me']:
                        request.session.set_expiry(0)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Disabled account')
            else:
                messages.warning(request, 'Invalid login')
        else:
            messages.warning(request, 'Invalid login or password')
    else:
        form = LoginForm()
    return render(request, 'api/login.html', {'form': form})


@login_required
def dashboard(request):
    queryset = Image.objects.filter(active=True, user_id=request.user.pk)
    return render(request, 'api/dashboard.html', {'images': queryset})



@login_required
def add_image(request):
    current_user = CustomUser.objects.get(id=request.user.pk)
    if request.method == 'POST':
        img_form = AddImageForm(data=request.POST, files=request.FILES)
        if img_form.is_valid():
            form = img_form.save(commit=False)
            form.user_id = current_user
            form.save()
            messages.success(request, 'Image uploaded successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error uploading image')
    else:
        img_form = AddImageForm()
    return render(request, 'api/add_image.html', {'img_form': img_form,
                                                  'current_user': current_user})


@login_required
def edit_image(request, id=None):
    current_user = CustomUser.objects.get(id=request.user.pk)
    if id:
        image = get_object_or_404(Image, pk=id)
        if image.user_id != request.user:
            messages.error(request, "You cannot access someone else's image")
            return redirect('dashboard')
    else:
        image = Image(user_id=request.user)
    img_form = AddImageForm(request.POST or None, instance=image)
    sizes = current_user.profile.img_size.all()
    if request.POST and img_form.is_valid():
        img_form.save()
        return redirect('dashboard')

    return render(request, 'api/edit_image.html', {'img_form': img_form,
                                                   'image': image,
                                                   'current_user': current_user,
                                                   'sizes': sizes})

def thumb_image(request, id=None, height=None, width=None):
    if id and height and width:
        image = Image.objects.get(id=id)
        size = f'{width}x{height}'
        if image.expires:
            current_time = now()
            delta = current_time - image.created
            delta_sec = int(delta.total_seconds())
            if delta_sec >= image.expires:
                messages.error(request, "Sorry! The link has expired!")
                return redirect('index')
            else:
                return render(request, 'api/thumb_image.html', {'image': image,
                                                                'size': size})

