"""Run directly with Python; ORM doubles validate both integration hooks."""
from copy import deepcopy
from decimal import Decimal
import importlib.util
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
package = types.ModuleType('fay02_models')
package.__path__ = [str(ROOT / 'models')]
sys.modules['fay02_models'] = package


class Parent:
    def _dian_tax_totals(self, move, taxes_vals, withholding):
        return deepcopy(taxes_vals['fixture'])

    def _get_tax_total_node(self, vals):
        return deepcopy(vals['fixture'])

    def format_float(self, value, dp):
        return format(value, '.%df' % dp)


odoo = types.ModuleType('odoo')
odoo.models = types.SimpleNamespace(AbstractModel=Parent)
sys.modules['odoo'] = odoo
spec = importlib.util.spec_from_file_location(
    'fay02_models.account_edi_xml_ubl_dian',
    ROOT / 'models' / 'account_edi_xml_ubl_dian.py',
)
integration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integration)
from fay02_models.subtotal_order import stable_order


class TestOrder(unittest.TestCase):
    def test_three_problematic_blocks(self):
        for total, values in [
            ('1642.50', ['1059.68', '291.41', '291.41']),
            ('333015.02', ['214848.40', '59083.31', '59083.31']),
            ('23311.08', ['15039.40', '4135.84', '4135.84']),
        ]:
            order = stable_order(total, values)
            self.assertNotEqual(order, (0, 1, 2))
            result = 0.0
            for index in order:
                result += float(values[index])
            self.assertEqual(result, float(total))
            self.assertEqual(sum(map(Decimal, values)), Decimal(total))

    def test_correct_order_preserved(self):
        self.assertEqual(stable_order('11879.82', ['7664.40', '2107.71', '2107.71']), (0, 1, 2))

    def test_real_decimal_difference_preserved(self):
        self.assertEqual(stable_order('1642.51', ['1059.68', '291.41', '291.41']), (0, 1, 2))

    def test_invalid_data_preserved(self):
        self.assertEqual(stable_order('NaN', ['1', '2']), (0, 1))
        self.assertEqual(stable_order('3', ['invalid', '2']), (0, 1))

    def test_legacy_hook(self):
        model = integration.AccountEdiXmlUblDian()
        fixture = [{'currency_dp': 2, 'tax_amount': 1642.50, 'tax_subtotal_vals': [
            {'tax_amount': 1059.68, 'id': 1},
            {'tax_amount': 291.41, 'id': 2},
            {'tax_amount': 291.41, 'id': 3},
        ]}]
        output = model._dian_tax_totals(None, {'fixture': fixture}, True)
        self.assertEqual([v['id'] for v in output[0]['tax_subtotal_vals']], [2, 3, 1])
        self.assertEqual(model._dian_tax_totals(None, {'fixture': fixture}, False), fixture)
        self.assertEqual(output[0]['tax_amount'], fixture[0]['tax_amount'])

    def test_node_hook(self):
        model = integration.AccountEdiXmlUblDian()
        fixture = {'cbc:TaxAmount': {'_text': '1642.50', 'currencyID': 'COP'}, 'cac:TaxSubtotal': [
            {'cbc:TaxAmount': {'_text': value}, 'category': index}
            for index, value in enumerate(['1059.68', '291.41', '291.41'])
        ]}
        output = model._get_tax_total_node({'fixture': fixture, 'sign': -1})
        self.assertEqual([v['category'] for v in output['cac:TaxSubtotal']], [1, 2, 0])
        self.assertEqual(model._get_tax_total_node({'fixture': fixture}), fixture)
        self.assertEqual(output['cbc:TaxAmount'], fixture['cbc:TaxAmount'])
        self.assertCountEqual(output['cac:TaxSubtotal'], fixture['cac:TaxSubtotal'])


if __name__ == '__main__':
    unittest.main()
