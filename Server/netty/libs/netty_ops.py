from pyats.topology import loader
from genie import testbed
from rest_framework import status
import sys
import os

# Fetching the operational state of the network device

class NettyOps:

    def __init__(self, device_name, command, username, password):
        self.device_name = device_name
        self.command = command
        self.username = username
        self.password = password

    def parser(self):
        try:
            inventory = testbed.load('netty/inventory.yaml')
        except Exception as e:
            return {"error": "Unable to load inventory", "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
        inventory.testbed.credentials.default.username = self.username
        inventory.testbed.credentials.default.password = self.password
        print("Credentials: ",  inventory.testbed.credentials.default)
        try:
            device = inventory.devices[self.device_name]
        except Exception as e:
            return {"error": str(e) + " does not exist in the testbed", "status_code": status.HTTP_404_NOT_FOUND}

        dd = ""
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")
        try:
            inventory.connect(device, mit=True, connection_timeout=10)
            dd = inventory.parse('show version')
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout

        return {"result": dd, "status_code": status.HTTP_200_OK}