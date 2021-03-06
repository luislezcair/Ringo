# coding=utf-8

from ringoserver.models import *
from forms import ContactForm, VisitorForm, UserForm, DeviceForm
from django.core.mail import send_mail
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string


@login_required
def index(request):
    return render(request, 'webadmin/index.html')


@login_required
def visit_list(request):
    latest_visits_list = Visit.objects.order_by('-date')
    context = {'latest_visits_list': latest_visits_list}
    return render(request, 'ringoserver/visit_list.html', context)


@login_required
def visit_detail(request, visit_id):
    # TODO: discuss how to treat the case when unknown people is in the picture.
    visit = get_object_or_404(Visit, pk=visit_id)
    visitors = Visitor.objects.filter(visit=visit_id)
    unknowns = int(visit.people) - len(visitors)
    # picture = Picture.objects.get(id=visit.picture.id)
    context = {'visit': visit, 'visitors': visitors, 'unknowns': unknowns}
    return render(request, 'ringoserver/visit_detail.html', context)


@login_required
def visitor_list(request):
    visitors = Visitor.objects.order_by('name')
    context = {'visitor_list': visitors}
    return render(request, 'ringoserver/visitor_list.html', context)


@login_required
def visitor_details(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    context = {'visitor': visitor}
    return render(request, 'ringoserver/visitor_detail.html', context)


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
    template_name = 'ringoserver/visitor_create.html'
    form_class = VisitorForm
    success_url = '/webadmin/visitors/'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(VisitorCreate, self).get_form_kwargs()
        redirect = self.request.GET.get('next')
        if redirect:
            if 'initial' in kwargs.keys():
                kwargs['initial'].update({'next': redirect})
            else:
                kwargs['initial'] = {'next': redirect}
        return kwargs

    def form_invalid(self, form):
        return super(VisitorCreate, self).form_invalid(form)

    def form_valid(self, form):
        redirect = form.cleaned_data.get('next')
        if redirect:
            self.success_url = redirect
        return super(VisitorCreate, self).form_valid(form)


class VisitorDelete(DeleteView):
    model = Visitor
    success_url = '/webadmin/visitors'


class ConfigurationUpdate(SuccessMessageMixin, UpdateView):
    model = Configuration
    fields = '__all__'
    template_name_suffix = '_update'
    success_url = '/webadmin/settings/1'
    success_message = "The configuration was successfully updated"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,)


class VisitUpdate(UpdateView):
    model = Visit
    fields = ('visitors',)
    template_name_suffix = '_update'
    success_url = '/webadmin/visits'


class OwnersDevicesListView(ListView):
    model = Owner
    context_object_name = 'owners'

    @staticmethod
    def post(request, *args, **kwargs):
        owner = Owner.objects.get(pk=request.POST['id'])
        html = render_to_string('ringoserver/device_list.html', {'owner': owner}, request=request)
        return JsonResponse({'html': html})


class OwnerDetailView(DetailView):
    model = User
    template_name = 'ringoserver/owner_detail.html'
    context_object_name = 'user'


class OwnerEditView(UpdateView):
    model = User
    template_name = 'ringoserver/owner_update.html'
    form_class = UserForm
    success_url = '/webadmin/owners_devices'


class OwnerDeleteView(DeleteView):
    model = Owner
    success_url = '/webadmin/owners_devices'


class OwnerCreateView(CreateView):
    model = User
    template_name = 'ringoserver/owner_create_form.html'
    form_class = UserForm
    success_url = '/webadmin/owners_devices'


class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    success_url = '/webadmin/owners_devices'

    def get_context_data(self, **kwargs):
        context = super(DeviceCreateView, self).get_context_data(**kwargs)
        context['owner'] = Owner.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super(DeviceCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.kwargs['pk']
        return kwargs


class DeviceDeleteView(DeleteView):
    model = Device
    success_url = '/webadmin/owners_devices'
