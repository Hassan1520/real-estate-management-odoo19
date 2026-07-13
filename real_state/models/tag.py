from odoo import fields, models


class Tag(models.Model):
    _name = 'tag'
    _description = 'Property Tag'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
