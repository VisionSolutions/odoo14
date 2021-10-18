# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class KnowCompany(models.Model):
    _name = 'know.company'

    name = fields.Char('Name')


class ResUser(models.Model):
    _inherit = 'res.users'

    color = fields.Integer('color', help="Colour in Number")


class ResUserStaff(models.Model):
    _name = "res.users.staff"

    name = fields.Char('Name')
    is_installed_by = fields.Boolean('Is Installer')
    is_trade_assistant = fields.Boolean('Is Trade Assistant')


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    def action_apply(self):
        result = super(Lead2OpportunityPartner, self).action_apply()
        lead = self.lead_id
        lead.write({
            'site_street': lead.street,
            'site_street2': lead.street2,
            'site_zip': lead.zip,
            'site_city': lead.city,
            'site_state_id': lead.state_id and lead.state_id.id,
            'site_country_id': lead.country_id and lead.country_id.id,
        })
        return result


class OrsCrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'AU')], limit=1)
        return country

    @api.model
    def _get_default_ids(self):
        rec = self.env['crm.tag'].search([('name', '=', 'newsletter')], limit=1).ids
        return rec

    country_id = fields.Many2one(
        'res.country', string='Country',
        compute='_compute_partner_address_values', readonly=False, store=True, default=_get_default_country)

    tag_ids = fields.Many2many(
        'crm.tag', 'crm_tag_rel', 'lead_id', 'tag_id', string='Tags',
        help="Classify and analyze your lead/opportunity categories like: Training, Service",default=_get_default_ids)
    # Lead fields
    # lead_stage_id = fields.Many2one(
    #     'crm.stage', string='Lead Stage', index=True, tracking=True,
    #     copy=False, )
    lead_stage = fields.Selection([
        ('new', 'New'),
        ('attempting', 'Attempting to contact'),
        ('contacted', 'Contacted'),
        ('no_response', 'No Response/Uncontactable'),
        ('not_engaged', 'Not Engaged'),
        ('disqualified', 'Disqualified'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted./ Qualified')], string='Lead Stage', default='new')  # Lead status
    # Lead Owner    Salesperson
    # Name      Lead
    first_name = fields.Char(
        'First Name', tracking=30)  # First Name
    middle_name = fields.Char(
        'Middle Name', tracking=30)  # Middle Name
    last_name = fields.Char(
        'Last Name', tracking=30)  # Last Name
    # Website   Website
    # Title     Title
    # Company   Company Name
    # Email     Email
    industry = fields.Selection([
        ('agriculture', 'Agriculture'),
        ('apparel', 'Apparel'),
        ('banking', 'Banking'),
        ('biotechnology', 'Biotechnology'),
        ('chemicals', 'Chemicals'),
        ('communications', 'Communications'),
        ('construction', 'Construction'),
        ('consulting', 'Consulting'),
        ('education', 'Education'),
        ('electronics', 'Electronics'),
        ('energy', 'Energy'),
        ('engineering', 'Engineering'),
        ('entertainment', 'Entertainment'),
        ('environmental', 'Environmental'),
        ('finance', 'Finance'),
        ('food_beverage', 'Food & Beverage'),
        ('government', 'Government'),
        ('healthcare', 'Healthcare'),
        ('hospitality', 'Hospitality'),
        ('insurance', 'Insurance'),
        ('machinery', 'Machinery'),
        ('manufacturing', 'Manufacturing'),
        ('media', 'Media'),
        ('not_profit', 'Not for Profit'),
        ('other', 'Other'),
        ('retail', 'Retail'),
        ('shipping', 'Shipping'),
        ('technology', 'Technology'),
        ('transportation', 'Transportation'),
        ('utilities', 'Utilities'),
        ('landscape', 'Landscape'),
        ('architect', 'Architect')], string='Industry')  # Industry
    # Phone     Phone
    no_of_employee = fields.Integer('No of Employee', default=0)  # No of Employee
    # Mobile    Mobile
    # Lead Source   Source
    # Rating    Priority
    know_about_company_id = fields.Many2one('know.company', string='How did You Know About Our Company?')  # How did You Know About Our Company

    request_type = fields.Selection([
        ('gen_req', 'General Request'),
        ('pur_prod', 'I want to purchase the product')], string='Request Type')  # Request Type
    product = fields.Selection([
        ('eclipse', 'Eclipse'),
        ('alfresco', 'Alfresco')], string='Product')  # Product
    approximate_area = fields.Char(
        'Approximate Size of Area')  # Approximate Size of Area
    is_newspaper_subscribe = fields.Boolean('Subscribe To Newspaper')  # Subscribe To Newspaper
    # Account   Expected Revenue
    build_time = fields.Selection([
        ('1_3', '1-3 months'),
        ('3_6', '3-6 months'),
        ('6_12', '6-12 months')], string='Timeline to build')  # Timeline to build
    construction_type = fields.Selection([
        ('new', 'New Build'),
        ('alteration', 'Alteration'),
        # ('non_structural', 'Non structural'),
        # ('non_structural_awning', 'Non structural Awning'),
        # ('steel_frame', 'Steel frame'),
        ('addition', 'Addition'),
        # ('ssc', 'Single Storey Construction'),
        # ('tf', 'Timber Frame'),
        # ('alum_awning', 'Alum & steel frame awning'),
        # ('aluminium_steel', 'Aluminium & steel frame'),
        # ('aluminium_frame', 'Aluminium Frame'),
        # ('sandwich_panel', 'Sandwich Panel'),
        # ('wooden_frame', 'Wooden Frame'),
        # ('sf', 'Steel Frames'),
        # ('timber_deck', 'Timber Frame on timber deck'),
        # ('combi_timber_steel', 'Combination Timber & Steel Frame'),
        # ('concrete_frame', 'Concrete Frame'),
        # ('non_carport_steel_posts', 'Non structural carport steel posts'),
        # ('not_awning', 'Not structural awning'),
        # ('steel_awning', 'Steel frame awning'),
        # ('non_remesh_screen', 'Non structural remesh screen enclosure'),
        # ('timer_hardie', 'Timber/Hardie Column Frame'),
        # ('steel_cfc', 'Steel frame & CFC Columns'),
        # ('steel_non', 'Steel frame - Non structural'),
        # ('non_steel', 'Non structural - Steel frame'),
        # ('non_awning', 'Non structural Awning - Steel frame'),
        # ('non_patio', 'Non structural Patio Cover'),
        # ('non_patio_awning_screeeninng', 'Non structural Patio cover awning & screening'),
        # ('non_exlips', 'Non structural Eclipse rotating louvre patio cover'),
        # ('aluminium', 'Aluminium'),
        # ('structural', 'Structural'),('other', 'Other')
    ], string='Type of Construction')  # Type of Construction

    tracking_medium = fields.Char('Tracking Medium')  # Tracking Medium
    tracking_campaign = fields.Char('Tracking Campaign')  # Tracking Campaign
    tracking_source = fields.Char('Tracking Source')  # Tracking Source
    tracking_content = fields.Char('Tracking Content')  # Tracking Content
    tracking_url = fields.Char('Tracking URL')  # Tracking URL
    tracking_term = fields.Char('Tracking Term')  # Tracking Term
    budget = fields.Char('Budget Old')  # Budget
    budget_new = fields.Selection([
        ('$10000 - 15000', '$10000 - 15000'),
        ('$15000 - 30000', '$15000 - 30000'),
        ('Over $30000', 'Over $30000'),
    ], 'Budget')  # Budget

    # Opportunity fields
    # Opportunity Name      Opportunity
    # Opportunity Owner     Customer
    # Account Name          Salesperson
    # Stage     State
    business_type = fields.Selection([
        ('existing', 'Existing Business'),
        ('new', 'New Business')], string='Type')  # Type
    # Probability
    primary_campaign_source = fields.Char('Primary Campaign Source')  # Primary Campaign Source
    # loss_reason = fields.Selection([
    #     ('lost_com', 'Lost to competitor'),
    #     ('no_budget', 'No Budget/Lost Funding'),
    #     ('no_decision', 'No Decision/Non Responsive'),
    #     ('price', 'Price'),
    #     ('prod_not_suit', 'Product not suitable'),
    #     ('site_not_suit', 'Site not suitable'),
    #     ('lost_tender', 'Lost Tender')], string='Loss Reason') # Loss Reason
    enquiry_number = fields.Char('Enquiry Number')  # Enquiry Number
    # Start Date        Days to Assign
    design_consultants = fields.Many2one('res.users', string='Design Consultants', index=True, tracking=True,)  # Design Consultant
    # Close Date    Days to Close
    amount = fields.Monetary('Amount', currency_field='company_currency', tracking=True)  # Amount
    contract_amount = fields.Monetary('Contract Amount', currency_field='company_currency', tracking=True)  # Contract Amount

    site_map = fields.Text('Site Map')  # Site Map
    next_step = fields.Char('Next Step')  # Next Step
    date_variation = fields.Datetime('Variation Date', copy=False)  # Variation Date
    estimated_purchase_month_date = fields.Datetime(string='Estimated Purchase Date')
    estimated_purchase_month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')], string='Estimated Purchase Month')  # Estimated Purchase Month
    variation_amount = fields.Monetary('Variation Amount', currency_field='company_currency', tracking=True)  # Variation Amount
    finance_required = fields.Boolean('Finance Required')  # Finance Required
    calculated_amount = fields.Monetary('Calculated Amount', currency_field='company_currency', tracking=True)  # Calculated Amount

    site_as_above = fields.Boolean('Site as above')  # Site as above
    number_stories = fields.Selection([
        ('single_lev_unit', 'Single Level Unit'),
        ('single_lev_walk', 'Single Level Unit on raised walkway'),
        ('multi_lev', 'Multi Level Unit'),
        ('2', '2'),
        ('non_structural', 'Non structural'),
        ('double_lev', 'Double Level Unit')], string='Number stories')  # Number Storeys
    site_unit = fields.Char('Site Unit')  # Site Unit
    square_meters = fields.Char('Square Meters')  # Square Meters
    site_lot = fields.Char('Site Lot')  # Site Lot
    site_street = fields.Char('Site Street No')  # Site Street No
    site_street2 = fields.Char('Site Street')  # Site Street
    site_zip = fields.Char('Site PostCode')  # Site PostCode
    site_city = fields.Char('Site Suburb')  # Site Suburb

    site_state_id = fields.Many2one(
        "res.country.state", string='Site State',
        domain="[('country_id', '=?', country_id)]")  # Site State
    site_country_id = fields.Many2one(
        'res.country', string='Site Country')
    site_contact_name = fields.Char('Site Contact Name')  # Site Contact Name
    site_phone = fields.Char('Site Contact Phone')  # Site Contact Phone
    site_email_from = fields.Char('Site Contact Email')  # Site Contact Email

    hbcf_required = fields.Boolean('HBCF Required')  # HBCF Required
    hbcf_policy_no = fields.Char('HBCF Policy Number')  # HBCF Policy Number
    hbcf_status = fields.Char('HBCF Status')  # HBCF Status
    hbcf_not = fields.Char('HBCF Not')  # HBCF Not
    hbcf_status_date = fields.Datetime('HBCF Status Date', copy=False)  # HBCF Status Date

    job_status = fields.Char('Job Status')  # Job Status
    job_start_date = fields.Datetime('Job Start Date', copy=False)  # Job Start Date
    jno = fields.Char('Job Number')  # JNO
    job_end_date = fields.Datetime('Job End Date', copy=False)  # Job End Date
    job_status_note = fields.Text('Job Status Notes')  # Job Status Notes
    job_days = fields.Datetime('Job Days Old', copy=False)  # Job Days
    job_days_new = fields.Char('Job Days', copy=False)  # Job Days
    # installed_by = fields.Many2one('res.users', string='Installed By', index=True, tracking=True)  # Installed By
    # trade_assistant = fields.Many2one('res.users', string='Trade Assistant', index=True, tracking=True)   # Trade Assistant
    installed_by = fields.Many2one('res.users.staff', string='Installed By', index=True, tracking=True, domain="[('is_installed_by', '=', True)]")  # Installed By
    trade_assistant = fields.Many2one('res.users.staff', string='Trade Assistant', index=True, tracking=True, domain="[('is_trade_assistant', '=', True)]")   # Trade Assistant
    deposit_payment = fields.Monetary('Deposit Payment', currency_field='company_currency', tracking=True)  # Deposit Payment
    check_measure = fields.Monetary('Check Measure', currency_field='company_currency', tracking=True)  # Check Measure
    start_payment = fields.Monetary('Start Payment', currency_field='company_currency', tracking=True)  # Start Payment
    progress_payment2 = fields.Monetary('Progress Payment 2', currency_field='company_currency', tracking=True)  # Progress Payment 2
    progress_payment3 = fields.Monetary('Progress Payment 3', currency_field='company_currency', tracking=True)  # Progress Payment 3
    completion_payment = fields.Monetary('Completion Payment', currency_field='company_currency', tracking=True)  # Completion Payment
    total_payments = fields.Monetary('Total Payments', currency_field='company_currency', tracking=True, compute='_compute_total_payment')  # Total Payments
    account_id = fields.Char('AccountId', help="To be mapped in future")
    contact_id = fields.Char('ContactId', help="To be mapped in future")
    sales_rep_id = fields.Char('Sales_Rep__c', help="To be mapped in future")
    date_closed = fields.Datetime('Closed Date', readonly=False, copy=False)
    date_closed_new = fields.Date('Closed Date New', readonly=False, copy=False)

    # expected_revenue = fields.Monetary('Expected Revenue', currency_field='company_currency', tracking=True)
    expected_revenue = fields.Float('Expected Revenue', tracking=True)

    # Field for data import
    converted_date = fields.Datetime('Converted Date', copy=False)  # ConvertedDate
    salesforce_create_date = fields.Datetime("Salesforce Create Date")
    owner_id = fields.Char('Owner Id')
    sale_rep_id = fields.Char('Sales Rep')
    AccountId = fields.Char('Account Id')

    @api.depends('deposit_payment', 'check_measure', 'start_payment', 'progress_payment2', 'progress_payment3', 'completion_payment')
    def _compute_total_payment(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            lead.total_payments = lead.deposit_payment + lead.check_measure + lead.start_payment + lead.progress_payment2 + lead.progress_payment3 + lead.completion_payment

    @api.onchange('hbcf_required')
    def onchange_hbfc(self):
        if self.hbcf_required:
            self.contract_amount = 395
        else:
            self.contract_amount = 0

    def default_get(self, fields):
        defaults = super(OrsCrmLead, self).default_get(fields)
        if 'user_id' in defaults:
            user = self.env.ref('ors_crm.user_sharon')
            defaults['user_id'] = user.id
        return defaults

    @api.depends('last_name', 'city', 'jno')
    def _compute_name(self):
        for lead in self:
            name = ''
            if lead.last_name:
                name += lead.last_name
            if lead.jno:
                name += '-' + lead.jno
            if lead.city:
                name += '-' + lead.city
            lead.name = name

    @api.depends('partner_id', 'first_name', 'last_name')
    def _compute_contact_name(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not self.partner_id:
                if self.first_name or self.last_name:
                    lead.contact_name = "%s %s" % (lead.first_name or '', lead.last_name or '')
            else:
                lead.update(lead._prepare_contact_name_from_partner(lead.partner_id))

    # Detractive automatic probability calculation
    @api.depends(lambda self: ['tag_ids', 'stage_id', 'team_id'] + self._pls_get_safe_fields())
    def _compute_probabilities(self):
        lead_probabilities = self._pls_get_naive_bayes_probabilities()
        for lead in self:
            if lead.id in lead_probabilities:
                # was_automated = lead.active and lead.is_automated_probability
                was_automated = False
                lead.automated_probability = lead_probabilities[lead.id]
                if was_automated:
                    lead.probability = lead.automated_probability

    def get_map_url(self):
        self.ensure_one()
        # self.partner_id.geo_localize()
        map_address = ''
        if self.site_street and self.site_street2 and self.site_city:
            map_address = self.site_street + ' ' + self.site_street2 + ' ' + self.site_city
        elif self.site_street and self.site_street2:
            map_address = self.site_street + ' ' + self.site_street2
        elif self.site_street and self.site_city:
            map_address = self.site_street + ' ' + self.site_city
        elif self.site_street2 and self.site_city:
            map_address = self.site_street2 + ' ' + self.site_city
        elif self.site_street:
            map_address = self.site_street
        elif self.site_street2:
            map_address = self.site_street2
        elif self.site_city:
            map_address = self.site_city
        _logger.info("The Site map address is '%s'", map_address)

        if map_address:
            url = 'https://www.google.com/maps/search/?api=1&query={}'.format(map_address)
            # url = 'https://www.google.com/maps/search/?api=1&query={},{}'.format(self.partner_id.partner_latitude, self.partner_id.partner_longitude)
            # url = 'https://www.google.com/maps/dir/?api=1&destination={},{}'.format(self.partner_id.partner_latitude, self.partner_id.partner_longitude)
            return url
        else:
            raise UserError(_('Site address is not set properly, please set it correctly so you can view the map.'))

    def get_leads_map_url(self):
        self.ensure_one()
        map_address = ''
        if self.street and self.street2 and self.city:
            map_address = self.street + ' ' + self.street2 + ' ' + self.city
        elif self.street and self.street2:
            map_address = self.street + ' ' + self.street2
        elif self.street and self.city:
            map_address = self.street + ' ' + self.city
        elif self.street2 and self.city:
            map_address = self.street2 + ' ' + self.city
        elif self.street:
            map_address = self.street
        elif self.street2:
            map_address = self.street2
        elif self.city:
            map_address = self.city
        _logger.info("The Site map address is '%s'", map_address)

        if map_address:
            url = 'https://www.google.com/maps/search/?api=1&query={}'.format(map_address)
            return url
        else:
            raise UserError(_('Leads address is not set properly, please set it correctly so you can view the map.'))

    def leads_map_redirection(self):
        """Open leads address map based on partner's latitude and longitude."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': self.get_leads_map_url(),
        }


    def map_redirection(self):
        """Open map based on partner's latitude and longitude."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': self.get_map_url(),
        }

    # For open List view of calendar and own meeting from lead/opportunity
    # def action_schedule_meeting(self):
    #     self.ensure_one()
    #     action = self.env["ir.actions.actions"]._for_xml_id("crm.act_crm_opportunity_calendar_event_new")
    #     partner_ids = self.env.user.partner_id.ids
    #     if self.partner_id:
    #         partner_ids.append(self.partner_id.id)
    #     action['context'] = {
    #         'default_opportunity_id': self.id if self.type == 'opportunity' else False,
    #         'default_partner_id': self.partner_id.id,
    #         'default_partner_ids': partner_ids,
    #         'default_team_id': self.team_id.id,
    #         'default_name': self.name,
    #     }
    #     return action
