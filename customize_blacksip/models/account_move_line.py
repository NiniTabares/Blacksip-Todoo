from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    commercial = fields.Many2one("hr.employee", "Commercial")
    brand = fields.Char("Brand")
    csp = fields.Char("C.S.P.")
