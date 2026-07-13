from odoo import fields, models


class Owner(models.Model):
    _name = 'owner'
    _description = 'Owner'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    property_ids = fields.One2many('property', 'owner_id', string='Properties')