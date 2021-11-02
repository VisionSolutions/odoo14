# -*- coding: utf-8 -*-
{
    'name': "ORS CRM",

    'summary': """
        ORS --Crm realted changes""",

    'description': """
        Crm related changes for data import export
    """,

    'author': "Envertis Soln",
    'website': "http://www.envertis.com.au",
    'category': 'CRM',
    'version': '0.1.10',
    'depends': ['base', 'crm', 'mass_mailing', 'marketing_automation'],
    'data': [
        'security/ir.model.access.csv',
        'data/ors_crm_stage_data.xml',
        'data/ors_crm_lost_reason_data.xml',
        'data/user_demo_date.xml',
        'data/mail_data.xml',
        # 'data/mail_data_final.xml',
        'views/ors_res_users_staff.xml',
        'views/ors_crm_views.xml',
        'views/ors_opportunity_view.xml',
        'views/calendar_event_view.xml',
        'views/mail_activity_view.xml',
    ],
}
