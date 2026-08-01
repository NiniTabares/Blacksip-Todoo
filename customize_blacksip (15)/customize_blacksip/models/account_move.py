from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    commercial = fields.Many2one("hr.employee", "Commercial", compute="_compute_customize_values",
                                 inverse="_inverse_customize_values", store=True, readonly=False)
    brand = fields.Char("Brand", compute="_compute_customize_values",
                        inverse="_inverse_customize_values", store=True, readonly=False)
    csp = fields.Char("C.S.P.", compute="_compute_customize_values",
                      inverse="_inverse_customize_values", store=True, readonly=False)
    cost_center = fields.Many2one("account.analytic.plan", "Centro de Costo")
    trm = fields.Float("T.R.M.", compute="_compute_trm", digits=(12, 2), store=True)

    @api.depends("currency_id", "invoice_date", "date")
    def _compute_trm(self):
        for move in self:
            move.trm = move.currency_id._convert(1, move.company_currency_id, move.company_id, move.invoice_date or move.date)

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

    def _get_name_invoice_report(self):
        res = super(AccountMove, self)._get_name_invoice_report()
        if self.company_id.vat in ['805030145-8', '8050301458'] and self.move_type in ['out_invoice']:
            res = 'customize_blacksip.report_invoices_intello'
        return res