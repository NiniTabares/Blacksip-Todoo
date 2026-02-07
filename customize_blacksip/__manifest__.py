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
    'version': '0.2',

    'depends': ['account', 'l10n_co_dian'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_line_views.xml',
        'views/account_move_views.xml',
        'views/res_company_views.xml',
        'report/report_invoice.xml',
    ],
}

