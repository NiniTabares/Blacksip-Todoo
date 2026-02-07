import logging
from odoo import fields, models, api
import time


from zeep.wsse.username import UsernameToken
from zeep import Client, Settings
from zeep.transports import Transport

_logger = logging.getLogger(__name__)

class currency_rate(models.Model):
    _inherit = "res.currency.rate"

    @api.model
    def get_col_trm(self):

        WSDL_URL = 'https://www.superfinanciera.gov.co/SuperfinancieraWebServiceTRM/TCRMServicesWebService/TCRMServicesWebService?WSDL'
        date = time.strftime('%Y-%m-%d')
        settings = Settings(raw_response=True)
        transport = Transport(operation_timeout=15, timeout=15)
        try:
            client = Client(wsdl=WSDL_URL, settings=settings,
                            transport=transport)
            trm = client.service.queryTCRM(date)
        except Exception as e:
            return _logger.critical("Error while working with BancoRep API: " + str(e))
        usd = self.env.ref('base.USD')
        last_rates = self.env["res.currency.rate"].search([("name", "=", date), ("currency_id", "=", usd.id)])

        if last_rates.name == False :
            vals = {
            "inverse_company_rate": float(trm.value),
            "rate": 1/float(trm.value),
            "name": date,
            "currency_id": 2
            }
            self.create(vals)
            _logger.info(
                "New exchange rate created to date: " +
                date +
                ", with value: " +
                str(float(trm.value))
            )
        else:
            _logger.critical("Already exist TRM for the date "+date)
















