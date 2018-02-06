from decimal import Decimal
from django.conf import settings
from Comedor.models import Product
from django.shortcuts import redirect
from .models import OrderItem
import weasyprint
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
import win32api
import win32print
from django.contrib import messages

def carrito_vacio(request, total):
	if total == 0:
		messages.info(request, 'Tu orden no puede estar vacía')	
		redirect('../../',permanent=True)

def imprimir(cart, order):
	html_string = render_to_string("orders/order/ticketTarjeta.html",{'cart':cart,"order": order})
	html= HTML(string= html_string)
	result = html.write_pdf("ticket.pdf")

	win32api.ShellExecute(0,"print","ticket.pdf", None ,".",0)
	win32api.ShellExecute(0,"print","ticket.pdf", None ,".",0)
