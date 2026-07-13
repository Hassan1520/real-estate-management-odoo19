from odoo import fields, models


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'

    user_id = fields.Many2one('res.users', string='User')
    property_id = fields.Many2one('property', string='Property')
    old_state = fields.Char(string='Old State')
    new_state = fields.Char(string='New State')
    reason = fields.Char(string='Reason')
    line_ids = fields.One2many('property.history.line', 'history_id', string='Lines')


class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'
    _description = 'Property History Line'

    history_id = fields.Many2one('property.history', string='History')
    area = fields.Float(string='Area')
    description = fields.Char(string='Description')
