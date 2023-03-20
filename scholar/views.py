from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, EmailMultiAlternatives

# Create your views here.

def EditView(request, pk):
    data = Application.objects.filter(user=request.user).get(id=pk)
    form = ApplicationForm()
    if request.method != 'POST':
        form = ApplicationForm(instance=data)
    else:
        form = ApplicationForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update successful')
            return redirect(reverse('status', args=[data.scholarship.pk]))
    return render(request, 'apply.html', {'form':form, 'data':data})

def activate(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.success(request, 'Activation link is invalid!')
        return redirect('home')

def RegisterView(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            current_site = get_current_site(request) 
            subject = 'MacroPhages Group of Companies: Notification to verify email'
            email_template_name = 'acc_activate.txt'
            context = {
            'domain': current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': account_activation_token.make_token(user),
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, 'olayemipeter2005@gmail.com' , [user.email])
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'account created successfully. <br> Please check your email inbox or spam to confirm your email address and complete registration')
            return redirect('home')
    return render(request, 'registration/register.html', {'form':form})

@login_required
def StatusView(request, pk):
    obj = Scholarship.objects.get(id=pk)
    data = Application.objects.get(user=request.user, scholarship=obj)
    return render(request, 'status.html', {'obj':obj, 'data':data})

@login_required
def ApplicationView(request, pk):
    obj = Scholarship.objects.get(id=pk)
    post = Application.objects.all()
    form = ApplicationForm()
    if request.method != 'POST':
        form = ApplicationForm()
    else:
        form = ApplicationForm(request.POST, request.FILES) 
        if form.is_valid():
            if post.filter(user=request.user, scholarship=obj).exists():
                post.filter(user=request.user, scholarship=obj).delete()
                request.user.delete()
                messages.success(request, 'In accordance with our privacy policy, your account and applications has been deleted due to duplicate applications. Kindly fuck off.')
                return redirect(reverse('home'))
            else:
                data = form.save(commit=False)
                data.user = request.user
                data.scholarship = obj
                data.save()
                return redirect(reverse('send_mail', args=[data.pk]))
    return render(request, 'apply.html', {'form':form, 'obj':obj})

def DetailView(request, pk):
    obj = Scholarship.objects.get(id=pk)
    data = Application.objects.all()
    applied = False
    try:
        if data.filter(user=request.user, scholarship=obj).exists():
            applied = True
    except (User.DoesNotExist, TypeError):
        applied = False
    return render(request, 'detail.html', {'obj':obj, 'applied':applied})

class AvailableView(ListView):
    queryset = Scholarship.objects.order_by('-date')
    template_name = 'available.html'
    context_object_name = 'obj'

class HomeView(TemplateView):
    template_name = 'home.html'

def apply_mail(request, pk):
    data = Application.objects.filter(user=request.user).get(id=pk)
    current_site = get_current_site(request)
    subject = 'MacroPhages Group of Companies: Scholarship application Notification'
    email_template_name = 'apply.txt'
    context = {
    'domain':current_site,
    'user':data.user,
    'data':data
    }
    email = render_to_string(email_template_name, context)
    msg = EmailMultiAlternatives(subject, email, 'olayemipeter2005@gmail.com', [data.email])
    msg.send()
    messages.success(request, 'Application successful.<br>Your application details has been sent to your mail. check inbox or spam.')
    return redirect(reverse('info', args=[data.scholarship.pk]))
