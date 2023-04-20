from datetime import date
from django import forms
from Attendance.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import Attendance_App
from .models import Company, Attendance
from django.utils import timezone
import random
import string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# SignIn form additional fields
# class SigninForm(UserCreationForm):

#     ROLES = (('HR','HR'),
#              ('Manager','Manager'),
#              ('Admin','Admin'),)
    
#     email = forms.EmailField(max_length=200, help_text='Required')  
#     role = forms.ChoiceField(choices=ROLES,label='Select your role')
#     eid = forms.CharField(label='Employee ID')
#     password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput)
    
#     class Meta: 
#         model = User
#         fields = ['email','first_name','last_name']

# Employee Forms
class EmpForm1(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}),label='Address')
    class Meta:
        model = Employee
        fields = ['firstname','lastname','email','phone','address','bloodgroup','econtactname','econtactphone',]

class EmpForm2(forms.ModelForm):
    # OPTION = (('Yes','Yes'),
    #           ('No','No'),)
    
    ROLES = (('Employee', 'Employee'),
            ('Manager', 'Manager'),
            ('HR', 'HR'),)

    role = forms.ChoiceField(choices=ROLES, label='Role')
    doj = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Joining')
    # option = forms.ChoiceField(choices=OPTION, widget=forms.RadioSelect,label='Do the employee have juniors?')
    class Meta:
        model = Employee
        fields = ['role','empid','doj','department','designation','emptype','salary','per']

# Client Forms
class ClientForm1(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['cid','ctype','compname','compweb','typeob']

class ClientForm2(forms.ModelForm):
    PCM = (('Email','Email'),
           ('Phone','Phone'),)

    caddress = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label='Address')
    ainfo = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label='Additional Information')
    cpcm = forms.ChoiceField(choices=PCM, widget=forms.RadioSelect,label='Preferred Contact Method')
    class Meta:
        model = Client
        fields = ['cfirstname','clastname','cpcm','cemail','cphone','caddress','ainfo',]

# Company Detail Forms
class CompForm1(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['compname','oname','compemail','compphone','compaddress',]

class CompForm2(forms.ModelForm):
    # offleave = forms.MultipleChoiceField(choices=Company.OFFLEAVE, widget=forms.CheckboxSelectMultiple, label='Weekend Official Leave')
    # sttime = forms.TimeField(widget=TimePicker(options={'format': 'HH:mm'}),label='Starting Time')
    # endtime = forms.TimeField(widget=TimePicker(options={'format': 'HH:mm'}),label='Ending Time')

    class Meta:
        model = Company
        fields = ['lapm','plgm','offleave',]

# Project Detail Forms
class PrjForm1(forms.ModelForm):
    startdt = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Start Date')
    client = forms.ChoiceField(choices=[])
    prjtitle = forms.CharField(widget=forms.Textarea(attrs={"rows": 1}), label='Project Title')
    siteloc = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label='Site Location')
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label='Description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].choices = [((obj.cid,obj.cfirstname), obj.client()) for obj in Client.objects.all()]
    
    class Meta:
        model = Project
        fields = ['client','prjtitle','siteloc','startdt','region','description',]

class PrjForm2(forms.ModelForm):
    prjhead = forms.ChoiceField(choices=[], label='Project Head')
    regionhead = forms.ChoiceField(choices=[], label='Region Head')
    sitehead = forms.ChoiceField(choices=[], label='Site Head')
    
    class Meta:
        model = Project
        fields = ['prjhead','regionhead','sitehead',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prjhead'].choices = [(obj.firstname, obj.employee()) for obj in Employee.objects.all()]
        self.fields['regionhead'].choices = [(obj.firstname, obj.employee()) for obj in Employee.objects.all()]
        self.fields['sitehead'].choices = [(obj.firstname, obj.employee()) for obj in Employee.objects.all()]

# class SrjrMapForm(forms.ModelForm):
    
#     junior = forms.ModelMultipleChoiceField(
#         queryset=Employee.objects.all(),
#         widget=forms.CheckboxSelectMultiple(),
#         label='Select Junior(s)'
#     )

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)
#         if self.instance.junior:
#             self.fields['junior'].queryset = Employee.objects.exclude(id=self.instance.junior.id)
#             # self.fields['junior'].queryset = User.objects.exclude(user=request.user)
#         else:
#             self.fields['junior'].queryset = Employee.objects.exclude(id=user.id)

#         # self.fields['junior'].label_from_instance = lambda user: f"{user.first_name} {user.last_name}"

#     def save(self, commit=True):
#         juniors = self.cleaned_data.get('junior', [])
#         mappings = []
#         for junior in juniors:
#             mapping = Mapping(user=self.user, junior=junior)
#             if commit:
#                 mapping.save()
#             mappings.append(mapping)
#         return mappings

#     def clean(self):
#         cleaned_data = super().clean()
#         juniors = cleaned_data.get('junior', [])
#         if juniors and Mapping.objects.filter(user=self.user).exists():
#             raise forms.ValidationError('You have already selected junior(s)!')
#         return cleaned_data

