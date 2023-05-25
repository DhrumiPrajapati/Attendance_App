from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from email.message import EmailMessage
from django.contrib import messages
from django.forms import PasswordInput
from django.template import loader
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from Attendance.form import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Employee
from Attendance_App import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.models import Group
# from django.utils import timezone
from pytz import timezone
from datetime import datetime, timedelta
# from django.utils import timezone

# Create your views here.

#home template view
@login_required(login_url='loginview')
@never_cache
def home(request):
    template = loader.get_template('home.html')
    context = {'username': request.user.username}
    return HttpResponse(template.render(context, request))

# #tasks template view
# @login_required(login_url='loginview')
# @never_cache
# def tasklist(request):
#     template = loader.get_template('TaskList.html')
#     context = {'username': request.user.username}
#     return HttpResponse(template.render(context, request))

# @login_required(login_url='loginview')
# @never_cache
# def tasklist(request):
#     juniors = Mapping.objects.filter(user=request.user)
#     data = Attendance.objects.filter(user=request.user, mapping__junior__isnull=False)
#     template = loader.get_template('TaskList.html')
#     context = {
#         'username': request.user.username,
#         'attdata': data,
#         'juniors': juniors,
#     }
#     return HttpResponse(template.render(context, request))

#user_data view (when clicked on the dp)
@login_required(login_url='loginview')
@never_cache
def userdata(request):
    # Get the employee object matching the user's email ID
    user = request.user
    employee = None

    # If the user is a superuser, show their details
    if user.is_superuser:
        context = {'user': user}
    # If the user is an employee, show their details
    else:
        employee = get_object_or_404(Employee, email=user.username)
        context = {'employee': employee, 'user': user}

    template = loader.get_template('userdata.html')
    return HttpResponse(template.render(context, request))

# @login_required(login_url='loginview')
# @never_cache
# def userdata(request):
#     # Get the employee object matching the user's email ID
#     user = request.user
#     employee = get_object_or_404(Employee, email=request.user.username)

#     template = loader.get_template('userdata.html')
#     context = {'username': request.user.username, 'employee': employee, 'user':user}
#     return HttpResponse(template.render(context, request))

# class EmpDelete(DeleteView):
#     model = Employee
#     success_url = reverse_lazy('EmpList')
#     template_name = 'Attendance/templates/delete_confirm.html'

#emp_home template view
@login_required(login_url='loginview')
def emp_home(request):
    template = loader.get_template('emp_home.html')
    context = {'username': request.user.username}
    return HttpResponse(template.render(context, request))

