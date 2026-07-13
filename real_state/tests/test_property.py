from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref': 'PRT10001',
            'name': 'property1',
            'description': 'property1 des 1',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'bedrooms': 10,
            'expected_price': 1000,
        })

    def test_01_property_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(property_id, [{
            'ref': 'PRT10001',
            'name': 'property1',
            'description': 'property1 des 1',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'bedrooms': 10,
            'expected_price': 1000,
        }])

    def test_02_state_transition(self):
        self.property_01_record.action_pending()
        self.assertEqual(self.property_01_record.state, 'pending')

        self.property_01_record.action_sold()
        self.assertEqual(self.property_01_record.state, 'sold')

    def test_03_negative_price_validation(self):
        with self.assertRaises(ValidationError):
            self.env['property'].create({
                'name': 'Invalid Property',
                'expected_price': -50,
            })
