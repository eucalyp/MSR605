 #!/usr/bin/env python

# based on tutorials:
#   http://www.roman10.net/serial-port-communication-in-python/
#   http://www.brettdangerfield.com/post/raspberrypi_tempature_monitor_project/

import serial, time
import argparse
from msr605 import MSR605

SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 9600

ser = serial.Serial(SERIALPORT, BAUDRATE)

ser.bytesize = serial.EIGHTBITS #number of bits per bytes

ser.parity = serial.PARITY_NONE #set parity check: no parity

ser.stopbits = serial.STOPBITS_ONE #number of stop bits

#ser.timeout = None          #block read

#ser.timeout = 0             #non-block read

ser.timeout = 1              #timeout block read

ser.xonxoff = False     #disable software flow control

ser.rtscts = False     #disable hardware (RTS/CTS) flow control

ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

ser.writeTimeout = 0     #timeout for write

parser = argparse.ArgumentParser(description='This program is a toolbox to help the use of the MSR605 magnetic card reader/writer. Take a look at the MSR605 documentation for more details (http://www.triades.net/downloads/MSR605%20Programmer%27s%20Manual.pdf).We are also trying to respect the ISO7811 standard. Have fun and fork us on github.')
parser.add_argument('-r', '--read', action='store_true', help='set read mode. default mode.')
parser.add_argument('-w', '--write', action='store_true', help='set write mode. ignored if read mode is set.')
parser.add_argument('-e', '--erase', action='store', type=str, choices=['1', '2', '3', '12', '13', '23', '123'], help='set erase mode. ignored if read or write mode is set. its value determine wich track to erase; default erase all tracks.')
parser.add_argument('-t1', '--track1', action='store', type=str, help='data to write on track 1. alphanureic; see iso7811.')
parser.add_argument('-t2', '--track2', action='store', type=str, help='data to write on track 2. only numeric; see iso7811.')
parser.add_argument('-t3', '--track3', action='store', type=str, help='data to write on track 3. only numeric; see iso7811.')
parser.add_argument('-bpc', '--bpc', nargs=3, action='store', type=int, choices=range(5, 9), help='set bit per character for the 3 tracks. give the values with the order: track1 track2 track3')
parser.add_argument('-bpi1', '--bpi1', action='store', type=int, choices=[75, 210], help='bit per inch for track 1. overwrite -bpi argument')
parser.add_argument('-bpi2', '--bpi2', action='store', type=int, choices=[75, 210], help='bit per inch for track 2. overwrite -bpi argument')
parser.add_argument('-bpi3', '--bpi3', action='store', type=int, choices=[75, 210], help='bit per inch for track 3. overwrite -bpi argument')
parser.add_argument('-bpi', '--bpi', nargs=3, action='store', type=int, choices=[75, 210], help='set bit per inch for the 3 tracks. give the values with the order: track1 track2 track3')
parser.add_argument('-iso', '--iso', action='store_true', help='set iso format for read and write. default mode. overwrite -raw if both set')
parser.add_argument('-raw', '--raw', action='store_true', help='set raw format for read and write.')
parser.add_argument('--reset', action='store_true', help='only reset the MSR605.')
parser.add_argument('--com_test', action='store_true', help='only test the communication with the MSR605.')
parser.add_argument('--sensor_test', action='store_true', help='only run the sensor test on the MSR605.')
parser.add_argument('--ram_test', action='store_true', help='only run the ram test on the MSR605.')
parser.add_argument('--test', action='store_true', help='run communication, ram and sensor tests on the MSR605.')
parser.add_argument('--info', action='store_true', help='display device model and firmware version of the MSR605.')
parser.add_argument('--model', action='store_true', help='display device model of the MSR605.')
parser.add_argument('--firmware', action='store_true', help='display firmware version of the MSR605.')
parser.add_argument('-hi','--hico', action='store_true', help='set high-coercivity mode of the MSR605.')
parser.add_argument('-low','--lowco', action='store_true', help='set low-coercivity mode. ignored if high-coercivity mode is set.')
parser.add_argument('--info_coer', action='store_true', help='display coercivity status of the MSR605.')
parser.add_argument('--green', action='store_true', help='turn on green led, turn off red and yellow leds.')
parser.add_argument('--yellow', action='store_true', help='turn on yellow led, turn off green and red leds. overwrite --green argument')
parser.add_argument('--red', action='store_true', help='turn on red led and turn off green and yellow leds. overwrite --green and --yellow arguments')
parser.add_argument('--leds', action='store_true', help='turn all leds on. overwrite --green, --yellow and --red arguments')
parser.add_argument('-v', '--verbose', action='store_true', help='the tool is more verbatim')
args = parser.parse_args()

