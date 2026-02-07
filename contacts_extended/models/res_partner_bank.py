from odoo import models, fields


class Bank(models.Model):
    _inherit = 'res.partner.bank'
    _description = 'Campos adicionales tipo'

    account_type = fields.Selection(selection=[('1','Ahorros'),('2','Corriente')], string="Tipo cuenta")
