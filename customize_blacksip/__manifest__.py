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
    'version': '0.1',

    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_line_views.xml',
        'views/account_move_views.xml',
    ],
}

