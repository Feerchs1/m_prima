from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto

def home_cotizacion(request):
    productos = Producto.objects.all() # Trae los 2 productos disponibles
    
    if request.method == 'POST':
        empresa = request.POST.get('empresa')
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        
        producto = get_object_or_404(Producto, id=producto_id)
        
        # ⚠️ Validación de Stock exigida
        if cantidad > producto.stock:
            messages.error(request, f"Cantidad superior al stock. Stock disponible: {producto.stock}")
            return render(request, 'compras/formulario.html', {'productos': productos})
        
        # 📉 Restar del stock y guardar
        producto.stock -= cantidad
        producto.save()
        
        # Calcular total para el ticket
        total = producto.precio * cantidad
        
        # Guardamos los datos en la sesión temporal para mostrarlos en la página del ticket
        request.session['ticket_data'] = {
            'empresa': empresa,
            'producto_nombre': producto.nombre,
            'cantidad': cantidad,
            'total': float(total)
        }
        return redirect('ticket')

    return render(request, 'compras/formulario.html', {'productos': productos})

def ticket_view(request):
    # Recuperamos los datos de la compra actual
    context = request.session.get('ticket_data')
    if not context:
        return redirect('home_cotizacion')
    return render(request, 'compras/ticket.html', context)
