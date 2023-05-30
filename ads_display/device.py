import pyopencl as cl

def main():
    # Get the OpenCL platforms and devices
    platforms = cl.get_platforms()
    devices = platforms[0].get_devices()

    # Print some information about the available devices
    for device in devices:
        print("Device name:", device.name)
        print("Device type:", cl.device_type.to_string(device.type))
        print("Device vendor:", device.vendor)
        print("Device version:", device.version)
        print("Device max clock speed:", device.max_clock_frequency, "MHz")
        print()

if __name__ == '__main__':
    main()
