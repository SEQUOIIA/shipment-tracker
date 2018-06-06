from shipment_tracker.provider.provider import Provider
import requests

class DHL(Provider):
    @staticmethod
    def getProgressX(shippingCode):
        req = requests.Request('GET', 
        'http://www.dhl.com/shipmentTracking?AWB={trackingNumber}&countryCode=g0&languageCode=en&_=1515593653850'.format(trackingNumber=shippingCode),
        headers={
            'User-Agent': 'User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

        s = requests.session()
        req = s.prepare_request(req)
        resp = s.send(req, stream=True)
        json = resp.json()
        print(json)