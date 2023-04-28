from django.db import models
from django.utils import timezone
from datetime import datetime
from django.forms import ValidationError
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
#Model for additional fields of SignUp form
# class UserData(models.Model):
#         user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
#         ROLES = (('HR','HR'),
#                  ('Manager','Manager'),
#                  ('Admin','Admin'),)
#         role = models.CharField(choices=ROLES, verbose_name='Select your role',max_length=50)
#         eid = models.CharField(verbose_name='Employee ID', max_length=20, null=True)
#         # is_staff = models.BooleanField(default=False)
#         # is_superuser = models.BooleanField(default=False)

#Model for the EmpForm
class Employee(models.Model):
        BG = (('A+', 'A+'),
                ('A-', 'A-'),
                ('B+', 'B+'),
                ('B-', 'B-'),
                ('O+', 'O+'),
                ('O-', 'O-'),
                ('AB+', 'AB+'),
                ('AB-', 'AB-'),)

        DEPT = (('IT','IT'),
                ('Production','Production'),
                ('Sales','Sales'),
                ('HR','HR'),
                ('Finance','Finance'),
                ('Marketing','Marketing'),
                ('Other','Other'),)

        DESIG = (('Employee','Employee'),
                ('Intern','Intern'),
                ('Site Head','Site Head'),
                ('Region Head','Region Head'),
                ('Manager','Manager'),
                ('HR','HR'),
                ('Director','Director'),
                ('President','President'),
                ('CEO','CEO'),
                ('Owner','Owner'),
                ('Other','Other'),)

        TYPE = (('Permanent Employee','Permanent Employee'),
                ('Contract Based','Contract Based'),)

        MODE = (('Day','Day'),
                ('Month','Month'),)

        # OPTION = (('Yes','Yes'),
        #           ('No','No'),)

        ROLES = (('Employee','Employee'),
                 ('Manager','Manager'),
                 ('HR','HR'),)

        user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
        #personal detail field
        firstname = models.CharField(max_length=20, null=True, verbose_name='First Name')
        lastname = models.CharField(max_length=30, null=True, verbose_name='Last Name')
        email = models.EmailField(max_length=50, null=True, verbose_name='Email')
        phone = models.CharField(max_length=10, null=True, verbose_name='Phone')
        address = models.CharField(max_length=100, null=True, verbose_name='Address')
        bloodgroup = models.CharField(choices=BG, max_length=20, null=True, default='A+', verbose_name='Blood Group')
        econtactname = models.CharField(max_length=30, null=True, verbose_name='Emergency Contact Name')
        econtactphone = models.CharField(max_length=10, null=True, verbose_name='Emergency Contact Number')

        #widget=models.Select(attrs={'style':'width:15%','class': 'form-control'})

        #job detail fields
        empid = models.CharField(max_length=20, null=True, unique=True, verbose_name='Employee ID')
        role = models.CharField(choices=ROLES, verbose_name='Select your role',max_length=50,default='Employee')
        doj = models.DateTimeField(default=datetime.now,help_text = "Please use the following format: <em>YYYY-MM-DD HH:MM:SS</em>.", verbose_name='Date of Joining')
        department = models.CharField(choices=DEPT,max_length=20,null=True, default='IT', verbose_name='Department')
        designation = models.CharField(choices=DESIG,max_length=20,null=True, default='Employee', verbose_name='Designation')
        emptype = models.CharField(choices=TYPE, max_length=20,default='Permanent Employee',null=True, verbose_name='Employment Type')
        salary = models.IntegerField(null=True, verbose_name='Salary')
        per = models.CharField(choices=MODE,max_length=20,null=True, default='Month', verbose_name='Per')
        # option = models.CharField(choices=OPTION,max_length=20,null=True, default='No', verbose_name='Do the employee have juniors?')

        def employee(self):
                return f"{self.empid} - {self.firstname} {self.lastname}"

        class Meta:
                db_table = "Employee"

        def __str__(self):
                if self.firstname and self.lastname is not None:
                        return self.firstname + " " + self.lastname
                else:
                        return ""

# #Model for the ClientForm
class Client(models.Model):
        CTYPE = (('Individual','Individual'),
                ('Company','Company'),)

        TOB = (('Service Provider','Service Provider'),
                ('Manufacturer','Manufacturer'),
                ('Consultant','Consultant'),
                ('Traders and Distributors','Traders and Distributors'),
                ('Other','Other'))

        PCM = (('Email','Email'),
                ('Phone','Phone'),)

        user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

        #general detail fields
        cid = models.CharField(max_length=20, null=True, unique=True, verbose_name='Client ID')
        ctype = models.CharField(choices=CTYPE,max_length=20,null=True, default='Individual', verbose_name='Client Type')
        compname = models.CharField(max_length=100, null=True, verbose_name='Company Name')
        compweb = models.CharField(max_length=100,null=True, verbose_name='Company Website')
        typeob = MultiSelectField(choices=TOB,max_length=50,null=True, verbose_name='Type of Business')

        #contact detail fields
        cfirstname = models.CharField(max_length=20, null=True, verbose_name='First Name')
        clastname = models.CharField(max_length=30, null=True, verbose_name='Last Name')
        cpcm = models.CharField(choices=PCM,max_length=50,null=True, default='Phone', verbose_name='Preferred Contact Method')
        cemail = models.EmailField(max_length=20, null=True, verbose_name='Email')
        cphone = models.CharField(max_length=10, null=True, verbose_name='Phone')
        caddress = models.TextField(max_length=50, null=True, verbose_name='Address')
        ainfo = models.TextField(max_length=50, null=True, verbose_name='Additional Information')


        def client(self):
                return f"{self.cid} - {self.cfirstname} {self.clastname}"

        class Meta:
                db_table = "Client"

        def __str__(self):
                if self.cfirstname and self.clastname is not None:
                        return self.cfirstname + " " + self.clastname
                else:
                        return ""

