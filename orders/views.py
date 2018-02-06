from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm, OrderCashForm
from cart.cart import Cart
from django.db import connection
from django.contrib import messages
from django.template.loader import render_to_string
import weasyprint
from weasyprint import HTML, CSS
import win32api
import win32print
from . import ords
import re
	
def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		form2 = OrderCashForm(request.POST)
		if form2.is_valid():
			data = form2.cleaned_data
			order = form.save(commit = False)
			pago = data['Pago']
			total = cart.descuento_iva()
			if total == 0:
				messages.info(request, 'Tu orden no puede estar vacía')	
				return redirect('/../../')
			cambio = pago - total 
			order.totalcompra = total
			
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order,product= item['product'], price = item['price'], quantity=item['quantity'])
			
			cart.clear()
			
			imprimir(cart,order)
			return render(request, 'orders/order/createdEfectivo.html', {'order':order, 'cambio': cambio})
		elif form.is_valid():
			data = form.cleaned_data	
			nt = data['numerotarjeta']
			total = cart.get_total_price()
			if total == 0:
				messages.info(request, 'Tu orden no puede estar vacía')	
				return redirect('/../../')
			if len(nt) > 16 or len(nt) < 16:
				messages.info(request, 'Ingresaste una tarjeta no válida.')	
				return redirect('../pay')
			reg = re.search('(?<=\;)(.+?)(?=\?)', nt)
			if reg:
				numerotarjeta = reg.group(1)
			cursor = connection.cursor()
			query = cursor.execute('SELECT * FROM empleados WHERE Tarjeta = "%s"' % numerotarjeta)
			if query > 0 :
				nombres = cursor.fetchall()


				order = form.save(commit = False)
				order.nombre = str(nombres[0][0]+' '+nombres[0][2]+' '+nombres[0][1])
				order.numeroempleado= str(nombres[0][3])  
				order.totalcompra = cart.get_total_price()
				order.numerotarjeta = numerotarjeta
				order =  form.save()
				nom = str(nombres[0][0]) 
				total = cart.get_total_price()

				for item in cart:
					OrderItem.objects.create(order=order, product= item['product'], price = item['price'], quantity=item['quantity'])
				cart.clear()
				imprimir(cart,order)

				return render(request, 'orders/order/createdTarjeta.html', {'nombre':nom, 'total':total})			
			else:
				messages.info(request, 'Tu numero de tarjeta no se encuentra en la base de datos, porfavor intenta denuevo.')	
				return render(request, 'orders/order/payment.html')

		else:
			return render(request,'orders/order/payment.html')


	elif 'Tarjeta' in request.GET: 
		form = OrderCreateForm()
		return render(request, 'orders/order/ordentarjeta.html',{'cart':cart, 'form':form})
	else: 
		form = OrderCashForm()
		return render(request, 'orders/order/ordenefectivo.html',{'cart':cart, 'form':form})
		

def clear_session(request):
	cart = Cart(request)
	cart.clear()

	return redirect('/')

def payment(request):
	return render(request,'orders/order/payment.html')
	

def imprimir(cart, order):
	html_string = render_to_string("orders/order/ticketTarjeta.html",{'cart':cart,"order": order})
	html= HTML(string= html_string)
	result = html.write_pdf("ticket.pdf")

	win32api.ShellExecute(0,"print","ticket.pdf", None ,".",0)
	win32api.ShellExecute(0,"print","ticket.pdf", None ,".",0)

