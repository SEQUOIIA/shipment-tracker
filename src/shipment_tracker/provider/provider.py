from sys import exit

class Provider:
    def __init__(self):
        self.name = ""

    @staticmethod
    def getProgress(shippingCode):
        print("getProgress not implemented for provider yet.")
        exit(1)

class ShipmentProgress:
    def __init__(self):
        self.status = []
        self.packageID = ""
        self.packageStatus = ""
    def addStatus(self, status):
        self.status.append(status)
    def statusSize(self):
        return len(self.status)