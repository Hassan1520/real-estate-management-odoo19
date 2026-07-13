from odoo import fields, models


class ChangeState(models.TransientModel):
    _name = 'change.state'
    _description = 'Change Property State'

    property_id = fields.Many2one('property', string='Property', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], string='New State', required=True)
    reason = fields.Char(string='Reason')

    def action_confirm(self):
        if self.property_id and self.property_id.state == 'closed':
            self.property_id.create_history_record('closed', self.state, self.reason)
            self.property_id.write({'state': self.state})
            return {'type': 'ir.actions.act_window_close'}
        return {'type': 'ir.actions.act_window_close'}