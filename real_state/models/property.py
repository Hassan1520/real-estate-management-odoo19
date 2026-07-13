from datetime import timedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    ref = fields.Char(string='Reference', readonly=True, default='New', tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True, translate=True)
    description = fields.Text(string='Description', tracking=True, translate=True)
    postcode = fields.Char(string='Postcode', tracking=True)
    date_availability = fields.Date(string='Availability Date')
    expected_selling_date = fields.Date(string='Expected Selling Date')
    is_late = fields.Boolean(string='Late', default=False, tracking=True)
    expected_price = fields.Float(string='Expected Price', digits=(16, 3))
    selling_price = fields.Float(string='Selling Price', digits=(16, 3))
    diff = fields.Float(string='Difference', compute='_compute_diff', store=True)
    bedrooms = fields.Integer(string='Bedrooms', tracking=True)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], string='State', default='draft', tracking=True)

    owner_id = fields.Many2one('owner', string='Owner', tracking=True)
    owner_address = fields.Char(related='owner_id.address', string='Owner Address', store=False)
    owner_phone = fields.Char(related='owner_id.phone', string='Owner Phone', store=False)
    tag_ids = fields.Many2many('tag', string='Tags')
    line_ids = fields.One2many('property.line', 'property_id', string='Property Lines')
    active = fields.Boolean(string='Active', default=True, tracking=True)
    create_time = fields.Datetime(string='Created On', default=fields.Datetime.now)
    next_time = fields.Datetime(string='Next Reminder', compute='_compute_next_time', store=False)

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            rec.next_time = rec.create_time + timedelta(hours=6) if rec.create_time else False

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.constrains('expected_price', 'selling_price')
    def _check_prices(self):
        for rec in self:
            if rec.expected_price < 0 or rec.selling_price < 0:
                raise ValidationError(_('Expected price and selling price must be positive.'))

    @api.onchange('expected_price')
    def _onchange_diff(self):
        self.diff = self.expected_price - self.selling_price

    def _change_state(self, new_state):
        allowed_transitions = {
            ('draft', 'pending'): True,
            ('pending', 'draft'): True,
            ('pending', 'sold'): True,
            ('sold', 'draft'): True,
            ('sold', 'closed'): True,
        }
        if (self.state, new_state) not in allowed_transitions:
            raise ValidationError(_(f'Invalid state transition from {self.state} to {new_state}.'))
        self.create_history_record(self.state, new_state)
        self.state = new_state

    def action_draft(self):
        for rec in self:
            rec._change_state('draft')

    def action_pending(self):
        for rec in self:
            rec._change_state('pending')

    def action_sold(self):
        for rec in self:
            rec._change_state('sold')

    def action_closed(self):
        for rec in self:
            rec._change_state('closed')

    def create_history_record(self, old_state, new_state, reason=False):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or '',
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids],
            })

    def check_expected_selling_date(self):
        domain = [
            ('expected_selling_date', '!=', False),
            ('expected_selling_date', '<', fields.Date.today()),
            ('is_late', '=', False),
        ]
        records = self.search(domain, limit=50)
        records.write({'is_late': True})

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == "New":
            res.ref = self.env["ir.sequence"].next_by_code('property_seq')
        return res

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_state.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_state.owner_action')
        view_id = self.env.ref('real_state.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    def property_xlsx_report(self):
        active_ids = self.env.context.get('active_ids') or self.ids
        return {
            'type': 'ir.actions.act_url',
            'url': f'/property/excal/report/{active_ids}',
            'target': 'new',
        }


class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Line'

    property_id = fields.Many2one('property', string='Property')
    area = fields.Float(string='Area')
    description = fields.Char(string='Description')