#Model for the CompanyDetail
class Company(models.Model):

        OFFLEAVE = (('Saturday','Saturday'),
                    ('Sunday','Sunday'),)

        #general details fields
        compname = models.CharField(max_length=20, null=True, verbose_name='Company Name')
        oname = models.CharField(max_length=20, null=True, verbose_name='Company Owner Name')
        compemail = models.EmailField(max_length=20, null=True, verbose_name='Email')
        compphone = models.CharField(max_length=10, null=True, verbose_name='Phone')
        compaddress = models.TextField(max_length=50, null=True, verbose_name='Address')

        #additional details fields
        lapm = models.IntegerField(null=True, verbose_name='Leaves allowed per month')
        plgm = models.IntegerField(null=True, verbose_name='Paid Leaves given per month')
        offleave = MultiSelectField(choices=OFFLEAVE,max_length=50,null=True, verbose_name='Weekend Official Leave')
        # sttime = models.TimeField(auto_now=False, auto_now_add=False, null=True)
        # endtime = models.TimeField(auto_now=False, auto_now_add=False, null=True)

        class Meta:
                db_table = "Company"

        def __str__(self):
                if self.compname is not None:
                        return self.compname + " " + "Data"
                else:
                        return ""

#model for the ProjectForm
class Project(models.Model):

        REGIONS = (('R1','R1'),
                   ('R2','R2'),
                   ('R3','R3'),)

        user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

        #project detail fields
        client = models.CharField(max_length=100, null=True, verbose_name='Client')
        prjtitle = models.CharField(max_length=50, null=True, verbose_name='Project Title')
        siteloc = models.TextField(max_length=50, null=True, verbose_name='Site Location')
        startdt = models.DateTimeField(default=datetime.now,help_text = "Please use the following format: <em>YYYY-MM-DD HH:MM:SS</em>.", verbose_name='Starting Date')
        region = models.CharField(choices=REGIONS,max_length=50,null=True, default='Service Provider', verbose_name='Region')
        description = models.TextField(max_length=50, null=True, verbose_name='Description')

        #assigned staff detail fields
        prjhead = models.CharField(max_length=100, null=True, verbose_name='Project Head')
        regionhead = models.CharField(max_length=100, null=True, verbose_name='Region Head')
        sitehead = models.CharField(max_length=100, null=True, verbose_name='Site Head')

        # def __str__(self):
        #         return f"{self.cid} - {self.cfirstname} {self.clastname}"

        class Meta:
                db_table = "Project"

        def __str__(self):
                if self.prjtitle is not None:
                        return self.prjtitle
                else:
                        return ""

#model for the Senior-Junior Mapping Form
class Mapping(models.Model):

        user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
        # jid = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_id', null=True)
        # junior = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, verbose_name='Junior')
        junior = models.CharField(max_length=255, null=True,verbose_name='Junior')
        # junior = models.ForeignKey(User, on_delete=models.CASCADE, related_name='junior_mappings', null=True, verbose_name='Junior')

        class Meta:
                db_table = "Mapping"

        def __str__(self):
                if self.junior is not None:
                        return self.junior
                        # f"{self.junior.first_name} {self.junior.last_name}"
                else:
                        return ""

#model for the Attendance Entry Form
class Attendance(models.Model):
        ATTENDANCE = (('Full Day','Full Day'),
                      ('Half Day','Half Day'),
                      ('Overtime','Overtime'),
                      ('Absent','Absent'),)

        user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
        tdate = models.DateTimeField(default=timezone.now, verbose_name='Today Date', editable=False)
        # tdate=models.DateTimeField(default=timezone.now, verbose_name='Today Date')
        attendance = models.CharField(choices=ATTENDANCE, max_length=100, null=True, verbose_name='Attendance', default='Full Day')
        mapping = models.ForeignKey(Mapping, on_delete=models.CASCADE, default=None, null=True)
     
        class Meta:
                db_table = "Attendance"

        def __str__(self):
                if self.attendance is not None:
                        return self.attendance
                else:
                        return ""

# class JrAttendance(models.Model):
#         ATTENDANCE = (('Full Day','Full Day'),
#                       ('Half Day','Half Day'),
#                       ('Overtime','Overtime'),
#                       ('Absent','Absent'),)

#         user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
#         # mapping = models.ForeignKey(Mapping, on_delete=models.CASCADE, null=False)
#         mapping = models.CharField(max_length=255, null=True,verbose_name='Juniors')
#         tdate=models.DateTimeField(default=datetime.now, verbose_name='Today Date')
#         attendance = models.CharField(choices=ATTENDANCE, max_length=100, null=True, verbose_name='Attendance', default='Full Day')

#         class Meta:
#                 db_table = "JrAttendance"

#         def __str__(self):
#                 if self.attendance is not None:
#                         return self.attendance
#                 else:
#                         return ""