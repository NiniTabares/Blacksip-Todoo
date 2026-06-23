from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    blacksip_name = fields.Char("Description", compute="_compute_blacksip_name", inverse="_inverse_blacksip_name")
    
    def _inverse_blacksip_name(self):
        for line in self:
            if line.blacksip_name:
                line.name = line.blacksip_name

    @api.depends('name')
    def _compute_blacksip_name(self):
        for line in self:
            line.blacksip_name = line.name
