from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    brand_id = fields.Many2one(
        "product.brand",
        string="Brand",
        help="Select a brand for this sale order if any.",
    )
    brand_number = fields.Char(
        string="Brand Number",
        help="Optional field to store a brand-specific number or code.",
        tracking=True,
        copy=False,
    )

    # Contacto responsable del cliente.
    customer_contact_id = fields.Many2one(
        "res.partner",
        string="Customer Contact",
        help="Select the main contact for this customer.",
    )

    # Fechas independientes de la fecha estándar de la cotización (date_order).
    service_start_date = fields.Date(
        string="Fecha de inicio del servicio",
        tracking=True,
        copy=True,
        help="Fecha programada para iniciar la ejecución del servicio.",
    )
    service_order_date = fields.Date(
        string="Fecha de elaboración de la orden de servicio",
        default=fields.Date.context_today,
        tracking=True,
        copy=True,
        help="Fecha en la que se elabora la orden de servicio.",
    )

    # Se conserva por compatibilidad con el módulo actual.
    estimated_duration = fields.Date(
        string="Estimated Duration",
        help="Estimated duration for the sale order.",
        tracking=True,
    )

    # Contacto responsable en Blacksip.
    responsible_contact_id = fields.Many2one(
        "res.partner",
        string="Responsible Contact",
        help="Select the responsible contact for this sale order.",
        default=lambda self: self.env.user.partner_id,
        tracking=True,
    )
    csp_id = fields.Many2one(
        "blacksip.csp",
        string="CSP",
        help="Select the CSP for this sale order.",
        tracking=True,
    )

    @api.onchange("partner_id")
    def _onchange_custom_partner_id(self):
        for order in self:
            if order.partner_id:
                contacts = order.partner_id.child_ids.filtered(
                    lambda contact: contact.type in ("contact", "other")
                )
                order.customer_contact_id = contacts[:1]
            else:
                order.customer_contact_id = False

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            if order.brand_id.sequence_id and not order.brand_number:
                order.brand_number = order.brand_id.sequence_id.next_by_id()
        return result

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            "brand": self.brand_id.name or False,
            "csp": self.csp_id.name or False,
        })
        return invoice_vals

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            if order.brand_id.sequence_id and not order.brand_number:
                brand_number = order.brand_id.sequence_id.next_by_id()
                order.brand_number = brand_number
                order.name = brand_number
        return orders

    def write(self, vals):
        result = super().write(vals)
        for order in self:
            if order.brand_id.sequence_id and not order.brand_number:
                brand_number = order.brand_id.sequence_id.next_by_id()
                order.brand_number = brand_number
                order.name = brand_number
        return result
