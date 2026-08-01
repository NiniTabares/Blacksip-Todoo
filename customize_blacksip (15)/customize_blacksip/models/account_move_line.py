from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    commercial = fields.Many2one("hr.employee", "Commercial")
    brand = fields.Char("Brand")
    csp = fields.Char("C.S.P.")
    blacksip_name = fields.Char("Description", compute="_compute_blacksip_name", inverse="_inverse_blacksip_name")
    
    def _inverse_blacksip_name(self):
        for line in self:
            if line.blacksip_name:
                line.name = line.blacksip_name

    @api.depends('name')
    def _compute_blacksip_name(self):
        for line in self:
            line.blacksip_name = line.name


    @api.depends('product_id', 'move_id.ref', 'move_id.payment_reference')
    def _compute_name(self):
        def get_sale_name(line):
            values = []
            if line.partner_id.lang:
                product = line.product_id.with_context(lang=line.partner_id.lang)
            else:
                product = line.product_id
            if not product:
                return False
            if not product.description_sale:
                return False
            if line.journal_id.type == 'sale':
                if product.description_sale:
                    values.append(product.description_sale)
            return '\n'.join(values) if values else False
        sale_move_lines = self.filtered(lambda l: l.journal_id.type == 'sale' and l.company_id.country_id.code == 'CO')
        other_move_lines = self - sale_move_lines
        super(AccountMoveLine, other_move_lines)._compute_name()
        if sale_move_lines:
            term_by_move = (self.move_id.line_ids | self).filtered(lambda l: l.display_type == 'payment_term').sorted(lambda l: l.date_maturity or date.max).grouped('move_id')
            for line in self.filtered(lambda l: l.move_id.inalterable_hash is False):
                if line.display_type == 'payment_term':
                    term_lines = term_by_move.get(line.move_id, self.env['account.move.line'])
                    n_terms = len(line.move_id.invoice_payment_term_id.line_ids)
                    if line.move_id.payment_reference and line.move_id.ref and line.move_id.payment_reference != line.move_id.ref:
                        name = f'{line.move_id.ref} - {line.move_id.payment_reference}'
                    elif line.move_id.payment_reference:
                        name = line.move_id.payment_reference
                    elif line.move_id.move_type in ['in_invoice', 'in_refund'] and line.move_id.ref:
                        name = line.move_id.ref
                    else:
                        name = False

                    if n_terms > 1:
                        index = term_lines._ids.index(line.id) if line in term_lines else len(term_lines)

                        name = _('%(name)s installment #%(number)s', name=name if name else '', number=index + 1).lstrip()
                    if name:
                        line.name = name
                if not line.product_id or line.display_type in ('line_section', 'line_note'):
                    continue

                if not line.name or line._origin.name == get_sale_name(line._origin) or line.product_id != line._origin.product_id:
                    line.name = get_sale_name(line)