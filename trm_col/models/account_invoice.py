from odoo import fields, models, api
# from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'TRM (USD) Factura'

    trm = fields.Float(string='TRM', compute = 'compute_trm')
    trm_date = fields.Date(string='Fecha TRM')

    @api.onchange('invoice_date')
    def compute_date_trm(self):
        for record in self:
            if record.invoice_date:
                record.trm_date = record.invoice_date

    @api.onchange('invoice_date', 'currency_id','trm_date')
    def compute_trm(self):
        for record in self:
            rates = self.env["res.currency.rate"].search([("name", "=", record.trm_date), ("currency_id", "=", record.currency_id.id)])
            if rates:
                record.trm = rates.inverse_company_rate
            else:
                record.trm = 0











