"""Offline validation; never modifies or sends an invoice.
Usage: python tools/validate_xml.py invoice.xml [accepted.zip ...]
Requires lxml. Accepts Invoice, AttachedDocument and ZIP with XML.
"""
import argparse
from decimal import Decimal
import importlib.util
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

helper = Path(__file__).resolve().parents[1] / 'models' / 'subtotal_order.py'
spec = importlib.util.spec_from_file_location('subtotal_order', helper)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
NS = {
    'a': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
    'b': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
}


def invoices(raw):
    root = etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
    if etree.QName(root).localname == 'Invoice':
        yield root
    elif etree.QName(root).localname == 'AttachedDocument':
        for description in root.xpath('//b:Description', namespaces=NS):
            text = description.text or ''
            if text.lstrip().startswith('<'):
                yield from invoices(text.encode())


def check(raw):
    for root in invoices(raw):
        print('FACTURA:', root.findtext('b:ID', namespaces=NS))
        failing = 0
        changed = 0
        for block in root.xpath('//a:WithholdingTaxTotal', namespaces=NS):
            subtotals = block.findall('a:TaxSubtotal', NS)
            values = [item.findtext('b:TaxAmount', namespaces=NS) for item in subtotals]
            total = block.findtext('b:TaxAmount', namespaces=NS)
            decimal_ok = Decimal(total) == sum(map(Decimal, values), Decimal('0'))
            xpath_ok = block.xpath('number(b:TaxAmount)=sum(a:TaxSubtotal/b:TaxAmount)', namespaces=NS)
            if not xpath_ok:
                failing += 1
                print('  XPATH FALLA:', block.getroottree().getpath(block), values, 'total', total,
                      'suma XPath', repr(block.xpath('sum(a:TaxSubtotal/b:TaxAmount)', namespaces=NS)),
                      'decimal correcto', decimal_ok)
            order = module.stable_order(total, values)
            if order != tuple(range(len(subtotals))):
                changed += 1
                for item in subtotals:
                    block.remove(item)
                for index in order:
                    block.append(subtotals[index])
                print('  ORDEN PROPUESTO:', [values[index] for index in order])
            if decimal_ok:
                assert block.xpath('number(b:TaxAmount)=sum(a:TaxSubtotal/b:TaxAmount)', namespaces=NS), 'XPath sigue fallando'
            else:
                raise AssertionError('Diferencia decimal real: no se corrige reordenando')
        print('  Bloques fallidos antes:', failing, '| Reordenados:', changed, '| XPath final: OK')
        print('  Simulación en memoria; archivo firmado original conservado.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    for filename in args.files:
        path = Path(filename)
        if path.suffix.lower() == '.zip':
            with ZipFile(path) as archive:
                for name in archive.namelist():
                    if name.lower().endswith('.xml'):
                        check(archive.read(name))
        else:
            check(path.read_bytes())
