from shipment_tracker.provider.provider import Provider, ShipmentProgress
import requests

class UPS(Provider):
    @staticmethod
    def getProgress(shippingCode):
        payload = {
            'Track30Request': {
                'UpsLocale': 'en_GB',
                'InquiryNumber': [shippingCode],
                'TrackingOption': '02',
                'Request': {
                    'RequestOption': ['1'],
                    'SubVersion': '1507'
                }
            },
            'UPSSecurity': {
                'ServiceAccessToken': {
                    'AccessLicenseNumber': '7D099AD569BB5765'
                }
            }
        }

        req = requests.Request('POST', 
        'https://onlinetools.ups.com/json/TrackPrivileged',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }, json=payload)

        s = requests.session()
        req = s.prepare_request(req)
        resp = s.send(req, stream=True)
        jsonResp = resp.json()
        r = ShipmentProgress()
        for shipment in jsonResp['TrackResponse']['Shipment']['Package']['Activity']:
            status = '{description}[{date} - {time}]: {city}, {country}'.format(
                description=shipment['Status']['Description'],
                date=shipment['Date'],
                time=shipment['Time'],
                city=shipment['ActivityLocation']['Address'].get('City', '?'),
                country=shipment['ActivityLocation']['Address'].get('CountryCode', '?')
            )
            r.addStatus(status)

        r.packageID = jsonResp['TrackResponse']['Shipment']['Package']['TrackingNumber']
        r.packageStatus = jsonResp['TrackResponse']['Shipment']['Package']['CurrentStatus']['Description']
        
        return r