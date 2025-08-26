from odoo import models, fields, api

class AirWaybill(models.Model):
    _name = 'air.waybill'
    _description = 'Air Waybill'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Main fields
    name = fields.Char(string='AWB Number', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, tracking=True)
    shipper_id = fields.Many2one('res.partner', string='Shipper', required=True)
    shipper_address = fields.Text(string='Shipper Address')
    consignee_id = fields.Many2one('res.partner', string='Consignee', required=True)
    consignee_address = fields.Text(string='Consignee Address')
    flight_number = fields.Char(string='Flight Number')
    departure = fields.Char(string='Departure')
    destination = fields.Char(string='Destination')
    iata_code = fields.Char(string='IATA Code')
    gross_weight = fields.Float(string='Gross Weight (kg)')
    chargeable_weight = fields.Float(string='Chargeable Weight (kg)')
    pieces = fields.Integer(string='Number of Pieces')
    handling_info = fields.Text(string='Handling Information')
    purchase_amount = fields.Float(string='Purchase Amount')
    sale_amount = fields.Float(string='Sale Amount')
    currency_id = fields.Many2one('res.currency', string='Currency')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    # Volume calculation
    length = fields.Float(string="Length (cm)")
    width = fields.Float(string="Width (cm)")
    height = fields.Float(string="Height (cm)")
    volume = fields.Float(string="Volume (m³)", compute="_compute_volume", store=True)

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):
        for rec in self:
            rec.volume = rec.length * rec.width * rec.height / 60000  # m³

    # One2many financial lines
    financial_line_ids = fields.One2many('air.waybill.line', 'air_waybill_id', string='Financial Lines')

    # Toggle column 2 visibility
    hide_column_2 = fields.Boolean(string="Hide Column 2", default=False)

    def action_toggle_column_2(self):
        for rec in self:
            rec.write({'hide_column_2': not rec.hide_column_2})
        return {'type': 'ir.actions.client', 'tag': 'reload'}



class AirWaybillLine(models.Model):
    _name = 'air.waybill.line'
    _description = 'Air Waybill Financial Line'

    air_waybill_id = fields.Many2one('air.waybill', string='Air Waybill')
    column_1 = fields.Char('Prix/Unit')
    column_2 = fields.Char('Company')
    column_3 = fields.Char('Agent')
    column_4 = fields.Char('Socotu')
    column_5 = fields.Char('Client')
