from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    airwaybill_ids = fields.One2many(
        "sale.airwaybill", 
        "order_id", 
        string="Air Waybills",
        copy=False
    )


class SaleAirwaybill(models.Model):
    _name = "sale.airwaybill"
    _description = "Air Waybill"

    order_id = fields.Many2one("sale.order", string="Sale Order", required=True)

    # Champs Air Waybill
    airwaybill_number = fields.Char(string="Air Waybill No.", required=True)
    shipper = fields.Char(string="Shipper")
    consignee = fields.Char(string="Consignee")
    airline = fields.Char(string="Airline")
    departure = fields.Char(string="Departure Airport")
    arrival = fields.Char(string="Arrival Airport")
    flight_no = fields.Char(string="Flight Number")
    flight_date = fields.Date(string="Flight Date")

    gross_weight = fields.Float(string="Gross Weight (kg)")
    chargeable_weight = fields.Float(string="Chargeable Weight (kg)")
    freight_amount = fields.Float(string="Freight Amount")

    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)

    cargo_status = fields.Selection([
        ("pending", "Pending"),
        ("in_transit", "In Transit"),
        ("arrived", "Arrived"),
        ("delivered", "Delivered"),
    ], string="Cargo Status", default="pending")
