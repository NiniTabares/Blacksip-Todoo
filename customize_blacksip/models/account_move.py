from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    commercial = fields.Many2one("hr.employee", "Commercial", compute="_compute_customize_values",
                                 inverse="_inverse_customize_values", store=True, readonly=False)
    brand = fields.Char("Brand", compute="_compute_customize_values",
                        inverse="_inverse_customize_values", store=True, readonly=False)
    csp = fields.Char("C.S.P.", compute="_compute_customize_values",
                      inverse="_inverse_customize_values", store=True, readonly=False)

    @api.depends("line_ids.commercial", "line_ids.brand", "line_ids.csp")
    def _compute_customize_values(self):
        for move in self:
            move.commercial = move.line_ids and move.line_ids[0].commercial or False
            move.brand = move.line_ids and move.line_ids[0].brand or False
            move.csp = move.line_ids and move.line_ids[0].csp or False

    def _inverse_customize_values(self):
        for move in self:
            move.line_ids.write({'commercial': move.commercial,
                                 'brand': move.brand,
                                 'csp': move.csp})