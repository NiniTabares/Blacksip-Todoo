from odoo import models
from .subtotal_order import stable_order


class AccountEdiXmlUblDian(models.AbstractModel):
    _inherit = 'account.edi.xml.ubl_dian'

    def _dian_tax_totals(self, move, taxes_vals, withholding):
        # Legacy renderer, present in the customer-provided Odoo 18 code.
        totals = super()._dian_tax_totals(move, taxes_vals, withholding)
        if not withholding:
            return totals
        for total in totals:
            subtotals = total.get('tax_subtotal_vals', [])
            precision = total['currency_dp']
            order = stable_order(
                self.format_float(total['tax_amount'], precision),
                [self.format_float(item['tax_amount'], precision) for item in subtotals],
            )
            total['tax_subtotal_vals'] = [subtotals[index] for index in order]
        return totals

    def _get_tax_total_node(self, vals):
        # Node renderer also present in the customer-provided Odoo 18 code.
        node = super()._get_tax_total_node(vals)
        if vals.get('sign') != -1:
            return node
        subtotals = node.get('cac:TaxSubtotal', [])
        total = node.get('cbc:TaxAmount')
        if not isinstance(total, dict) or not isinstance(subtotals, list):
            return node
        if not all(isinstance(item.get('cbc:TaxAmount'), dict) for item in subtotals):
            return node
        order = stable_order(
            total.get('_text'),
            [item['cbc:TaxAmount'].get('_text') for item in subtotals],
        )
        node['cac:TaxSubtotal'] = [subtotals[index] for index in order]
        return node
