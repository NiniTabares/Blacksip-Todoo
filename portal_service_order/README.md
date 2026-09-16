# Portal - Órdenes de servicio

Módulo para Odoo 18 que cambia la denominación visual de las cotizaciones y
pedidos de venta en el portal del cliente.

## Cambios incluidos

- `Cotización - CC...` pasa a `Orden de servicio - CC...`.
- `Cotizaciones` y `Órdenes de venta` pasan a `Órdenes de servicio` en las
  migas de navegación.
- `Cotización CC...` pasa a `Orden de servicio CC...` en el documento abierto.

El módulo no modifica estados, secuencias, rutas, aceptación, firma, pagos,
correos ni reportes PDF.

## Instalación en Odoo.sh

1. Copiar la carpeta `portal_service_order` dentro del repositorio de addons.
2. Confirmar y enviar los cambios a la rama de Odoo.sh.
3. Esperar a que termine la compilación.
4. Activar el modo desarrollador y actualizar la lista de aplicaciones.
5. Buscar `Portal - Órdenes de servicio` e instalar el módulo.
6. Probar una cotización enviada usando el enlace del portal en una ventana
   privada.

