from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment
from .forms import ContactCourse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def courses(request):
    courses = Course.objects.all()
    template_name= 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request,template_name, context)


def details(request,slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_email(course)
            form = ContactCourse()

    else:
        form = ContactCourse()
    context ['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
       #enrollment.active()
        messages.success(request,'Voce foi inscrito no curso com sucesso!')
    else:
        messages.info(request,'Voce ja esta inscrito no curso')

    return redirect('accounts:dashboard')