#LogIn Page View
def loginview(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            # print(request.user.is_authenticated)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('AttFormView')
            else:
                messages.error(request, 'Invalid username or password.')
                # return redirect('loginview')
        else:
            for field, errors in fm.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        fm = AuthenticationForm()

    context = {
        'form': fm,
        'user': request.user,
    }

    return render(request, 'login.html', context)

#logout page view
def logoutview(request):
    logout(request)
    messages.success(request, "Your account has been logged out successfully.")

    return redirect('loginview')

#Employee Form View
@login_required(login_url='loginview')
@never_cache
def EmpForm(request):
    emp = Employee()  # initialize the employee object as None
    if request.method == 'POST':
        empform1 = EmpForm1(request.POST, instance=emp)  # pass the object to both forms
        empform2 = EmpForm2(request.POST, instance=emp)
        if empform1.is_valid() and empform2.is_valid():
            emp = empform1.save(commit=False)
            emp = empform2.save(commit=False)

            # Set the employee's Gmail address as their udsername
            email = emp.email.strip()
            if emp is not None and emp.email:
                username = emp.email
                role = empform2.cleaned_data.get('role')

                password=get_user_model().objects.make_random_password()
                emp.user = get_user_model().objects.create_user(username=username, password=password)

                # emp.user = get_user_model().objects.create_user(username=username, password=get_user_model().objects.make_random_password())
                emp.user.email = email
                emp.user.first_name = emp.firstname
                emp.user.last_name = emp.lastname
                emp.user.save()

                group_name = ''
                if role == 'HR':
                    group_name = 'HR'
                    is_staff = True
                    is_superuser = True

                elif role == 'Manager':
                    group_name = 'Manager'
                    is_staff = True
                    is_superuser = False

                else:
                    group_name = 'Employee'
                    is_staff = False
                    is_superuser = False                   

                group = Group.objects.get(name = group_name)
                group.user_set.add(emp.user)

                user = User.objects.get(username=username, email=email, first_name=emp.user.first_name, last_name=emp.user.last_name)

                user.is_staff = is_staff
                user.is_superuser = is_superuser
                user.save()


                subject = 'Your login credentials for the attendance portal'
                message = f'Your username is {username} and your password is {password}.'
                from_email = 'hrcompany852@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                emp.user = request.user
                emp.save()

                if empform2.cleaned_data['emptype']=='Contract Based':
                    return redirect('SrjrMapFormView')
                else:
                    return redirect('EmpEntry')
                
            else:
                messages.error(request, 'Invalid email address')

                return redirect('EmpForm')

    else:
        empform1 = EmpForm1(instance=emp)  # pass the object to both forms
        empform2 = EmpForm2(instance=emp)
    return render(request, "EmpForm.html", {'empform1': empform1, 'empform2': empform2})

#Employee Entries View
@login_required(login_url='loginview')
@never_cache 
def EmpEntry(request):
    # data = Employee.objects.all()
    data = Employee.objects.filter(user=request.user)
    template = loader.get_template('EmpEntry.html')
    context = {
        'empdata': data,
    }

    return HttpResponse(template.render(context, request))

# @login_required(login_url='loginview')
# @never_cache
# def EmpUpdateForm(request, pk):
#     emp = Employee.objects.get(pk=pk)
#     context = {'emp': emp}
#     return render(request, 'EmpUpdate.html', context)

# def EmpUpdate(request, pk):
#     emp = Employee.objects.get(pk=pk)

#     if request.method == 'POST':
#         emp.firstname = request.POST.get('firstname')
#         emp.lastname = request.POST.get('lastname')
#         emp.email = request.POST.get('email')
#         emp.phone = request.POST.get('phone')
#         emp.address = request.POST.get('address')
#         emp.bloodgroup = request.POST.get('bloodgroup')
#         emp.econtactname = request.POST.get('econtactname')
#         emp.econtactphone = request.POST.get('econtactphone')
#         emp.empid = request.POST.get('empid')
#         emp.role = request.POST.get('role')
#         emp.doj = request.POST.get('doj')
#         emp.department = request.POST.get('department')
#         emp.designation = request.POST.get('designation')
#         emp.emptype = request.POST.get('emptype')
#         emp.salary = request.POST.get('salary')
#         emp.per = request.POST.get('per')
#         emp.save()
#         return redirect('EmpEntry')

#     context = {'emp': emp}
#     return render(request, 'EmpUpdate.html', context)

#Employee Entry Update View
@login_required(login_url='loginview')
@never_cache
def EmpUpdate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        empform1 = EmpForm1(request.POST, instance=employee)
        empform2 = EmpForm2(request.POST, instance=employee)
        
        if empform1.is_valid() and empform2.is_valid():
            # empform1.instance.firstname = employee.firstname
            # empform1.instance.lastname = employee.lastname
            # empform1.instance.email = employee.email

            # empform2.instance.empid = employee.empid
            # empform2.instance.role = employee.role
            # empform2.instance.doj = employee.doj

            empform1.save()
            empform2.save()
            return redirect('EmpEntry')
        print(empform1.errors)
        print(empform2.errors)

    else:
        empform1 = EmpForm1(instance=employee)
        empform2 = EmpForm2(instance=employee)

    return render(request, 'EmpUpdate.html', {'empform1': empform1, 'empform2': empform2, 'emp':employee})

#Employee Entry Delete View
@login_required(login_url='loginview')
@never_cache
def EmpDelete(request, pk, template_name='delete_confirm_emp.html'):
    emp= get_object_or_404(Employee, pk=pk)    
    if request.method=='POST':
        # user = emp.user
        emp.delete()
        # user.delete()

        return redirect('EmpEntry')
    return render(request, template_name, {'object':emp})

# Client Form View
@login_required(login_url='loginview')
@never_cache
def ClientForm(request):
    client = Client()  # create an object for the shared model
    if request.method == 'POST':
        clientform1 = ClientForm1(request.POST, instance=client)  # pass the object to both forms
        clientform2 = ClientForm2(request.POST, instance=client)
        if clientform1.is_valid() and clientform2.is_valid():
            client = clientform1.save(commit=False)
            client = clientform2.save(commit=False)
            client.user = request.user
            client.save()
            # clientform1.save()
            # clientform2.save()

            return redirect('ClientEntry')
    else:
        clientform1 = ClientForm1(instance=client)  # pass the object to both forms
        clientform2 = ClientForm2(instance=client)
    return render(request, "ClientForm.html", {'clientform1': clientform1, 'clientform2': clientform2})

# Client Entries View
@login_required(login_url='loginview')
@never_cache
def ClientEntry(request):
    # data = Client.objects.filter(user=request.user)
    data = Client.objects.all()
    
    template = loader.get_template('ClientEntry.html')
    context = {
        'clientdata': data,
    }
    # print(data)

    return HttpResponse(template.render(context, request))

#Client Entry Update View
@login_required(login_url='loginview')
@never_cache
def CliUpdate(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        clientform1 = ClientForm1(request.POST, instance=client)
        clientform2 = ClientForm2(request.POST, instance=client)
        
        if clientform1.is_valid() and clientform2.is_valid():
            clientform1.save()
            clientform2.save()
            return redirect('ClientEntry')

    else:
        clientform1 = ClientForm1(instance=client)
        clientform2 = ClientForm2(instance=client)

    return render(request, 'CliUpdate.html', {'clientform1': clientform1, 'clientform2': clientform2, 'cli':client})

#Client Entry Delete View
@login_required(login_url='loginview')
@never_cache
def ClientDelete(request, pk, template_name='delete_confirm_client.html'):
    cli= get_object_or_404(Client, pk=pk)    
    if request.method=='POST':
        cli.delete()
        return redirect('ClientEntry')
    return render(request, template_name, {'object':cli})

#Project Form View
@login_required(login_url='loginview')
@never_cache
def ProjectForm(request):
    client=Client.objects.all()
    project = Project()  # create an object for the shared model
    if request.method == 'POST':
        prjform1 = PrjForm1(request.POST, instance=project)  # pass the object to both forms
        prjform2 = PrjForm2(request.POST, instance=project)
        if prjform1.is_valid() and prjform2.is_valid():
            project = prjform1.save(commit=False)
            project = prjform2.save(commit=False)
            project.user = request.user
            project.save()

            return redirect('ProjectEntry')
    else:
        prjform1 = PrjForm1(instance=project)  # pass the object to both forms
        prjform2 = PrjForm2(instance=project)
    return render(request, "ProjectForm.html", {'prjform1': prjform1, 'prjform2': prjform2, 'client':client})

# Project Entries View
@login_required(login_url='loginview')
@never_cache
def ProjectEntry(request):
    # data = Project.objects.all()
    # data = Project.objects.filter(user=request.user)
    data = Project.objects.all()
    template = loader.get_template('ProjectEntry.html')
    context = {
        'prjdata': data,
    }
    return HttpResponse(template.render(context, request))

#Project Entry Update View
@login_required(login_url='loginview')
@never_cache
def PrjUpdate(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        prjform1 = PrjForm1(request.POST, instance=project)
        prjform2 = PrjForm2(request.POST, instance=project)
        
        if prjform1.is_valid() and prjform2.is_valid():
            prjform1.save()
            prjform2.save()
            return redirect('ProjectEntry')

    else:
        prjform1 = PrjForm1(instance=project)
        prjform2 = PrjForm2(instance=project)

    return render(request, 'PrjUpdate.html', {'prjform1': prjform1, 'prjform2': prjform2, 'prj':project})

#Project Entry Delete View
@login_required(login_url='loginview')
@never_cache
def ProjectDelete(request, pk, template_name='delete_confirm_prj.html'):
    prj= get_object_or_404(Project, pk=pk)    
    if request.method=='POST':
        prj.delete()
        return redirect('ProjectEntry')
    return render(request, template_name, {'object':prj})

# Senior-Junior Mapping Form View
@login_required(login_url='loginview')
@never_cache
def SrjrMapFormView(request):
    form = SrjrMapForm(user=request.user)
    empdata = Employee.objects.all()
    map_data = Mapping.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SrjrMapForm(request.user, request.POST)
        if form.is_valid():
            # form.empid = empdata.empid
            # form.firstname = empdata.firstname
            # form.lastname = empdata.lastname
            form.save()
            return redirect('SrjrEntry')
    else:
        form = SrjrMapForm(user=request.user)
    return render(request, "SrjrMapForm.html", {'form': form, 'map_data': map_data, 'empdata':empdata,})

#Senior-Junior Mapping Entries View
@login_required(login_url='loginview')
@never_cache
def SrjrEntry(request):
    data = Mapping.objects.filter(user=request.user).select_related('user')
    num_juniors = data.values_list('junior', flat=True).distinct().count()
    template = loader.get_template('SrjrEntry.html')
    context = {
        'mapdata': data,
        'num_juniors': num_juniors,
    }

    return HttpResponse(template.render(context, request))

# @login_required(login_url='loginview')
# @never_cache
# def MapUpdate(request, pk):
#     mapping = get_object_or_404(Mapping, pk=pk)

#     if request.method == 'POST':
#         mapform = SrjrMapForm(request.POST, instance=mapping)
        
#         if mapform.is_valid():
#             mapform.save()
#             return redirect('SrjrEntry')
#     else:
#         mapform = SrjrMapForm(request.POST, instance=mapping)

#     return render(request, 'MapUpdate.html', {'mapform': mapform, 'mapping':mapping})

@login_required(login_url='loginview')
@never_cache
def MapDelete(request, pk, template_name='delete_confirm_map.html'):
    map = get_object_or_404(Mapping, pk=pk)    
    if request.method=='POST':
        map.delete()
        return redirect('SrjrEntry')
    return render(request, template_name, {'object':map})

#################################################################################################################################
#Attendance Form View
# @login_required(login_url='loginview')
# @never_cache
# def AttFormView(request):
#     juniors = Mapping.objects.filter(user=request.user)
#     names = Attendance.objects.filter(user=request.user)
#     if request.method == 'POST':
#         att1 = Attendance()
#         attform1 = AttForm1(request.POST, instance=att1)
#         if attform1.is_valid():
#             att1 = attform1.save(commit=False)
#             att1.user = request.user
#             # att1.tdate = timezone.now().astimezone(timezone('Asia/Kolkata'))
#             att1.tdate = timezone('Asia/Kolkata').localize(datetime.now())
#             att1.save()
#             for junior in juniors:
#                 att2 = Attendance()
#                 post_data = request.POST.copy()
#                 post_data['mapping'] = junior.id
#                 attform2 = AttForm2(post_data, instance=att2)
#                 if attform2.is_valid():
#                     att2 = attform2.save(commit=False)
#                     att2.user = request.user
#                     att2.tdate = att1.tdate
#                     att2.mapping = junior
#                     # Set the attendance of AttForm2 to the selected attendance by logged in user for that particular junior
#                     att2.attendance = request.POST.get(f"{ junior.id }_attendance")
#                     att2.save()
#         return redirect('AttEntry')
#     else:
#         attform1 = AttForm1() 
#         attform2 = AttForm2() 
#     return render(request, "AttForm.html", {'attform1': attform1, 'attform2': attform2, 'juniors':juniors, 'names':names})


#Attendance Form View
@login_required(login_url='loginview')
@never_cache
def AttFormView(request):
    juniors = Mapping.objects.filter(user=request.user)
    names = Attendance.objects.filter(user=request.user)
    if request.method == 'POST':
        att1 = Attendance()
        attform1 = AttForm1(request.POST, instance=att1)
        if attform1.is_valid():
            att1 = attform1.save(commit=False)
            att1.user = request.user
            # att1.tdate = timezone.now().astimezone(timezone('Asia/Kolkata'))
            att1.tdate = timezone('Asia/Kolkata').localize(datetime.now())
            att1.save()
            for junior in juniors:
                att2 = Attendance()
                post_data = request.POST.copy()
                post_data['mapping'] = junior.id
                attform2 = AttForm2(post_data, instance=att2)
                if attform2.is_valid():
                    att2 = attform2.save(commit=False)
                    att2.user = request.user
                    att2.tdate = att1.tdate
                    att2.mapping = junior
                    # Set the attendance of AttForm2 to the selected attendance by logged in user for that particular junior
                    att2.attendance = request.POST.get(f"{ junior.id }_attendance")
                    att2.save()
        return redirect('AttEntry')
    else:
        attform1 = AttForm1() 
        attform2 = AttForm2() 
    return render(request, "AttForm.html", {'attform1': attform1, 'attform2': attform2, 'juniors':juniors, 'names':names})

#################################################################################################################################
# @login_required(login_url='loginview')
# @never_cache
# def AttFormView(request):
#     juniors = Mapping.objects.filter(user=request.user)
#     names = Attendance.objects.filter(user=request.user)
    
#     # Get the current date
#     current_date = timezone.now().date()

#     # Check if the user has already filled the attendance for the current date
#     if Attendance.objects.filter(user=request.user, tdate__date=current_date).exists():
#         # Redirect or display an error message indicating that the user has already filled the attendance for today
#         messages.error(request, 'You have already filled the attendance for today.')
#         # return redirect('AttEntry')  # Update with the appropriate URL or template
    
#     if request.method == 'POST':
#         att1 = Attendance()
#         attform1 = AttForm1(request.POST, instance=att1)
        
#         if attform1.is_valid():
#             att1 = attform1.save(commit=False)
#             att1.user = request.user
#             att1.tdate = timezone.now()
#             att1.save()
            
#             for junior in juniors:
#                 att2 = Attendance()
#                 post_data = request.POST.copy()
#                 post_data['mapping'] = junior.id
#                 attform2 = AttForm2(post_data, instance=att2)
                
#                 if attform2.is_valid():
#                     att2 = attform2.save(commit=False)
#                     att2.user = request.user
#                     att2.tdate = att1.tdate
#                     att2.mapping = junior
#                     att2.attendance = request.POST.get(f"{junior.id}_attendance")
#                     att2.save()
        
#         return redirect('AttEntry')  # Update with the appropriate URL or template
    
#     else:
#         attform1 = AttForm1() 
#         attform2 = AttForm2() 
    
#     return render(request, "AttForm.html", {'attform1': attform1, 'attform2': attform2, 'juniors': juniors, 'names': names})
#################################################################################################################################
# @login_required(login_url='loginview')
# @never_cache
# def AttFormView(request):
#     juniors = Mapping.objects.filter(user=request.user)
#     names = Attendance.objects.filter(user=request.user)

#     # Get the current date
#     current_date = timezone.now().date()

#     # Check if the user has already filled the attendance for the current date
#     if Attendance.objects.filter(user=request.user, tdate__date=current_date).exists():
#         # Add an error message indicating that the user has already filled the attendance for today
#         messages.error(request, 'You have already filled the attendance for today.')
#         return redirect('AttEntry')  # Update with the appropriate URL or template

#     if request.method == 'POST':
#         attform1 = AttForm1(request.POST)
#         attform2 = AttForm2(request.POST)
        
#         if attform1.is_valid() and attform2.is_valid():
#             att1 = attform1.save(commit=False)
#             att1.user = request.user
#             att1.tdate = timezone.now()
#             att1.save()
            
#             for junior in juniors:
#                 att2 = Attendance()
#                 att2.user = request.user
#                 att2.tdate = att1.tdate
#                 att2.mapping = junior
#                 att2.attendance = request.POST.get(f"{junior.id}_attendance")
#                 att2.save()
        
#         return redirect('AttEntry')  # Update with the appropriate URL or template
    
#     else:
#         attform1 = AttForm1() 
#         attform2 = AttForm2() 
    
#     messages_to_render = messages.get_messages(request)
    
#     return render(request, "AttForm.html", {'attform1': attform1, 'attform2': attform2, 'juniors': juniors, 'names': names, 'messages': messages_to_render})
#################################################################################################################################

# Attendance Entries View
@login_required(login_url='loginview')
@never_cache
def AttEntry(request):
    # data = Attendance.objects.all()
    data = Attendance.objects.filter(user=request.user)
    juniors  = Mapping.objects.filter(user=request.user)
    # jratt = JrAttendance.objects.filter(user=request.user)
    template = loader.get_template('AttEntry.html')
    context = {
        'attdata': data,
        'juniorsatt': juniors,
        # 'jratt': jratt,
    }

    return HttpResponse(template.render(context, request))

# Pending Approval Task List
# @login_required(login_url='loginview')
# @never_cache
# def tasklist(request):
#     logged_in_user = request.user
#     junior_ids = Mapping.objects.filter(user=logged_in_user).values_list('junior', flat=True)
#     att_data = Attendance.objects.filter(user__id__in=junior_ids, mapping=None)
#     template = loader.get_template('TaskList.html')
#     context = {'att_data': att_data, 'username': request.user.username, 'junior_ids': junior_ids}
#     return HttpResponse(template.render(context, request))

@login_required(login_url='loginview')
@never_cache
def tasklist(request):
    logged_in_user = request.user
    junior_ids = Mapping.objects.filter(user=logged_in_user).values_list('junior', flat=True)
    
    if logged_in_user.is_superuser:
        att_data = Attendance.objects.filter(mapping=None)
        # att_data = Attendance.objects.all()
        # att_data = Attendance.objects.filter(user=request.user)
    else:
        att_data = Attendance.objects.filter(user__id__in=junior_ids, mapping=None)
    
    template = loader.get_template('TaskList.html')
    context = {'att_data': att_data, 'username': request.user.username, 'junior_ids': junior_ids}
    return HttpResponse(template.render(context, request))

# Approved Task List
@login_required(login_url='loginview')
@never_cache
def TLUpdate(request, pk):
    att = get_object_or_404(Attendance, pk=pk)

    if request.method == 'POST':
        attform1 = AttForm1(request.POST, instance=att)

        if attform1.is_valid():
            attform1.instance.user = att.user
            attform1.instance.tdate = att.tdate
            attform1.save()
            return redirect('tasklist')
        
        print(attform1.errors)

    else:
        attform1 = AttForm1(instance=att)

    return render(request, 'TLUpdate.html', {'attform1': attform1, 'att': att})

#function to approve the task (button)
@login_required(login_url='loginview')
@never_cache
def approve_task(request, pk):
    task = Attendance.objects.get(id=pk)
    ApprovedAtt.objects.create(
        user=request.user,
        name = task.user,
        tdate=task.tdate,
        attendance=task.attendance,
        mapping = task.mapping
    )
    task.delete()
    return redirect('tasklist')  # Redirect to the original page with the updated task list

#to display all approved tasks
@login_required(login_url='loginview')
@never_cache
def approval_list(request):
    logged_in_user = request.user

    if logged_in_user.is_superuser:
        approved_tasks = ApprovedAtt.objects.all()
    else:
        approved_tasks = ApprovedAtt.objects.filter(user=request.user)
    return render(request, 'ApprovedTask.html', {'approved_tasks': approved_tasks})

# def approval_list(request):
#     one_day_ago = datetime.now() - timedelta(days=1)
#     approved_tasks = ApprovedAtt.objects.filter(approved_timestamp__gte=one_day_ago)
#     return render(request, 'ApprovedTask.html', {'approved_tasks': approved_tasks})

#Company Form View
@login_required(login_url='loginview')
@never_cache
def CompanyDetail(request):
    company = Company()  # create an object for the shared model
    entry_count = Company.objects.count()
    if entry_count == 1:
        return render(request, template_name="error.html", context={"error":"You can add only 1 entry, you need to delete the previous one!"})

    if request.method == 'POST':
        compform1 = CompForm1(request.POST, instance=company)  # pass the object to both forms
        compform2 = CompForm2(request.POST, instance=company)
        if compform1.is_valid() and compform2.is_valid():
            compform1.save()  # save the object if both forms are valid
            compform2.save()
            return redirect('CompanyEntry')
    else:
        compform1 = CompForm1(instance=company)  # pass the object to both forms
        compform2 = CompForm2(instance=company)
    return render(request, "CompanyDetail.html", {'compform1': compform1, 'compform2': compform2})

#Company Detail View
@login_required(login_url='loginview')
@never_cache
def CompanyEntry(request):
    data = Company.objects.all()
    template = loader.get_template('CompanyEntry.html')
    context = {
        'compdata': data,
    }

    return HttpResponse(template.render(context, request))

#Company Entry Update View
@login_required(login_url='loginview')
@never_cache
def CompUpdate(request, pk):
    comp = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        compform1 = CompForm1(request.POST, instance=comp)
        compform2 = CompForm2(request.POST, instance=comp)
        
        if compform1.is_valid() and compform2.is_valid():
            compform1.save()
            compform2.save()
            return redirect('CompanyEntry')

    else:
        compform1 = CompForm1(instance=comp)
        compform2 = CompForm2(instance=comp)

    return render(request, 'CompanyUpdate.html', {'compform1': compform1, 'compform2': compform2, 'comp':comp})

#Company Entry Delete View
@login_required(login_url='loginview')
@never_cache
def CompDelete(request, pk, template_name='delete_confirm_comp.html'):
    comp= get_object_or_404(Company, pk=pk)    
    if request.method=='POST':
        comp.delete()
        return redirect('CompanyEntry')
    return render(request, template_name, {'object':comp})

#Summary Page View
# @login_required(login_url='loginview')
# @never_cache
# def summary(request):
#     approved_tasks = ApprovedAtt.objects.all()
#     year = datetime.now().year

#     # month = datetime.now().month
#     # month_name = datetime.now().strftime('%B')

#     # Get the selected month from the request GET parameters
#     month = int(request.GET.get('month', datetime.now().month))
#     month_name = datetime(year, month, 1).strftime('%B')

#     total_working_days = 0
#     total_weekends = 0
#     employee_counts = {}  # Dictionary to store the counts for each employee

#     # Perform computation for each approved task
#     for task in approved_tasks:
#         employee = task.name  # Assuming you have an 'employee' field in the ApprovedAtt model
#         if employee not in employee_counts:
#             employee_counts[employee] = {
#                 'fullday': 0,
#                 'halfday': 0,
#                 'overtime': 0,
#                 'absent': 0,
#             }

#         attendance = task.attendance
#         fullday = attendance.count('Full Day')
#         halfday = attendance.count('Half Day')
#         overtime = attendance.count('Overtime')
#         absent = attendance.count('Absent')

#         employee_counts[employee]['fullday'] += fullday
#         employee_counts[employee]['halfday'] += halfday
#         employee_counts[employee]['overtime'] += overtime
#         employee_counts[employee]['absent'] += absent

#     # Iterate over the days of the month
#     current_day = datetime(year, month, 1).date()
#     last_day = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

#     # Convert current_day to datetime.datetime object
#     current_day = datetime.combine(current_day, datetime.min.time())

#     while current_day <= last_day:
#         if current_day.weekday() < 5:  # Check if the day is a weekday (Monday to Friday)
#             total_working_days += 1
#         else:  # Check if the day is a weekend day (Saturday or Sunday)
#             total_weekends += 1
#         current_day += timedelta(days=1)

#     context = {
#         'employee_counts': employee_counts,
#         'approved_tasks': approved_tasks,
#         'total_working_days': total_working_days,
#         'total_weekends': total_weekends,
#         'month_name': month_name,
#     }

#     return render(request, 'summary.html', context)

@login_required(login_url='loginview')
@never_cache
def summary(request):
    approved_tasks = ApprovedAtt.objects.all()
    year = datetime.now().year

    # Get the selected month from the request GET parameters
    # month = int(request.GET.get('month', datetime.now().month))
    selected_month = int(request.GET.get('month', datetime.now().month))
    month_name = datetime(year, selected_month, 1).strftime('%B')

    # Filter the approved_tasks by the selected month
    approved_tasks = approved_tasks.filter(tdate__year=year, tdate__month=selected_month)

    total_working_days = 0
    total_weekends = 0
    employee_counts = {}

    # Perform computation for each approved task
    for task in approved_tasks:
        employee = task.name  # Assuming you have an 'employee' field in the ApprovedAtt model
        if employee not in employee_counts:
            employee_counts[employee] = {
                'fullday': 0,
                'halfday': 0,
                'overtime': 0,
                'absent': 0,
            }

        attendance = task.attendance
        fullday = attendance.count('Full Day')
        halfday = attendance.count('Half Day')
        overtime = attendance.count('Overtime')
        absent = attendance.count('Absent')

        employee_counts[employee]['fullday'] += fullday
        employee_counts[employee]['halfday'] += halfday
        employee_counts[employee]['overtime'] += overtime
        employee_counts[employee]['absent'] += absent

    # Iterate over the days of the month
    current_day = datetime(year, selected_month, 1).date()
    last_day = (datetime(year, selected_month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Convert current_day to datetime.datetime object
    current_day = datetime.combine(current_day, datetime.min.time())

    while current_day <= last_day:
        if current_day.weekday() < 5:  # Check if the day is a weekday (Monday to Friday)
            total_working_days += 1
        else:  # Check if the day is a weekend day (Saturday or Sunday)
            total_weekends += 1
        current_day += timedelta(days=1)

    # Get the current month and list of months for the dropdown
    current_month = datetime.now().month
    months = [
        (month_number, datetime(year, month_number, 1).strftime('%B'))
        for month_number in range(1, 13)
    ]


    context = {
        'employee_counts': employee_counts,
        'approved_tasks': approved_tasks,
        'total_working_days': total_working_days,
        'total_weekends': total_weekends,
        'month_name': month_name,
        'current_month': current_month,
        'months': months,
        'selected_month': selected_month,
    }

    return render(request, 'summary.html', context)


#Summary Page View
# @login_required(login_url='loginview')
# @never_cache
# def summary_detail(request):
#     data = ApprovedAtt.objects.all()
#     template = loader.get_template('summary_detail.html')
#     context = {'username': request.user.username, 'data': data}
#     return HttpResponse(template.render(context, request))

@login_required(login_url='loginview')
@never_cache
def summary_detail(request):
    employee_id = request.GET.get('employee_id')  # Assuming the employee ID is passed as a query parameter
    employee = User.objects.get(id=employee_id)
    approved_att = ApprovedAtt.objects.filter(name=employee)

    template = loader.get_template('summary_detail.html')
    context = {
        'username': request.user.username,
        'employee': employee,
        'approved_att': approved_att,
    }
    return HttpResponse(template.render(context, request))


#####################################################################################################################################
# def signin(request):
#     if request.method == 'POST':
#         fm = SigninForm(request.POST)
#         if fm.is_valid():
#             email = fm.cleaned_data.get('email')
#             # Set username to the entered email
#             username = email

#             # Check if the username is already taken
#             if User.objects.filter(username=username).exists():
#                 return HttpResponse("Username already exists")

#             # Create the user with email as username
#             # user = fm.save(commit=False)
#             # user.username = username
#             # user.is_active = False
#             # user.save()

#             # Set other user details
#             first_name = fm.cleaned_data.get('first_name')
#             last_name = fm.cleaned_data.get('last_name')
#             role = fm.cleaned_data.get('role')
#             # group_name = ' '

#             # # Add the user to a group

#             group_name = ''
#             if role == 'HR':
#                 group_name = 'HR'
#                 is_staff = True
#                 is_superuser = False

#             elif role == 'Manager':
#                 group_name = 'Manager'
#                 is_staff = True
#                 is_superuser = False

#             else:
#                 group_name = 'Admin'
#                 is_staff = True
#                 is_superuser = True


#             # user = User.objects.get(email=email, first_name=first_name, last_name=last_name)
#             user = fm.save(commit=False)
#             user.username = username
#             user.is_active = False
#             # user.save()
#             user.is_staff = is_staff
#             user.is_superuser = is_superuser
#             user.save()

#             # group = Group.objects.get(name=group_name)
#             # user.groups.add(group)

#             # Create user data object
#             user_data = UserData.objects.create(user=user, role=role)
#             user_data.save()

#             group = Group.objects.get(name=group_name)
#             user.groups.add(group)

#             # Send activation email
#             messages.success(request, "Your account has been successfully created. Kindly confirm your mail to activate your account from the confirmation email!")

#             activateEmail(request, user, email)

#             # activateEmail(request, user, email)

#             return redirect('loginview')
#     else:
#         fm = SigninForm()
#     return render(request, 'signin.html', {'form': fm})


# #SignIn page View
# def signin(request):
#     if request.method == 'POST':
#         fm = SigninForm(request.POST)
#         if fm.is_valid():
#             user=fm.save(commit=False)
#             user.is_active=False
#             user.save()
#             username = fm.cleaned_data.get('username')
#             email = fm.cleaned_data.get('email')
#             first_name = fm.cleaned_data.get('first_name')
#             last_name = fm.cleaned_data.get('last_name')
#             role = fm.cleaned_data.get('role')

#             # group = Group.objects.get(name = 'HR')
#             # user.groups.add(group)

            # group_name = ''
            # if role == 'HR':
            #     group_name = 'HR'
            #     is_staff = True
            #     is_superuser = False
            #     print(f'is_staff: {is_staff}, is_superuser: {is_superuser}')

            # elif role == 'Manager':
            #     group_name = 'Manager'
            #     is_staff = True
            #     is_superuser = False
            #     print(f'is_staff: {is_staff}, is_superuser: {is_superuser}')

#             # elif role == 'Admin':
#             #     group_name = 'Admin'
#             #     is_staff = True
#             #     is_superuser = True
#             #     print(f'is_staff: {is_staff}, is_superuser: {is_superuser}')

#             # else:
#             #     group_name = 'Employee'
#             #     is_staff = False
#             #     is_superuser = False
#             #     print(f'is_staff: {is_staff}, is_superuser: {is_superuser}')

#             user = User.objects.get(username=username, email=email, first_name=first_name, last_name=last_name)

#             # user.is_staff = is_staff
#             # user.is_superuser = is_superuser
#             user.save()

#             user_data = UserData.objects.create(user=user, role=role)
#             user_data.save()

#             # group = Group.objects.get(name=group_name)
#             # user.groups.add(group)

#             # messages.success(request, "Your account has been successfully created. Kindly confirm your mail to activate your account from the confirmation email!")

#             activateEmail(request, user, email)

#             return redirect('loginview')

#     else:
#         fm = SigninForm()

#     return render(request, 'signin.html', {'form': fm})

#View for the activation of account by link after sign up
# def activateEmail(request, user, to_email):
#     mail_subject = 'Activate your user account.'
#     message = render_to_string('acc_active_email.html', {
#         'user': user.first_name,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         'protocol': 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'Dear {user}, Your account has been successfully created. please go to you email {to_email} inbox and click on received activation link to confirm and complete the registration. Note: Check your spam folder.')
#     else:
#         messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

# #View for the sucessful activation of account
# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, '\nThank you for your email confirmation. Now you can login your account.')
#         return redirect('loginview')
#     else:
#         messages.error(request, 'Activation link is invalid!')
#     return redirect('loginview')