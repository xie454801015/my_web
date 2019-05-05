from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128)
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput)
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput)
    email = forms.EmailField(label='邮箱地址', widget=forms.EmailInput)
    sex = forms.ChoiceField(label='性别', choices=gender)
