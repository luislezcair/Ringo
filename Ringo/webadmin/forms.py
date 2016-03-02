from django import forms
from ringoserver.models import Visitor


TOPIC_CHOICES = (
    ('general', 'General Enquiry'),
    ('bug', 'Bug Report'),
    ('suggestions', 'Suggestions'),
)


class ContactForm (forms.Form):
    subject = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(), initial='Write your feedback here!')
    email = forms.EmailField(required=False)


class VisitorForm(forms.ModelForm):
    next = forms.CharField(required=False)

    class Meta:
        model = Visitor
        exclude = tuple()
