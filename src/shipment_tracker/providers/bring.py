from shipment_tracker.provider.provider import Provider, ShipmentProgress
import requests, time

class Bring(Provider):
    @staticmethod
    def getProgress(shippingCode):
        req = requests.Request('GET', 'https://tracking.bring.dk/tracking/api/fetch/{trackingnumber}?lang=da'.format(trackingnumber=shippingCode),
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

        s = requests.session()
        req = s.prepare_request(req)
        resp = s.send(req, stream=True)
        jsonResp = resp.json()
        r = ShipmentProgress()   
        r.packageID = shippingCode
        r.packageStatus = jsonResp['consignmentSet'][0]['packageSet'][0]['statusDescription']

        for shipment in jsonResp['consignmentSet'][0]['packageSet'][0]['eventSet']:
            status = u'{description}[{time}]: {city}, {country}'.format(
                description=shipment['description'],
                time=shipment['dateIso'],
                city=shipment.get('city', '?'),
                country=shipment.get('countryCode', '?')
            )
            r.addStatus(status)
        
        return r