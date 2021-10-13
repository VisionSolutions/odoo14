# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EC(models.Model):
    _inherit = 'calendar.event'

    # user_id = fields.Many2one(default=False)
    color = fields.Integer(string='color', related='user_id.color')
    partner_ids = fields.Many2many(default=False)
    duration = fields.Float('Duration', compute='_compute_duration', store=True, readonly=False, default=1)

    who_id = fields.Char('WhoId')
    what_id = fields.Char('WhatId')
    owner_id = fields.Char('OwnerId')
