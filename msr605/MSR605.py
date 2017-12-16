from .commands import *
from .debugs import *
from .debugs import verbose_mode as VERBOSE
import binascii

class MSR605:
    def __init__(self, fd):
        self.fd = fd

    def reset(self):
        if VERBOSE:
            print(DEBUG_RESET_BEFORE)
        
        self.write_serial(MSR_RESET)
        
        if VERBOSE:
            print(DEBUG_RESET_AFTER)

    def erase(self, track1=False, track2=False, track3=False):
        code = int(track3)*4 + int(track2)*2 + int(track1)

        command = MSR_ERASE_TRACKS + bytes([code])

        self.write_serial(command)
        response = self.read_serial(True)

        return response == MSR_ERASE_SUCCESS

    '''
    track1: bytes
    track2: bytes
    track3: bytes
    '''
    def write_iso(self, track1=None, track2=None, track3=None):
        data1 = data2 = data3 = b''

        if track1 != None:
            data1 = MSR_BEGIN_BYTE + b'\x01' + track1
        if track2 != None:
            data2 = MSR_BEGIN_BYTE + b'\x02' + track2
        if track3 != None:
            data3 = MSR_BEGIN_BYTE + b'\x03' + track3

        card_data = data1 + data2 + data3
        data_block = MSR_DATA_BEGIN_CODE + card_data + MSR_ENDING_FIELD
        command = MSR_WRITE_ISO + data_block
        self.write_serial(command)
        response = self.read_serial(True)

        if response == MSR_WRITE_ISO_SUCCESS:
            return True

        print('error while writing iso: ' + response.decode('ascii'))

    ###getters
    def get_firmware_version(self):
        self.write_serial(MSR_FIRMWARE_VERSION)
        return self.read_serial()

    def get_device_model(self):
        self.write_serial(MSR_DEVICE_MODEL)
        return self.read_serial()

    def get_info(self):
        if VERBOSE:
            print(DEBUG_GET_INFO_BEFORE)

        version = self.get_firmware_version()
        model = self.get_device_model()

        return {'version' : version, 'model' : model}

    def get_coercivity_status(self):
        self.write_serial(MSR_COERCIVITY_STATUS)
        status = self.read_serial()

        if status == MSR_COERCIVITY_STATUS_HIGH:
            return b'Hi-Co'

        if status == MSR_COERCIVITY_STATUS_LOW:
            return b'Low-Co'

        raise ValueError('Unknown coercivity status')
    ###

    ###setters
    def set_coercivity(self, command):
        self.write_serial(command)
        response = self.read()

        if response == MSR_SET_COERCIVITY_SUCCESS:
            return True

        raise ValueError('Unknown error while setting coercivity status')

    def set_high_coercivity(self):
        return self.set_coercivity(MSR_SET_HIGH_COERCIVITY)

    def set_low_coercivity(self):
        return self.set_coercivity(MSR_SET_LOW_COERCIVITY)

    '''
    track: int
    value: int
    '''
    def set_bpi(self, track, value):
        if track != 1 and track != 2 and track != 3:
            raise ValueError('Incorrect track number. Possible values are 1, 2 or 3')
        if value != MSR_BPI_75 and value != MSR_BPI_210:
            raise ValueError('Incorrect value for bpi. Possible values are 75 or 210')

        command = MSR_SET_BPI + MSR_BPI_HEX_CODE[track][value]
        self.write_serial(command)
        response = self.read_serial()

        if response == MSR_SET_BPI_SUCCESS:
            return True

        if response == MSR_SET_BPI_FAIL:
            return False

        raise ValueError('Unknown error while setting bpi')

    """
    track1: int
    track2: int
    track3: int
    return: [new value track1, new value track2, new value track3]
    """
    def set_bpc(self, track1, track2, track3):
        if track1 < MSR_BPC_MIN_VALUE or track1 > MSR_BPC_MAX_VALUE:
            raise ValueError('Wrong value for track1. Possible values are 5, 6, 7, 8')
        if track2 < MSR_BPC_MIN_VALUE or track2 > MSR_BPC_MAX_VALUE:
            raise ValueError('Wrong value for track2. Possible values are 5, 6, 7, 8')
        if track3 < MSR_BPC_MIN_VALUE or track3 > MSR_BPC_MAX_VALUE:
            raise ValueError('Wrong value for track3. Possible values are 5, 6, 7, 8')

        command = MSR_SET_BPC + bytes([track1]) + bytes([track2]) + bytes([track3])
        self.write_serial(command)

        response = self.read_serial()

        status = bytes([response[0]])
        if status == MSR_SET_BPC_SUCCESS:
            return [response[1], response[2], response[3]]

        raise ValueError('Unknown error while setting BPC values') 
    ###

    ###Leds actions
    def turn_on_leds(self):
        self.write_serial(MSR_ALL_LED_ON)

    def turn_on_green_led(self):
        self.write_serial(MSR_GREEN_LED_ON)

    def turn_on_yellow_led(self):
        self.write_serial(MSR_YELLOW_LED_ON)

    def turn_on_red_led(self):
        self.write_serial(MSR_RED_LED_ON)

    ###Tests
    def test_communication(self):
        self.write_serial(MSR_COMMUNICATION_TEST)
        response = self.read_serial()

        return response == MSR_COMMUNICATION_TEST_EXPECTED_RESPONSE

    def test_ram(self):
        self.write_serial(MSR_RAM_TEST)
        response = self.read_serial()

        return response == MSR_RAM_TEST_SUCCESS

    def test_sensor(self):
        self.write_serial(MSR_SENSOR_TEST)
        response = self.read_serial(True)

        return response == MSR_SENSOR_TEST_SUCCESS
    ###

    ###Serial
    def write_serial(self, data):
        if VERBOSE:
                print(data)
        self.fd.write(data)

    def read_serial(self, wait_for_swipping=False):
        timeout = self.fd.timeout
        if wait_for_swipping:
            self.fd.timeout = None
            print('Waiting for swipping...')

        #read the begins character. the same for every communication.
        byte = self.fd.read(1)
        if byte != MSR_BEGIN_BYTE:
            raise ValueError('The first communication character wasn\'t the one expected')

        data = b''
        while True:

            byte = self.fd.read(1)
            
            if wait_for_swipping:
                self.fd.timeout = timeout
                wait_for_swipping = False
            
            if byte.decode() == '':
                break
            
            if VERBOSE:
                print(byte)
            
            data = data + byte

        return data