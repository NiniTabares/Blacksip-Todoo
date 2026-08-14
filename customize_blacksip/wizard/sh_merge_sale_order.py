from odoo import models
from odoo.exceptions import ValidationError

class ShMsoMergeSaleOrderWizard(models.TransientModel):
    _inherit = "sh.mso.merge.sale.order.wizard"

    def action_merge_sale_order(self):
        if self.sale_order_ids and len(self.sale_order_ids.mapped('brand_id'))>1:
            raise ValidationError("No se puede crear una Orden de Servicio con Diferente Marca")
        res = super().action_merge_sale_order()
        if self.sale_order_ids and res and res.get('domain'):
            ids = res.get('domain')[0][2]
            order_ids = self.env['sale.order'].browse(ids)
            order_id = self.sale_order_ids and self.sale_order_ids[0] or False
            if order_id:
                vals = {
                    'brand_id' : order_id.brand_id.id,
                    'customer_contact_id' : order_id.customer_contact_id.id,
                    'estimated_duration' : order_id.estimated_duration,
                    'responsible_contact_id' : order_id.responsible_contact_id.id,
                    'csp_id' : order_id.csp_id.id,
                    'campaign_id': order_id.campaign_id.id,
                    'date_order': order_id.date_order
                }
                order_ids.write(vals)
        return res