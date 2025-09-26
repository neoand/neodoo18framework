# -*- coding: utf-8 -*-
{
    'name': '{{MODULE_NAME}}',
    'version': '18.0.1.0.0',
    'category': '{{CATEGORY}}',
    'summary': '{{SUMMARY}}',
    'description': """
{{DESCRIPTION}}
    """,
    'author': '{{AUTHOR}}',
    'website': '{{WEBSITE}}',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/{{MODULE_TECHNICAL_NAME}}_security.xml',
        'views/{{MODULE_TECHNICAL_NAME}}_views.xml',
        'views/{{MODULE_TECHNICAL_NAME}}_menu.xml',
    ],
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': {{IS_APPLICATION}},
    'license': 'LGPL-3',
}