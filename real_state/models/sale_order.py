from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property', string='Related Property')

    def action_confirm(self):
        res = super().action_confirm()
        if self.property_id:
            self.property_id.write({'state': 'sold', 'selling_price': self.amount_total})
        return res