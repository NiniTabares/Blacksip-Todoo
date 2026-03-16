from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        if self.env.company.country_id.code != 'CO':
             return super().get_product_multiline_description_sale()
        else:
            if self.description_sale:
                name = self.description_sale
            else:
                name = False
            return name