from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, StudyUser


class SignupForm(UserCreationForm):
    phone_number = forms.CharField()
    address = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = StudyUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self):
        user = super().save()
        profile = Profile.objects.create(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data['address']
        )
        return user
