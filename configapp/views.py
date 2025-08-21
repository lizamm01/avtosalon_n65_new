import io
import qrcode
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from pyexpat.errors import messages
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from .forms import *
from .models import Autosalon, Brand, Car
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


def index(request):
    salon = Autosalon.objects.all()
    context = {'salon': salon, 'title': 'AUTOSALON'}
    return render(request, 'index.html', context)

def add_salon(request):
    if request.method == 'POST':
        form = AvtoSalonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AvtoSalonForm()
    return render(request, 'add_salon.html', {'form': form})

def detail_salon(request, pk):
    salon = get_object_or_404(Autosalon, pk=pk)
    return render(request, 'detail_salon.html', {'salon': salon})

def salon_cars(request, brand_pk, salon_pk):
    cars = Car.objects.filter(brand=brand_pk, salon=salon_pk)
    brand = Brand.objects.all()
    context = {
        "salon_pk": salon_pk,
        "cars": cars,
        "brand": brand
    }
    return render(request, 'salon_cars.html', context)

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})

from django.core.files.storage import default_storage

import io
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import qrcode
from PIL import Image, ImageDraw, ImageFont

from .models import Car

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "car_detail.html", {"car": car})


import io
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def detailed_pdf(request, car_id):
    # Ob'ektni olish
    from .models import Car
    car = Car.objects.get(id=car_id)

    # --- PDF tayyorlash ---
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="car_{car.id}.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # --- Ma'lumotlarni yozish ---
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"Model: {car.model}")
    p.drawString(100, 780, f"Brand: {car.brand.title}")
    p.drawString(100, 760, f"Salon: {car.salon.title}")
    p.drawString(100, 740, f"Price: ${car.price}")
    p.drawString(100, 720, f"Year: {car.year}")
    p.drawString(100, 700, f"Color: {car.color}")

    # --- QR kod yaratish (rasmni papkaga saqlamasdan) ---
    qr_data = f"Model: {car.model}, Price: {car.price}, Year: {car.year}"
    qr = qrcode.make(qr_data)

    qr_buffer = io.BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    # --- PDF ga QR kod qo‘shish ---
    from reportlab.lib.utils import ImageReader
    qr_image = ImageReader(qr_buffer)
    p.drawImage(qr_image, 350, 600, width=150, height=150)  # joylashuvini va o‘lchamini sozlash

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'ok')
            return redirect('home')
        else:
            messages.error(request, 'Username yoki parol xato')

    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
