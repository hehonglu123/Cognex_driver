from cognex_robotraconteur_driver import _native_client

bmp_bytes = _native_client.native_read_image('192.168.1.175', '')

with open('image.bmp', 'wb') as f:
    f.write(bmp_bytes)
