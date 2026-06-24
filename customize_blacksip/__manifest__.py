# -*- coding: utf-8 -*-
{
    'name': "Customize Blacksip",

    'summary': "Add new fields to account.move",

    'description': """
Add new fields to account.move
    """,

    'author': "Grupo YACCK",
    'website': "https://www.grupoyacck.com",

    'category': 'Uncategorized',
    'version': '0.3',

    'depends': ['account', 'sale', 'l10n_co_dian', 'product_brand'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_line_views.xml',
        'views/account_move_views.xml',
        'views/res_company_views.xml',
        'views/res_config_settings_views.xml',\
        'views/sale_order_views.xml',
        'views/product_brand_view.xml',
        'report/report_invoice.xml',
        'report/ir_actions_report_templates.xml',
    ],
}

