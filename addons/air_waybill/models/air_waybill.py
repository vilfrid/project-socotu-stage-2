# -*- coding: utf-8 -*-
import requests
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AirWaybill(models.Model):
    _name = 'air.waybill'
    _description = 'Air Waybill'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --- Main fields ---
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
    length = fields.Float(string='Length')
    width = fields.Float(string='Width')
    height = fields.Float(string='Height')
    volume = fields.Float(string='Volume', compute='_compute_volume', store=True, readonly=True)
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

    # Financial lines
    financial_line_ids = fields.One2many('air.waybill.line', 'air_waybill_id', string='Financial Lines')
    hide_column_2 = fields.Boolean(string='Hide Column 2', default=False)

    # Tracking fields
    tracking_info_html = fields.Html(string="Tracking Info", readonly=True, copy=False)

    # Map field
    geoapify_map_html = fields.Html(string="Flight Map", sanitize=False)

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):
        for rec in self:
            rec.volume = rec.length * rec.width * rec.height

    def action_track_awb(self):
        """Calls the AWB tracking API and displays enriched tracking info and map."""
        self.ensure_one()
        awb_number = self.name or "157-03082623"
        api_key = "7561ff0c04mshbd5f260236dd25dp141995jsnd7d70f2e7cef"
        url = f"https://air-cargo-co2-track-and-trace.p.rapidapi.com/track?awb={awb_number}"

        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "air-cargo-co2-track-and-trace.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            if not data or not isinstance(data, list):
                raise UserError("Invalid API response format")
            record = data[0]

            # --- Extract general info ---
            tracking_number = record.get("awb", "")
            from_full = f"{record.get('origin', '')}"
            to_full = f"{record.get('destination', '')}"
            status = record.get("status", "Unknown")
            weight = f"{record.get('weight', '')} kg"
            volume = record.get("volume", "")
            pieces = record.get("pieces", "")
            distance = record.get("distance", "")
            duration = record.get("time", "")
            carbon = record.get("carbonEmission", "")

            general_info = f"""
            <h3>📦 Shipment Overview</h3>
            <p><b>Tracking (AWB):</b> {tracking_number}</p>
            <p><b>From (Origin):</b> {from_full}</p>
            <p><b>To (Destination):</b> {to_full}</p>
            <p><b>Status:</b> {status}</p>
            <p><b>Weight:</b> {weight}</p>
            <p><b>Volume:</b> {volume}</p>
            <p><b>Pieces:</b> {pieces}</p>
            <p><b>Total Distance:</b> {distance} km</p>
            <p><b>Total Flight Time:</b> {duration}</p>
            <p><b>Total CO₂ Emission:</b> {carbon}</p>
            <hr/>
            """

            # --- Flight Legs ---
            events = record.get("events", [])
            seen_legs = set()
            flight_legs = []

            html = general_info + "<h4>✈️ Flight Legs (Journey Path)</h4>"

            for ev in events:
                flight = ev.get("flight", {})
                if flight:
                    leg_id = (flight.get("number", ""), flight.get("origin", ""), flight.get("destination", ""))
                    if leg_id in seen_legs:
                        continue
                    seen_legs.add(leg_id)
                    flight_legs.append(flight)
                    html += f"""
                    <p><b>Flight Number:</b> {flight.get('number','')}</p>
                    <p>Route: {flight.get('origin','')} → {flight.get('destination','')}</p>
                    <p>Departure: {flight.get('actualDeparture','')}</p>
                    <p>Arrival: {flight.get('actualArrival','')}</p>
                    <p>Duration: {flight.get('duration','')}</p>
                    <p>Distance: {flight.get('distance','')} km</p>
                    <p>CO₂ Emission: {flight.get('carbonEmission','')}</p>
                    <hr/>
                    """

            # --- Key Events Timeline ---
            html += "<h4>📍 Key Events Timeline</h4><ul>"
            seen_events = set()
            for ev in events:
                ev_key = (ev.get("eventDate",""), ev.get("code",""), ev.get("eventLocation",""))
                if ev_key in seen_events:
                    continue
                seen_events.add(ev_key)
                html += f"<li>{ev.get('eventDate','')}: {ev.get('code','')} at {ev.get('eventLocation','')}</li>"
            html += "</ul>"

            # Update tracking field
            self.tracking_info_html = html

            # --- Compute map HTML ---
            self._compute_geoapify_map_html(flight_legs)

        except Exception as e:
            _logger.exception("Exception while calling AWB API")
            raise UserError(f"Exception while calling AWB API: {e}")

    def _compute_geoapify_map_html(self, flight_legs=None):
        """Generate Geoapify static map HTML showing all flight legs and events."""
        key = "5fb8882aff8f46c391af91c98ae8c8e3"  # Replace with your Geoapify API key
        for rec in self:
            coords = []

            # Collect coordinates from flight legs
            if flight_legs:
                for flight in flight_legs:
                    for coord_str in [flight.get("originCoord"), flight.get("destinationCoord")]:
                        if coord_str:
                            lon, lat = map(float, coord_str.split(","))
                            if (lon, lat) not in coords:
                                coords.append((lon, lat))

            # Collect coordinates from tracking events if needed
            if len(coords) < 2 and rec.tracking_info_html:
                import re
                matches = re.findall(r'eventLocationCoord":\s*"([0-9\.\-]+,[0-9\.\-]+)"', str(rec.tracking_info_html))
                for coord_str in matches:
                    lon, lat = map(float, coord_str.split(","))
                    if (lon, lat) not in coords:
                        coords.append((lon, lat))

            if len(coords) < 2:
                rec.geoapify_map_html = "<p>No map available</p>"
                continue

            # Markers
            marker_str = "%7C".join(
                f"lonlat:{lon},{lat};type:awesome;color:%23ff0000;size:x-large;icon:plane"
                for lon, lat in coords
            )

            # Polyline
            polyline_str = ",".join(f"{lon},{lat}" for lon, lat in coords)

            map_url = (
                f"https://maps.geoapify.com/v1/staticmap?"
                f"style=osm-bright-smooth&width=600&height=400&fit=true"
                f"&marker={marker_str}"
                f"&geometry=polyline:{polyline_str};linewidth:4;linecolor:%230000ff"
                f"&apiKey={key}"
            )
            rec.geoapify_map_html = f'<img src="{map_url}" alt="Flight Map" style="width:100%; max-width:600px; margin-top:10px;"/>'

class AirWaybillLine(models.Model):
    _name = 'air.waybill.line'
    _description = 'Air Waybill Financial Line'

    air_waybill_id = fields.Many2one('air.waybill', string='Air Waybill', required=True)
    column_1 = fields.Char('Prix/Unit')
    column_2 = fields.Char('Company')
    column_3 = fields.Char('Agent')
    column_4 = fields.Char('Socotu')
    column_5 = fields.Char('Client')
