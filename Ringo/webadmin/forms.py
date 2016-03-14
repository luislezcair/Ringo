from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from ringoserver.models import Visitor, Owner


TOPIC_CHOICES = (
    ('general', 'General Enquiry'),
    ('bug', 'Bug Report'),
    ('suggestions', 'Suggestions'),
)


class ContactForm(forms.Form):
    subject = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(), initial='Write your feedback here!')
    email = forms.EmailField(required=False)


class VisitorForm(forms.ModelForm):
    next = forms.CharField(required=False)

    class Meta:
        model = Visitor
        exclude = tuple()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm password',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        kwargs.setdefault('label_suffix', '')

        for key in self.fields:
            self.fields[key].required = True

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise ValidationError("Passwords do not match.", code='invalid')

        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User.objects.get(username=username)
            raise ValidationError("This username is already in use. Please choose another.", code='invalid')
        except ObjectDoesNotExist:
            pass

        return username

    def save(self, commit=True):
        user = super(UserForm, self).save()
        owner = Owner.objects.create(auth_user=user)
        owner.save()
        return user
