from ringoserver.models import *
from forms import ContactForm
from django.core.mail import send_mail
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin


@login_required
def index(request):
    return render(request, 'webadmin/index.html')


@login_required
def visit_list(request):
    latest_visits_list = Visit.objects.order_by('-date')
    context = RequestContext(request, {
        'latest_visits_list': latest_visits_list,
    })
    return render(request, 'ringoserver/visit_list.html', context)


@login_required
def visit_detail(request, visit_id):
    # TODO: discuss how to treat the case when unknown people is in the picture.
    visit = get_object_or_404(Visit, pk=visit_id)
    visitors = Visitor.objects.filter(visit=visit_id)
    unknowns = int(visit.people) - len(visitors)
    # picture = Picture.objects.get(id=visit.picture.id)
    return render(request, 'ringoserver/visit_detail.html',
                  {'visit': visit, 'visitors': visitors, 'unknowns': unknowns})


@login_required
def visitor_list(request):
    visitors = Visitor.objects.order_by('name')
    context = RequestContext(request, {
        'visitor_list': visitors,
    })
    return render(request, 'ringoserver/visitor_list.html', context)


@login_required
def visitor_details(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    # TODO: commented code get every picture of the visitor
    # visits = Visit.objects.filter(visitor__id=visitor_id)
    # images = []
    # for visit in visits:
    #     images.append(visit.picture)
    visits = Visit.objects.filter(visitors__id=visitor_id)
    images = []
    for visit in visits:
        images.append(visit.picture)
    # images = VisitorFaceSample.objects.filter(visitor__id=visitor.id)
    return render(request, 'ringoserver/visitor_detail.html', {'visitor': visitor, 'images': images})


@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['example@gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render(request, 'webadmin/contact.html', {'form': form})


class VisitorUpdate(UpdateView):
    model = Visitor
    fields = '__all__'
    template_name_suffix = '_update'
    success_url = '/webadmin/visitors'


class VisitorCreate(CreateView):
    model = Visitor
    fields = '__all__'
    template_name_suffix = '_create'
    success_url = '/webadmin/visitors'


class ConfigurationUpdate(SuccessMessageMixin, UpdateView):
    model = Configuration
    fields = '__all__'
    template_name_suffix = '_update'
    success_url = '/webadmin/settings/1'
    success_message = "The configuration was successfully updated"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
        )


class VisitUpdate(UpdateView):
    model = Visit
    fields = ('visitors',)
    template_name_suffix = '_update'
    success_url = '/webadmin'
