#!/usr/bin/python
#-*- coding: utf-8 -*-create_device.py

### configuration ######################################
DEVICE_NAME_KAROTZ = "test_karotz"
ADDRESS = "192.168.1.244"
VOICE = "claire"
TO = 'karotz'


from domogik.tests.common.testdevice import TestDevice
from domogik.common.utils import get_sanitized_hostname

plugin = 'nabaztag'

def create_device():
    ### create the device, and if ok, get its id in device_id
    client_id  = "plugin-{0}.{1}".format(plugin, get_sanitized_hostname())
    print "Creating the Karotz  device..."
    td = TestDevice()
    params = td.get_params(client_id, "karoz")
        # fill in the params
    params["device_type"] = "karoz"
    params["name"] = DEVICE_NAME_KAROTZ
    params["address"] = ADDRESS
    params["voice"] = VOICE
    for idx, val in enumerate(params['global']):
        if params['global'][idx]['key'] == 'name' :  params['global'][idx]['value'] = NAME
        if params['global'][idx]['key'] == 'address' :  params['global'][idx]['value'] = ADDRESS
        if params['global'][idx]['key'] == 'voice' :  params['global'][idx]['value'] = VOICE
    for idx, val in enumerate(params['xpl']):
        params['xpl'][idx]['value'] = TO

    # go and create
    td.create_device(params)
    print "Device Karotz {0} configured".format(DEVICE_NAME_KAROTZ)
    
if __name__ == "__main__":
    create_device()



