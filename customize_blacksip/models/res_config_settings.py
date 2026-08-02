# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    blacksip_sale_template = fields.Boolean(related="company_id.blacksip_sale_template", readonly=False, 
                                            string='Blacksip Template', 
                                            help="Enable the Blacksip template in the sales documents.")
