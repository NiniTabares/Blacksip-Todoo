# Corrección experimental FAY02 para Odoo 18 / DIAN directa

Versión 18.0.1.0.0. Dependencia: l10n_co_dian.

## Hallazgo reproducible

Se validaron los XML proporcionados por el cliente con lxml/libxml2 XPath 1.0.
La comparación utilizada fue:

    number(cbc:TaxAmount) = sum(cac:TaxSubtotal/cbc:TaxAmount)

En EXY13332 falla en los bloques ReteRenta de las líneas 1, 3 y 4, aunque los
importes con aritmética decimal exacta coinciden. En EXY13331 aceptada pasan
los diez bloques. Reordenar los subtotales permite que pasen los diez bloques
de EXY13332. No hay cambios en base, importe, tarifa, impuestos o cuentas.

| Línea | Total declarado | Suma binaria XPath original | Nuevo orden de importes |
|---|---:|---:|---|
| 1 | 1642.50 | 1642.5000000000002 | 291.41, 291.41, 1059.68 |
| 3 | 333015.02 | 333015.01999999996 | 59083.31, 59083.31, 214848.40 |
| 4 | 23311.08 | 23311.079999999998 | 4135.84, 4135.84, 15039.40 |

Esto es una hipótesis técnica fuerte y una reproducción local de una condición
compatible con FAY02. No prueba el motor interno usado por DIAN. La aceptación
remota debe verificarse con el nuevo envío; no se ha ejecutado desde este entorno.
Referencia: https://www.w3.org/TR/xpath-10/ (números IEEE 754 y función sum).

## Alcance

El módulo hereda account.edi.xml.ubl_dian y cubre los dos métodos del código
aportado por el cliente: _dian_tax_totals (ruta anterior) y _get_tax_total_node
(ruta de nodos). El reordenamiento ocurre antes de firmar el documento.
No interviene sobre XML ya firmado. No requiere campos ni configuración.
Conserva las dos autorretenciones y sus cuentas; no aplicar el módulo de
exclusión sugerido antes durante el diagnóstico.

La función solo cambia el orden si la suma decimal es exactamente correcta y
el orden actual falla en la suma binaria. Busca primero ascendente/descendente;
para hasta siete subtotales explora permutaciones. Si no encuentra un orden
válido conserva el original y registra advertencia. No garantiza resolver
cualquier caso FAY02, diferencias monetarias reales ni otros validadores.

## Instalación en Odoo.sh

1. Extraer la carpeta l10n_co_dian_fay02_order y añadirla al repositorio de addons.
2. Desplegar primero en staging, actualizar lista de aplicaciones e instalar
   'Colombia DIAN - Orden de subtotales FAY02'. No es un módulo de importación
   por la interfaz: utilizar el flujo Git habitual de Odoo.sh.
3. No habilitar credenciales ni envíos de producción desde staging.
4. Validar la instalación y generar el XML mediante el flujo de generación
   disponible en ese entorno. Si la generación requiere enviar, usar únicamente
   un entorno DIAN de pruebas configurado apropiadamente; no transmitir una
   copia de la factura real desde staging al servicio productivo.
5. Confirmar que en el XML generado los subtotales de ReteRenta de las líneas
   1, 3 y 4 estén ordenados como la tabla y conserven exactamente sus importes.
6. Confirmar saldo por cobrar 6.577.538,07 y ausencia de cambios contables.
7. Tras validar instalación y generación, desplegar el mismo módulo en la rama
   productiva e instalarlo. Conservar historial y adjuntos del rechazo.
8. Usar el flujo estándar que ya regeneró el XML del cliente para firmar y
   enviar EXY13332. Verificar nueva firma y orden de subtotales. No editar la
   firma ni cambiar secuencia, impuestos, importes, CUFE o estados por SQL.
9. Consultar la respuesta: solo estado aceptado en DIAN confirma la solución.
   Ante duplicado, consultar el estado del CUFE antes de otro envío.

El módulo aplica a futuras generaciones de retenciones de la integración
DIAN directa en la base donde se instala, no exclusivamente a EXY13332.
No modifica documentos anteriores ni los reenvía automáticamente.
Para revertir, desinstalarlo; los documentos ya aceptados se conservan.

## Verificación local independiente

Con Python y lxml:

    python tools/validate_xml.py dian_EXY13332.xml EXY13331.zip

El verificador abre el XML o el contenedor AttachedDocument, prueba XPath y
simula el orden en memoria. No escribe un XML modificado y no envía a DIAN.

## Validación realizada

- EXY13332 real: diez bloques revisados; tres fallos originales; cero tras
  reordenar los tres bloques afectados.
- EXY13331 aceptada: diez bloques pasan; ningún bloque reordenado.
- Importes de subtotales, categorías y totales conservados.
- Comprobaciones unitarias de las dos rutas mediante dobles del ORM.
- Compilación Python correcta.
- Instalación en Odoo, renderizado real del exportador y aceptación DIAN:
  pendientes de validar en el entorno del cliente.
