from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    brand_id = fields.Many2one("product.brand", "Brand", help="Select a brand for this sale order if any.")
    brand_number = fields.Char("Brand Number", help="Optional field to store a brand-specific number or code.", tracking=True, copy=False)
    # CONTACTO RESPONSABLE CLIENTE
    customer_contact_id = fields.Many2one("res.partner", "Customer Contact", help="Select the main contact for this customer.")
    # DURACIÓN ESTIMADA
    estimated_duration = fields.Date("Estimated Duration", help="Estimated duration for the sale order.", tracking=True)
    # CONTACTO RESPONSABLE EN BLACKSIP
    responsible_contact_id = fields.Many2one("res.partner", "Responsible Contact", help="Select the responsible contact for this sale order.",
                                             default=lambda self: self.env.user.partner_id, tracking=True)
    csp_id = fields.Many2one("blacksip.csp", "CSP", help="Select the CSP for this sale order.", tracking=True)


    @api.onchange('partner_id')
    def _onchange_custom_partner_id(self):
        for order in self:
            if order.partner_id:
                # Filter contacts that are not the main partner
                contacts = order.partner_id.child_ids.filtered(lambda c: c.type in ['contact', 'other'])
                order.customer_contact_id = contacts and contacts[0] or False
            else:
                order.customer_contact_id = order.partner_id

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.brand_id and order.brand_id.sequence_id and not order.brand_number:
                order.brand_number = order.brand_id.sequence_id.next_by_id()
        return res
    
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['brand'] = self.brand_id.name
        invoice_vals['csp'] = self.csp_id.name
        return invoice_vals
    
    @api.model_create_multi
    def create(self, vals_list):
        oders = super().create(vals_list)
        for order in oders:
            if order.brand_id and order.brand_id.sequence_id and not order.brand_number:
                order.brand_number = order.brand_id.sequence_id.next_by_id()
        return oders
    
    def write(self, vals):
        res = super().write(vals)
        for order in self:
            if order.brand_id and order.brand_id.sequence_id and not order.brand_number:
                order.brand_number = order.brand_id.sequence_id.next_by_id()
        return res
    
    def action_draft(self):
        res = super().action_draft()
        self.write({'brand_number': False})
        return res