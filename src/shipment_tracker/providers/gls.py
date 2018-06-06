from shipment_tracker.provider.provider import Provider, ShipmentProgress
import requests, time

class GLS(Provider):
    @staticmethod
    def getProgress(shippingCode):
        req = requests.Request('GET', 'https://gls-group.eu/app/service/open/rest/DK/da/rstt001?match={trackingnumber}'.format(trackingnumber=shippingCode),
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

        s = requests.session()
        req = s.prepare_request(req)
        resp = s.send(req, stream=True)
        jsonResp = resp.json()
        r = ShipmentProgress()   
        r.packageID = shippingCode     

        if jsonResp.__contains__('tuStatus') != True:
            time.sleep(10)
            return GLS.getProgress(shippingCode)


        for shipment in jsonResp['tuStatus'][0]['history']:
            status = u'{description}[{date} - {time}]: {city}, {country}'.format(
                description=shipment['evtDscr'],
                date=shipment['date'],
                time=shipment['time'],
                city=shipment['address'].get('city', '?'),
                country=shipment['address'].get('countryCode', '?')
            )
            r.addStatus(status)
        
        return r