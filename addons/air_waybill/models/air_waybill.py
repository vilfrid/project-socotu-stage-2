from odoo import models, fields, api

class AirWaybill(models.Model):
    _name = 'air.waybill'
    _description = 'Air Waybill'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='LTA Number', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, tracking=True)
    
    # Shipper Information
    shipper_id = fields.Many2one('res.partner', string='Shipper', required=True)
    shipper_address = fields.Text(string='Shipper Address')
    
    # Consignee Information
    consignee_id = fields.Many2one('res.partner', string='Consignee', required=True)
    consignee_address = fields.Text(string='Consignee Address')
    
    # Flight Information
    flight_number = fields.Char(string='Flight Number')
    departure = fields.Char(string='Departure')
    destination = fields.Char(string='Destination')
    
    # Cargo Information
    gross_weight = fields.Float(string='Gross Weight (kg)')
    chargeable_weight = fields.Float(string='Chargeable Weight (kg)')
    pieces = fields.Integer(string='Number of Pieces')
    
    # Financial Information
    purchase_amount = fields.Float(string='Purchase Amount')
    sale_amount = fields.Float(string='Sale Amount')
    currency_id = fields.Many2one('res.currency', string='Currency')
    
    # Additional Information
    handling_info = fields.Text(string='Handling Information')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)