import base64
import zipfile
import string
import sys

from homemate_bridge.cli import HomematePacket


TEST_PACKET = base64.b64decode("aGQAunBrIhyZnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALo38iee8lkDLaKG3CKoPZWoZb3OlVOLuRuClC2TYhs1bGofEH2ZxN2Jo7FtmDbLFiGoFZxPg2bxKDCxQWN9lLdmxW9F7JwXNOfz9Yq52xuL1351mPHIYcl/HSRtCtfiFOTx0TmrktL6qTnNnZXD7h8jPfg0D9yCJefpkO7x87IbhHUw9DIq1nlqjfj5Zc1+2")

printable = string.printable.encode('utf-8')


# https://stackoverflow.com/a/17197027/566216
def strings(f, target_len):
    result = b""
    for c in f.read():
        c = bytes([c])
        if c in printable:
            result += c
            continue
        if len(result) == target_len:
            yield result
        result = b""
    if len(result) == target_len:  # catch result at EOF
        yield result


with zipfile.ZipFile(sys.argv[1]) as myzip:
    with myzip.open('classes.dex', 'r') as myfile:
        possible_keys = strings(myfile, 16)
        for key in possible_keys:
            try:
                packet = HomematePacket(TEST_PACKET, {0x70: key})
            except:
                pass
            else:
                print(key)
