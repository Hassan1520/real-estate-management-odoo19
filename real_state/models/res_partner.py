from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property', string='Property')
    price = fields.Float(related='property_id.diff', string='Property Difference', store=False)


