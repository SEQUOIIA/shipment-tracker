import time, requests, click, sys, os
from shipment_tracker.providers.gls import GLS
from shipment_tracker.providers.ups import UPS
from shipment_tracker.providers.dhl import DHL

class ShippingTracker:
    def __init__(self, **kwargs):
        self.shippingCompany = "" if kwargs.__contains__('provider') is False else kwargs['provider']
        self.shippingCode = "" if kwargs.__contains__('trackingCode') is False else kwargs['trackingCode']
        self.providers = {}
        self.enableNotification = False
        self.pushoverToken = ""
        self.pushoverUser = ""

        if os.environ.__contains__('SHIPMENT_TRACKER_PUSHOVER_TOKEN') and os.environ.__contains__('SHIPMENT_TRACKER_PUSHOVER_USER'):
            self.pushoverToken = os.environ['SHIPMENT_TRACKER_PUSHOVER_TOKEN']
            self.pushoverUser = os.environ['SHIPMENT_TRACKER_PUSHOVER_USER']
            self.enableNotification = True

    def monitor(self):
        providers = {
            'gls': GLS.getProgress,
            'ups': UPS.getProgress,
            'dhl': DHL.getProgress
        }

        if providers.__contains__(self.shippingCompany.lower()):
            getProgress = providers[self.shippingCompany.lower()]
        else:
            print(("Provider {p} is not supported.").format(p=self.shippingCompany))
            exit(1)

        shipmentActivityCounter = 0

        while True:
            resp = getProgress(self.shippingCode)

            click.clear()
            packageStatus = u'Status of package {}'.format(resp.packageID)
            if resp.packageStatus:
                packageStatus = u'{} ({})'.format(packageStatus, resp.packageStatus)
            print(packageStatus)
            for status in resp.status:
                #timeU = unicode(time.strftime('%Y/%m/%d %H:%M:%S'))
                #statusU = unicode(status)
                print(u'{}: {}'.format(time.strftime('%Y/%m/%d %H:%M:%S'), status))
                #print(u'{}: {}'.format(timeU, statusU).encode('utf-8'))
            
            if resp.statusSize() > shipmentActivityCounter:
                shipmentActivityCounter = resp.statusSize()
                if self.enableNotification:
                    self.send_notification(resp.status[0])         
            time.sleep(60)

    def send_notification(self, status):
        req = requests.Request('POST', 'https://api.pushover.net/1/messages.json',
        data={
            'token': self.pushoverToken,
            'user': self.pushoverUser,
            'title': 'Shipment movement detected',
            'message': status
        })
        s = requests.session()
        req = s.prepare_request(req)
        s.send(req, stream=True)