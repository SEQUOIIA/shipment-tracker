from shipment_tracker.core import ShippingTracker
from sys import argv

def main():
    creator = "SEQUOIIA"
    print(("Shipment-tracker - @{creator}").format(creator=creator))

    st = ShippingTracker(provider=argv[1], trackingCode=argv[2])
    st.monitor()

main()