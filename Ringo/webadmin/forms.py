from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
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

        # If we're editing an user, blank passwords are ok (we don't change the passowrd)
        self.fields['password'].required = self.instance.pk is None
        self.fields['confirm_password'].required = self.instance.pk is None

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        # Blank password means we're not changing it
        if self.instance.pk and not password and not confirm_password:
            return self.cleaned_data

        if password != confirm_password:
            raise ValidationError("Passwords do not match.", code='invalid')

        self.cleaned_data['password'] = make_password(password)

        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']

        if not self.instance.pk:
            try:
                User.objects.get(username=username)
                raise ValidationError("This username is already in use. Please choose another.", code='invalid')
            except ObjectDoesNotExist:
                pass

        return username

    def save(self, commit=True):
        user = super(UserForm, self).save()

        try:
            if user.owner:
                pass
        except AttributeError:
            owner = Owner.objects.create(auth_user=user)
            owner.save()

        return user
