from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, MeasurementForm
from .models import Measurement
from django.db.models import Q

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Measurement
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
# views.py

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(0)  # Session expire après un an
        return super().form_valid(form)

@login_required
def download_all_measurements_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="la liste_de_tout_mesures.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    measurements = Measurement.objects.filter(user=request.user)
    
    # Create a stylesheet
    styles = getSampleStyleSheet()
    style_ul = ParagraphStyle(
        'ul',
        parent=styles['BodyText'],
        bulletFontName='Helvetica',
        bulletFontSize=10,
        bulletIndent=0,
        leftIndent=20,
    )
    style_li = ParagraphStyle(
        'li',
        parent=styles['BodyText'],
        leftIndent=40,
        rightIndent=20,
        firstLineIndent=0,
        spaceBefore=5,
        spaceAfter=5,
    )

    y = height - 40
    p.setFillColor(colors.darkblue)
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2.0, y, "La liste de tout les mesures")
    y -= 20

    for measurement in measurements:
        p.setFillColor(colors.darkblue)
        p.drawString(100, y, f"Nom du client: {measurement.name}")
        y -= 20
        if measurement.habit:
            p.setFillColor(colors.darkblue)
            p.drawString(100, y, f"Mesure de l'habit: {measurement.habit}")
            y -= 20
        if measurement.pant_size:
            p.setFillColor(colors.darkblue)
            p.drawString(100, y, f"Mesure du pantalon: {measurement.pant_size}")
            y -= 20
        if measurement.phone_number:
            p.setFillColor(colors.darkblue)
            p.drawString(100, y, f"Numéro de téléphone: {measurement.phone_number}")
            y -= 20
        p.setFillColor(colors.darkblue)
        p.drawString(100, y, f"Date: {measurement.date}")
        y -= 40  # Add extra space between measurements

    p.showPage()
    p.save()
    return response

@login_required
def download_measurement_pdf(request, pk):
    measurement = Measurement.objects.get(pk=pk, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="mesurepro_{request.user.username}_{measurement.name}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Create a stylesheet
    styles = getSampleStyleSheet()
    style_ul = ParagraphStyle(
        'ul',
        parent=styles['BodyText'],
        bulletFontName='Helvetica',
        bulletFontSize=10,
        bulletIndent=0,
        leftIndent=20,
    )
    style_li = ParagraphStyle(
        'li',
        parent=styles['BodyText'],
        leftIndent=40,
        rightIndent=20,
        firstLineIndent=0,
        spaceBefore=5,
        spaceAfter=5,
    )

    y = height - 40
    p.setFillColor(colors.darkblue)
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2.0, y, "Les détails de la mesures")
    y -= 20

    p.setFillColor(colors.darkblue)
    p.drawString(100, y, f"Nom du client: {measurement.name}")
    y -= 20
    if measurement.habit:
        p.setFillColor(colors.darkblue)
        p.drawString(100, y, f"Mesure de l'habit: {measurement.habit}")
        y -= 20
    if measurement.pant_size:
        p.setFillColor(colors.darkblue)
        p.drawString(100, y, f"Mesure du pantalon: {measurement.pant_size}")
        y -= 20
    if measurement.phone_number:
        p.setFillColor(colors.darkblue)
        p.drawString(100, y, f"Numéro de téléphone: {measurement.phone_number}")
        y -= 20
    p.setFillColor(colors.darkblue)
    p.drawString(100, y, f"Date: {measurement.date}")
    
    
    p.showPage()
    p.save()
    return response


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    print(request)
    return render(request, 'index.html')



@login_required
def dashboard_view(request):
    measurements = Measurement.objects.filter(user=request.user).order_by('-date')
    query = request.GET.get('q')
    if query:
        measurements = measurements.filter(Q(name__icontains=query) | Q(date__icontains=query))
        
   # measurements = Measurement.objects.all().order_by('-published_date')
    return render(request, 'dashboard.html', {'measurements': measurements})

@login_required
def add_measurement_view(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            return redirect('dashboard')
    else:
        form = MeasurementForm()
    return render(request, 'add_measurement.html', {'form': form})

@login_required
def edit_measurement_view(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MeasurementForm(instance=measurement)
    return render(request, 'edit_measurement.html', {'form': form})

@login_required
def delete_measurement_view(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)
    if request.method == 'POST':
        measurement.delete()
        return redirect('dashboard')
    return render(request, 'delete_measurement.html', {'measurement': measurement})
