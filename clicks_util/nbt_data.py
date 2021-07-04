import base64
import io

from nbt import nbt


def decode_inventory_data(raw, write_file=False):
    data = nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))
    if write_file:
        data.write_file("test.dat")
    else:
        return data




