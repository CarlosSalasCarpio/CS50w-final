from fileinput import filename
import requests
from django.http import StreamingHttpResponse, FileResponse
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .utils import csv_to_models, current_date_format, link_callback 
from .models import Employees, Desprendibles
import io
import os
from django.http import HttpResponse
from django.views.generic import View
from datetime import datetime
from xhtml2pdf import pisa
from django.template.loader import get_template
import urllib.request
import re
from PyPDF2 import PdfFileReader, PdfFileWriter


# Register form
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True, label='Correo electrónico')
	username = forms.CharField(required=True, label='Número de identificación')
	password1 = forms.CharField(label='Contraseña',
	widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirmar contraseña',
 	widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


# Upload CSV form
class UploadFileForm(forms.Form):
	file = forms.FileField(label=False)


# Upload PDF form
class DesprendiblesForm(forms.ModelForm):
	fortnight= (
		('First','First'),
		('Second','Second'),
	)

	month= (
		('January','January'),
		('February','February'),
		('March','March'),
		('April','April'),
		('May','May'),
		('June','June'),
		('July','July'),
		('August ','August '),
		('September','September'),
		('October','October'),
		('November','November'),
		('December','December'),
	)

	year= (
		('2020','2020'),
		('2021','2021'),
		('2022','2022'),
		('2023','2023'),
		('2024','2024'),
		('2025','2025'),
		('2026','2026'),
		('2027','2027'),
		('2028','2028'),
		('2029','2029'),
		('2030','2030'),
	)

	fortnight = forms.ChoiceField(widget=forms.Select, choices=fortnight)
	month = forms.ChoiceField(widget=forms.Select, choices=month)
	year = forms.ChoiceField(widget=forms.Select, choices=year)

	class Meta:
		model = Desprendibles
		fields = ('fortnight', 'month', 'year', 'pdf')


# User login
def login_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if not user.is_staff:
				return HttpResponseRedirect(reverse("index"))
			else:
				return HttpResponseRedirect(reverse("admin_main"))
		else:
			return render(request, "pdf_manager/login.html", {
			"message": "Credenciales incorrectas"
			})
	else:
		return render(request, "pdf_manager/login.html")


# User logout
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("login"))


# New user register
def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)

		# If user id is not within employees table or already registered
		if Employees.objects.filter(NÚMERODEIDENTIFICACIÓN = request.POST['username']).exists() == False or User.objects.filter(username = request.POST['username']).exists() == True:
			message = "Número de identificación no válido"
			return render (request, "pdf_manager/register.html", context={
				"register_form": form,
				'message': message
			})

		# If email entered is not from the company (here you can set the email providers accepted)
		#elif '@example.com' not in str(request.POST['email']) and '@example2.com' not in str(request.POST['email']):
		#	message = "Correo no válido, asegurese de utilizar un correo @example.com o @example2.com"
		#	return render (request, "pdf_manager/register.html", context={
		#		"register_form": form,
		#		'message': message
		#	})

		# Form is valid, user to be registered successfully
		elif form.is_valid():
			form.save()
			messages.success(request, "Registration successful." )
			message = "Registro exitoso"
			return render (request, "pdf_manager/register_success.html", context={
				'message': message
			})

		# Form is not valid
		else:
			message = "Información invalida"
			return render (request, "pdf_manager/register.html", context={
				"register_form": form,
				'message': message
			})

	form = NewUserForm()
	return render (request, "pdf_manager/register.html", context={
		"register_form": form
	})


# From index users can download payroll stud or labor certificate
@login_required
def index(request):
	if request.user.is_staff:
		return HttpResponseRedirect(reverse("admin_main"))
	else:
		desprendibles = Desprendibles.objects.all()
		return render(request, 'pdf_manager/user.html', {
			'username': request.user.username,
			'email': request.user.email,
			'desprendibles': desprendibles
		})