#     class Meta:
#         model = Mapping
#         fields = ['junior']

#############################################################################################

class SrjrMapForm(forms.ModelForm):
    junior = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple(),label='Select Junior(s)')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        employee_j = [(obj.firstname, obj.employee()) for obj in Employee.objects.all()]
        # employee_j = [(obj.id, obj.firstname) for obj in Employee.objects.all()]

    #     employee_j = [(obj.firstname, obj.employee()) for obj in Employee.objects.all()]

        # Add a check to ensure that junior is not None before accessing its id attribute
        if self.instance.junior:
            employee_j = [(obj.firstname, obj.employee()) for obj in Employee.objects.exclude(id=self.instance.junior.id)]
            # employee_j = [(obj.id, obj.firstname) for obj in Employee.objects.all()]

        # self.fields['senior'].choices = employee_s
        self.fields['junior'].choices = employee_j

    def save(self, commit=True):
        # Override the save method to create multiple Mapping objects, one for each selected junior
        juniors = self.cleaned_data.get('junior', [])
        mappings = []
        for junior in juniors:
            mapping = Mapping(user=self.user, junior=junior)
            if commit:
                mapping.save()
            mappings.append(mapping)
        return mappings
    
    def clean(self):
        cleaned_data = super().clean()
        juniors = cleaned_data.get('junior', [])
        if juniors and Mapping.objects.filter(user=self.user).exists():
            raise forms.ValidationError('You have already selected junior(s)!')
        return cleaned_data

    class Meta:
        model = Mapping
        fields = ['junior']

#############################################################################################
# Mapping Form
# class SrjrMapForm(forms.ModelForm):
#     senior = forms.ChoiceField(choices=[])
#     junior = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)

#     class Meta:
#         model = Mapping
#         fields = ['senior','junior',]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         employee_s = [(obj.firstname, obj.employee()) for obj in Employee.objects.filter(emptype='Permanent Employee')]
#         employee_j = [(obj.firstname, obj.employee()) for obj in Employee.objects.filter(emptype='Contract Based')]

#         # Add a check to ensure that junior is not None before accessing its id attribute
#         if self.instance.junior:
#             employee_j = [(obj.firstname, obj.employee()) for obj in Employee.objects.exclude(id=self.instance.junior.id)]

#         self.fields['senior'].choices = employee_s
#         self.fields['junior'].choices = employee_j

#     def clean_junior(self):
#         return ','.join(self.cleaned_data.get('junior', []))
    
#     def clean(self):
#         cleaned_data = super().clean()
#         senior = cleaned_data.get('senior')

#         if Mapping.objects.filter(senior=senior).exists():
#             self.add_error('senior', 'This senior already has an entry in the database.')
#         return cleaned_data
    
# Attendance Forms
class AttForm1(forms.ModelForm):
    ATTENDANCE = (('Full Day','Full Day'),
                  ('Half Day','Half Day'),
                  ('Overtime','Overtime'),
                  ('Absent','Absent'),)
    
    # tdate = models.DateTimeField(auto_now_add=True, verbose_name='Today Date')  
    tdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Today Date')
    senioratt = forms.ChoiceField(choices=ATTENDANCE, widget=forms.RadioSelect,label='My Attendance')

    class Meta:
        model = Attendance
        fields = ['tdate','senioratt']

    # def save(self, commit=True):
    #     attendance = super().save(commit=False)
    #     attendance.tdate = timezone.now()  # Set tdate to the current date and time
    #     attendance.senioratt = self.cleaned_data['senioratt']
    #     if commit:
    #         attendance.save()
    #     return attendance

# class AttForm2(forms.ModelForm):
#     ATTENDANCE = (('Full Day','Full Day'),
#                   ('Half Day','Half Day'),
#                   ('Overtime','Overtime'),
#                   ('Absent','Absent'),)
    
#     junioratt = forms.ChoiceField(choices=ATTENDANCE, widget=forms.RadioSelect,label='Attendance')
#     # def save(self, commit=True):
#     #     attendance = super().save(commit=False)
#     #     #attendance.junioratt = self.cleaned_data['junioratt']
#     #     if commit:
#     #         attendance.save()
#     #     return attendance
    
#     class Meta:
#         model = Attendance
#         #fields = ['juniors','junioratt']
#         fields = ['juniors','junioratt']

class AttForm2(forms.ModelForm):
    ATTENDANCE = (
        ('Full Day', 'Full Day'),
        ('Half Day', 'Half Day'),
        ('Overtime', 'Overtime'),
        ('Absent', 'Absent'),
    )

    junioratt = forms.ChoiceField(choices=ATTENDANCE, widget=forms.RadioSelect)

    class Meta:
        model = Attendance
        fields = ('senioratt',)

    def save(self, commit=True):
        attendance = super().save(commit=False)
        attendance.senioratt = self.cleaned_data['senioratt']
        attendance.junioratt = self.cleaned_data['junioratt']
        if commit:
            attendance.save()
        return attendance