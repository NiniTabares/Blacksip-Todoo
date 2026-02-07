from odoo import models, fields


class Bank(models.Model):
    _inherit = 'res.bank'
    _description = 'Campos adicionales tipo y codigo'

    code = fields.Char('Codigo banco')