if args.verbose:
    print(args)

MSR605.VERBOSE = args.verbose

msr605 = MSR605.MSR605(ser)

###utils
def test_communication():
    print('testing communication...')
    result = msr605.test_communication()
    if result:
        print('communication test succeeded')
    else:
        print('communication test failed')

def test_ram():
    print('testing ram...')
    result = msr605.test_ram()
    if result:
        print('ram test succeeded')
    else:
        print('ram test failed')

def test_sensor():
    print('testing sensor...')
    result = msr605.test_sensor()
    if result:
        print('sensor test succeeded')
    else:
        print('sensor test failed')
###

if ser.isOpen():
    print('Communication opened with MSR605')

    try:

        if args.reset:
            print('reseting MSR605')
            msr605.reset()

        if args.erase:
            erase1 = '1' in args.erase
            erase2 = '2' in args.erase
            erase3 = '3' in args.erase
            msr605.erase(erase1, erase2, erase3)

        if args.write:
            if args.iso or not args.raw:
                msr605.write_iso(args.track1.encode('ascii'), args.track2.encode('ascii'), args.track3.encode('ascii'))
            else:
                msr605.write_raw(args.track1, args.track2, args.track3)

        if args.info:
            print('getting info...')
            info = msr605.get_info()
            print('firmware version: ' + info['version'].decode('ascii'))
            print('device model: ' + info['model'].decode('ascii'))

        if args.firmware:
            print('getting firmware version...')
            version = msr605.get_firmware_version()
            print('firmware version: ' + version.decode('ascii'))

        if args.model: 
            print('getting device model...')
            model = msr605.get_device_model()
            print('device model: ' + model.decode('ascii'))

        if args.com_test:
            test_communication()

        if args.ram_test:
            test_ram()

        if args.sensor_test:
            test_sensor()

        if args.test:
            test_communication()
            test_ram()
            test_sensor()

        if args.hico:
            print('setting coercivity to high...')
            msr605.set_high_coercivity()
            print('coercivity set to high')

        elif args.lowco:
            print('setting coercivity to low...')
            msr605.set_low_coercivity()
            print('coercivity set to low')

        
        if args.info_coer:
            print('getting coercivity status...')
            status = msr605.get_coercivity_status()
            print('coercivity status: ' + status.decode('ascii'))

        if args.bpc:
            print('setting bpc values...')
            response = msr605.set_bpc(args.bpc[0], args.bpc[1], args.bpc[2])
            print('bpc values set to: track1=' + str(response[0]) + ', track2=' + str(response[1]) + ', track3=' + str(response[2]))

        if args.bpi:
            print('setting bpi for track1 to ' + str(args.bpi[0]))
            msr605.set_bpi(1, args.bpi[0])
            print('setting bpi for track2 to ' + str(args.bpi[1]))
            msr605.set_bpi(2, args.bpi[1])
            print('setting bpi for track3 to ' + str(args.bpi[2]))
            msr605.set_bpi(3, args.bpi[2])
            print('bpi values set')

        if args.bpi1:
            print('setting bpi for track1')
            msr605.set_bpi(1, args.bpi1)
            print('bpi set for track1')

        if args.bpi2:
            print('setting bpi for track2')
            msr605.set_bpi(2, args.bpi2)
            print('bpi set for track2')

        if args.bpi3:
            print('setting bpi for track3')
            msr605.set_bpi(3, args.bpi3)
            print('bpi set for track3')


        if args.green:
            msr605.turn_on_green_led()

        if args.yellow:
            msr605.turn_on_yellow_led()

        if args.red:
            msr605.turn_on_red_led()

        if args.leds:
            msr605.turn_on_leds()

        print('closing communication...')
        ser.close()

    #except Exception as e:
    #    ser.close()
    #    print('error communicating...: ' + str(e))

    except KeyboardInterrupt:
        ser.close()

    print('Communication closed with MSR605')
else:
    print('cannot open serial port')

