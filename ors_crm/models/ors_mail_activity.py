# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    who_id = fields.Char('WhoId')
    what_id = fields.Char('WhatId')
    owner_id = fields.Char('OwnerId')
    account_id = fields.Char('AccountId')
