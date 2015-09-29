from django import forms


TOPIC_CHOICES = (
    ('general', 'General Enquiry'),
    ('bug', 'Bug Report'),
    ('suggestions', 'Suggestions'),
)


class ContactForm (forms.Form):
    subject = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(), initial='Write your feedback here!')
    email = forms.EmailField(required=False)


