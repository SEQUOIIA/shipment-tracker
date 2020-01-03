from shipment_tracker.provider.provider import Provider, ShipmentProgress
import requests

class DHL(Provider):
    @staticmethod
    def getProgress(shippingCode):
        req = requests.Request('GET', 
        'https://www.dhl.com/shipmentTracking?AWB={trackingNumber}&countryCode=g0&languageCode=en&_=1515593653850'.format(trackingNumber=shippingCode),
        headers={
            'User-Agent': 'User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

        s = requests.session()
        req = s.prepare_request(req)
        resp = s.send(req, stream=True)
        json = resp.json()
        r = ShipmentProgress()
        for shipment in json['results'][0]['checkpoints']:
            status = u'{description}[{time} {date}]: {location}'.format(
                description=shipment['description'],
                time=shipment['time'],
                date=shipment['date'],
                location=shipment['location']
            )
            r.addStatus(status)
        
        return r