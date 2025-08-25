from odoo import models, fields, api

class AirWaybill(models.Model):
    _name = 'air.waybill'
    _description = 'Air Waybill'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='LTA Number', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, tracking=True)

    # Shipper
    shipper_id = fields.Many2one('res.partner', string='Shipper', required=True)
    shipper_address = fields.Text(string='Shipper Address')

    # Consignee
    consignee_id = fields.Many2one('res.partner', string='Consignee', required=True)
    consignee_address = fields.Text(string='Consignee Address')

    # Flight info
    flight_number = fields.Char(string='Flight Number')
    departure = fields.Char(string='Departure')
    destination = fields.Char(string='Destination')
    iata_code = fields.Char(string="IATA Code")

    # Cargo info
    length = fields.Float(string="Length (cm)")
    width = fields.Float(string="Width (cm)")
    height = fields.Float(string="Height (cm)")

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):
        for rec in self:
            rec.volume = rec.length * rec.width * rec.height / 1000000  # m³

    gross_weight = fields.Float(string='Gross Weight (kg)')
    chargeable_weight = fields.Float(string='Chargeable Weight (kg)')
    pieces = fields.Integer(string='Number of Pieces')
    volume = fields.Float(string="Volume (m³)", compute="_compute_volume", store=True)

    # Financial info
    purchase_amount = fields.Float(string='Purchase Amount')
    sale_amount = fields.Float(string='Sale Amount')
    currency_id = fields.Many2one('res.currency', string='Currency')

    # Additional info
    handling_info = fields.Text(string='Handling Information')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