# HR can choose to update PDF for (desprendibles) or CSV for (certificados)
@login_required
def admin_main(request):
	form_csv = UploadFileForm(request.POST, request.FILES)
	form_pdf = DesprendiblesForm()
	desprendibles = Desprendibles.objects.all()

	if request.method == 'GET':
		if request.user.is_staff:
			return render(request, 'pdf_manager/admin.html', {
				'upload_csv_form': form_csv,
				'upload_pdf_form': form_pdf,
				'desprendibles': desprendibles
			})
		else:
			return HttpResponseRedirect(reverse("index"))

	elif request.method == 'POST':

		# Upload .CSV
		if request.POST['submit_button'] == 'csv':
			if form_csv.is_valid() and str(os.path.splitext(request.FILES['file'].name)[1]) == '.csv':
				csv_file = request.FILES['file']
				csv_file = csv_file.read().decode('utf-8')
				csv_file = io.StringIO(csv_file)
				csv_to_models(csv_file)
				message_success = 'Información de empleados actualizada correctamente'
				return render(request, 'pdf_manager/admin.html', {
					'upload_csv_form': form_csv,
					'upload_pdf_form': form_pdf,
					'desprendibles': desprendibles,
					'message_success': message_success
				})
			else:
				message = 'Documento no válido, por vafor verifique que la extensión del documento es .csv'
				return render(request, 'pdf_manager/admin.html', {
					'upload_csv_form': form_csv,
					'upload_pdf_form': form_pdf,
					'desprendibles': desprendibles,
					'message': message
				})

		# Upload .PDF	
		if request.POST['submit_button'] == 'pdf':
			form = DesprendiblesForm(request.POST, request.FILES)
			doc_extension_is_pdf = str(os.path.splitext(request.FILES['pdf'].name)[1]) == '.pdf'
			doc_exists = Desprendibles.objects.filter(fortnight=form['fortnight'].value(), month=form['month'].value(), year=form['year'].value()).exists()
			print(doc_extension_is_pdf)
			print(doc_exists)

			if form.is_valid() and doc_extension_is_pdf == False:
				message = 'Documento no válido, por vafor verifique que la extensión del documento es .pdf'
				return render(request, 'pdf_manager/admin.html', {
					'upload_csv_form': form_csv,
					'upload_pdf_form': form_pdf,
					'desprendibles': desprendibles,
					'message': message
				})
			
			elif form.is_valid() and doc_extension_is_pdf and doc_exists  == False:			
				form.save()
				message_success = 'Documento cargado de forma exitosa'
				return render(request, 'pdf_manager/admin.html', {
					'upload_csv_form': form_csv,
					'upload_pdf_form': form_pdf,
					'desprendibles': desprendibles,
					'message_success': message_success
				})

			elif form.is_valid() and doc_exists:
				message = 'El documento que intenta cargar ya existe, si desea cargarlo nuevamente por favor elimine el existente'
				return render(request, 'pdf_manager/admin.html', {
					'upload_csv_form': form_csv,
					'upload_pdf_form': form_pdf,
					'desprendibles': desprendibles,
					'message': message
				})

			else:
				message = "Error, Por favor verifique los datos ingresados"
				return render(request, 'pdf_manager/admin.html', {
					'upload_csv_form': form_csv,
					'upload_pdf_form': form_pdf,
					'desprendibles': desprendibles,
					'message': message
				})	


# HR can delete desprendibles
@login_required
def delete_desprendible(request, pk):
	if request.method == 'POST':
		desprendible = Desprendibles.objects.get(pk = pk)
		desprendible.delete()
	return redirect('admin_main')


# HR can download desprendibles
@login_required
def download_desprendible(request):
	if request.method == 'POST':
		file_location = request.POST.get('pdf_download')
		file_name = file_location.replace('media/', '')
		file = FileResponse(open(file_location, 'rb'), content_type='application/pdf')
		file['Content-Disposition'] = f'attachment; filename={file_name}'
		
		return file


# User can download certificados
@login_required
def download_certificado_user(request):
	if request.method == 'POST':
		name = Employees.objects.get(NÚMERODEIDENTIFICACIÓN = request.user.username).EMPLEADO
		document_type = Employees.objects.get(NÚMERODEIDENTIFICACIÓN = request.user.username).TIPODOCUMENTO
		id = request.user.username
		hire_date = Employees.objects.get(NÚMERODEIDENTIFICACIÓN = request.user.username).FECHADEINGRESO.replace("-", " de ")
		possition = Employees.objects.get(NÚMERODEIDENTIFICACIÓN = request.user.username).NOMBREDELCARGO
		contract_type = Employees.objects.get(NÚMERODEIDENTIFICACIÓN = request.user.username).TIPODECONTRATO
		salary = Employees.objects.get(NÚMERODEIDENTIFICACIÓN = request.user.username).VALORSUELDO
		company_db = Employees.objects.get(NÚMERODEIDENTIFICACIÓN = request.user.username).EMPRESA
		today = current_date_format(datetime.now())
		logo = 'pdf_manager/logo.JPG'
		firma = 'pdf_manager/firma.JPG'
		footer = 'pdf_manager/footer.JPG'

		template_path = 'pdf_manager/certificado.html'
		context = {
			'name': name,
			'document_type': document_type,
			'id': id,
			'hire_date': hire_date,
			'possition': possition,
			'contract_type': contract_type,
			'salary': salary,
			'company_db': company_db,
			'today': today,
			'logo': logo,
			'firma': firma,
			'footer': footer
			}
		# Create a Django response object, and specify content_type as pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="CERTIFICACIÓN_LABORAL.pdf"'
		# find the template and render it.
		template = get_template(template_path)
		html = template.render(context)

		# create a pdf
		pisa_status = pisa.CreatePDF(
			html, dest=response, link_callback=link_callback)
		return response