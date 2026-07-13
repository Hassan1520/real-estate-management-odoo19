from odoo import fields, models


class Building(models.Model):
    _name = 'building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    no = fields.Integer(string='Number')
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
