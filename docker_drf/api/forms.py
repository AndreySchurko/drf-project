from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from api.models import CustomUser, Image


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class LoginForm(forms.Form):
    email = forms.CharField(required=True,
                            label='Email',
                            widget=forms.TextInput(attrs={
                                'class': 'py-3 px-4 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400',
                                'placeholder': 'name@mail.com',
                                'autocomplete': 'off',
                                'aria-describedby': 'email-error'}))
    password = forms.CharField(required=True,
                               label='Password',
                               widget=forms.PasswordInput(attrs={
                                    'class': 'py-3 px-4 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 toggle-id-1',
                                    'placeholder': 'Password',
                                    'autocomplete': 'off',
                                    'data-toggle': 'password',
                                    'aria-describedby': 'password-error'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'shrink-0 mt-0.5 border-gray-200 rounded text-blue-600 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800'}))

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if CustomUser.objects.filter(email__iexact=email).exists():
            user = CustomUser.objects.get(email__iexact=email)
        else:
            raise ValidationError('email')
        if user:
            if not user.check_password(password):
                raise ValidationError('password')
        return cleaned_data


class AddImageForm(forms.ModelForm):
    default_image = forms.ImageField(widget=forms.FileInput(attrs={
                                    'class': 'hidden'}),
                                     required=True)
    title = forms.CharField(label='Image title',
                            help_text='required',
                            widget=forms.TextInput(attrs={
                                   'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                   'placeholder': '',
                                   'autocomplete': 'off'}),
                            required=True)
    author = forms.CharField(label='Image author',
                             widget=forms.TextInput(attrs={
                                'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                'placeholder': '',
                                'autocomplete': 'off'}),
                             required=False)
    published = forms.BooleanField(label='Published',
                                   help_text='I want to publish it for everyone',
                                   required=False,
                                   widget=forms.CheckboxInput(attrs={
                                       'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
                                   }))
    expires = forms.IntegerField(label='Link will expire, sec.',
                                 help_text='Min. 300, Max. 30 000 seconds',
                                 required=False,
                                 widget=forms.TextInput(attrs={
                                     'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                     'placeholder': 'Link will expire, sec.',
                                     'autocomplete': 'off',
                                     'type': 'number',
                                     'min': '300',
                                     'max': '30000',
                                     'step': '1'
                                 }))

    class Meta:
        model = Image
        fields = ['default_image', 'title', 'author', 'published', 'expires']
