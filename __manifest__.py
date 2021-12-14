{
    'name': "sbm",
    'author':
        'ENZAPPS',
    'summary': """
This module is for My School Managment.
""",

    'description': """
        This module is for My School Managment.
    """,
    'website': "",
    'category': 'base',
    'version': '14.0',
    'depends': ['base','account','uom_unece','base_unece','account_tax_unece','base_vat_sanitized','onchange_helper','base_iban','base_bank_from_iban','base_business_document_import','account_invoice_import','base_ubl_payment','account_payment_partner','account_invoice_import_ubl','account_invoice_ubl','sale','purchase','stock',],
    "images": ['static/description/icon.png'],
    'data': [
        "views/account_move.xml",
        # 'security/contact_form.xml',
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
        # 'data/sequence.xml',
        # 'wizards/create_address.xml',
        # 'views/image.xml',
        # 'views/product.xml',
        # 'views/minister.xml',
        # 'views/lead_type.xml',
         'reports/report.xml',
        'reports/report_view.xml',



        # 'views/newxml.xml',


    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
