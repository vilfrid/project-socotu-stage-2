from odoo import models
import requests
import logging

_logger = logging.getLogger(__name__)

class AirWaybill(models.Model):
    _inherit = 'air.waybill'

    def action_run_test(self):
        awb_number = "157-03082623"  # replace with any AWB number
        url = f"https://air-cargo-co2-track-and-trace.p.rapidapi.com/track?awb={awb_number}"

        headers = {
            "x-rapidapi-key": "7561ff0c04mshbd5f260236dd25dp141995jsnd7d70f2e7cef",
            "x-rapidapi-host": "air-cargo-co2-track-and-trace.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                data = response.json()
                _logger.info("✅ API Result: %s", data)
                print("✅ API Result:", data)  # prints to terminal
            else:
                _logger.warning("❌ API Error %s: %s", response.status_code, response.text)
                print(f"❌ API Error {response.status_code}: {response.text}")
        except Exception as e:
            _logger.error("Exception in action_run_test: %s", e)
            print("❌ Exception:", e)
