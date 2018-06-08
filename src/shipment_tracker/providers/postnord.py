from shipment_tracker.provider.provider import Provider, ShipmentProgress
import requests, time, sys

class PostNord(Provider):
    @staticmethod
    def getProgress(shippingCode):
        req = requests.Request('GET', 'https://www.postnord.dk/api/shipment/{trackingnumber}/en'.format(trackingnumber=shippingCode),
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

        s = requests.session()
        req = s.prepare_request(req)
        resp = s.send(req, stream=True)
        jsonResp = resp.json()
        r = ShipmentProgress()   
        r.packageID = shippingCode
        try:
            r.packageStatus = jsonResp['response']['trackingInformationResponse']['shipments'][0]['items'][0]['statusText']['header']
        except TypeError:
            print(jsonResp)
            sys.exit(1)

        for shipment in jsonResp['response']['trackingInformationResponse']['shipments'][0]['items'][0]['events']:
            status = u'{description}[{time}]: {city}, {country}'.format(
                description=shipment['eventDescription'],
                time=shipment['eventTime'],
                city=shipment['location'].get('city', '?'),
                country=shipment['location'].get('countryCode', '?')
            )
            r.addStatus(status)
        
        return r