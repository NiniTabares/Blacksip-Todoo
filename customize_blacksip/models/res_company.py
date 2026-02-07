from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    payment_instructions = fields.Html(string='Payment Instructions',)
