from shipment_tracker.provider.provider import Provider, ShipmentProgress
import requests, time

class DHLDE(Provider):
    @staticmethod
    def getProgress(shippingCode):
        payload = {
            'languageCode': 'de'
        }

        req = requests.Request('POST', 'https://app.dhl.de/shipments/{trackingnumber}'.format(trackingnumber=shippingCode),
        headers={
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A5010 Build/PKQ1.180716.001)',
            'Content-Type': 'application/json; charset=utf-8',
            'device-class': 'Smartphone',
            'emmi-api-version': '10',
            'platform': 'AndroidApp',
            'app-version': '2.24',
            'Interface-Key': '6cczx3k4z8o46izeprkh05xgeund8m0e'
        }, json=payload)

        s = requests.session()
        req = s.prepare_request(req)
        resp = s.send(req, stream=True)
        jsonResp = resp.json()
        print(resp.json())
        r = ShipmentProgress()   
        r.packageID = shippingCode
        r.packageStatus = jsonResp['events'][0]['eventStatus']

        for shipment in jsonResp['events']:
            status = u'{description}[{time}]: {city}, {country}'.format(
                description=shipment['eventStatus'],
                time=shipment['eventDateTime'],
                city=shipment.get('eventLocation', '?'),
                country=shipment.get('eventCountry', '?')
            )
            r.addStatus(status)
        
        return r