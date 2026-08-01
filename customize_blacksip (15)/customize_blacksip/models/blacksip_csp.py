from odoo import fields, models, api

class BlacksipCSP(models.Model):
    _name = "blacksip.csp"
    _description = "Blacksip CSP"

    name = fields.Char("CSP", required=True, help="Enter the CSP value.")