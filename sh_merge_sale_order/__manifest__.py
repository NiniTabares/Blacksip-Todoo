# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Merge Sale Orders",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": """
Merge Sale Orders,
merge quotation,
merge sale order,
combine quotation,
combine sale order,
merge so app,
combine quotations module,
append sales order odoo
""",
    "description": """
This module useful to Merge Sale Orders.
Sometime required to make single quote from multi quotation.
This module help user to merge quotation as well many more options.
easy and quick solition to make
new quotation or replace existing quotation.
""",
    "version": "0.0.1",
    "depends": [
        "sale_management",
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/sh_merge_sale_order_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price":21,
    "currency": "EUR"
}
