from odoo import api, fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    sequence_id = fields.Many2one("ir.sequence", "Sequence", help="Select a sequence for this brand if any.")