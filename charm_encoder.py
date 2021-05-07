from py_encoder import py_encoder


def encode_charms(charm_file):
    with open(charm_json) as cjsf:  
        charm_data = cjsf.read()
    x = py_encoder.encodeFromPython(charm_data)

if __name__ == '__main__':
    charm_file = "charms.json"
    encode_charms(charm_file)