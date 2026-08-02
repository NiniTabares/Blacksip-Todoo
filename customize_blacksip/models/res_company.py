from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    payment_instructions = fields.Html(string='Payment Instructions',)
    blacksip_sale_template = fields.Boolean(string='Blacksip Template', help="Enable the Blacksip template in the sales documents.")
