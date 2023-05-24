from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.
class NewUserForm(UserCreationForm):
	perans = (
	('Atlet', 'Atlet'),
	('Pelatih', 'Pelatih'),
	('Umpire', 'Umpire'),
	)
	email = forms.EmailField(required=True)
	peran = forms.ChoiceField(choices=perans)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "peran")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user