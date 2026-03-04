from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        if self.description_sale:
            name = self.description_sale
        else:
            name = False
        return name