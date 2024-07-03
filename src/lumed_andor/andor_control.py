import ctypes
import logging
from pathlib import Path
from typing import Tuple

import numpy as np

logger = logging.getLogger(__name__)

READ_MODES = {
    0: "Full Vertical Binning",
    1: "Multi-Track",
    2: "Random-Track",
    3: "Single-Track",
    4: "Image",
}

ACQUISITION_MODES = {
    1: "Single Scan",
    2: "Accumulate",
    3: "Kinetics",
    4: "Fast Kinetics",
    5: "Run till abort",
}

ANDOR_CODES = {
    20001: "DRV_ERROR_CODES",
    20002: "DRV_SUCCESS",
    20003: "DRV_VXDNOTINSTALLED",
    20004: "DRV_ERROR_SCAN",
    20005: "DRV_ERROR_CHECK_SUM",
    20006: "DRV_ERROR_FILELOAD",
    20007: "DRV_UNKNOWN_FUNCTION",
    20008: "DRV_ERROR_VXD_INIT",
    20009: "DRV_ERROR_ADDRESS",
    20010: "DRV_ERROR_PAGELOCK",
    20011: "DRV_ERROR_PAGEUNLOCK",
    20012: "DRV_ERROR_BOARDTEST",
    20013: "DRV_ERROR_ACK",
    20014: "DRV_ERROR_UP_FIFO",
    20015: "DRV_ERROR_PATTERN",
    20017: "DRV_ACQUISITION_ERRORS",
    20018: "DRV_ACQ_BUFFER",
    20019: "DRV_ACQ_DOWNFIFO_FULL",
    20020: "DRV_PROC_UNKONWN_INSTRUCTION",
    20021: "DRV_ILLEGAL_OP_CODE",
    20022: "DRV_KINETIC_TIME_NOT_MET",
    20023: "DRV_ACCUM_TIME_NOT_MET",
    20024: "DRV_NO_NEW_DATA",
    20025: "DRV_PCI_DMA_FAIL",
    20026: "DRV_SPOOLERROR",
    20027: "DRV_SPOOLSETUPERROR",
    20028: "DRV_FILESIZELIMITERROR",
    20029: "DRV_ERROR_FILESAVE",
    20033: "DRV_TEMPERATURE_CODES",
    20034: "DRV_TEMPERATURE_OFF",
    20035: "DRV_TEMPERATURE_NOT_STABILIZED",
    20036: "DRV_TEMPERATURE_STABILIZED",
    20037: "DRV_TEMPERATURE_NOT_REACHED",
    20038: "DRV_TEMPERATURE_OUT_RANGE",
    20039: "DRV_TEMPERATURE_NOT_SUPPORTED",
    20040: "DRV_TEMPERATURE_DRIFT",
    20049: "DRV_GENERAL_ERRORS",
    20050: "DRV_INVALID_AUX",
    20051: "DRV_COF_NOTLOADED",
    20052: "DRV_FPGAPROG",
    20053: "DRV_FLEXERROR",
    20054: "DRV_GPIBERROR",
    20055: "DRV_EEPROMVERSIONERROR",
    20064: "DRV_DATATYPE",
    20065: "DRV_DRIVER_ERRORS",
    20066: "DRV_P1INVALID",
    20067: "DRV_P2INVALID",
    20068: "DRV_P3INVALID",
    20069: "DRV_P4INVALID",
    20070: "DRV_INIERROR",
    20071: "DRV_COFERROR",
    20072: "DRV_ACQUIRING",
    20073: "DRV_IDLE",
    20074: "DRV_TEMPCYCLE",
    20075: "DRV_NOT_INITIALIZED",
    20076: "DRV_P5INVALID",
    20077: "DRV_P6INVALID",
    20078: "DRV_INVALID_MODE",
    20079: "DRV_INVALID_FILTER",
    20080: "DRV_I2CERRORS",
    20081: "DRV_I2CDEVNOTFOUND",
    20082: "DRV_I2CTIMEOUT",
    20083: "DRV_P7INVALID",
    20084: "DRV_P8INVALID",
    20085: "DRV_P9INVALID",
    20086: "DRV_P10INVALID",
    20087: "DRV_P11INVALID",
    20089: "DRV_USBERROR",
    20090: "DRV_IOCERROR",
    20091: "DRV_VRMVERSIONERROR",
    20092: "DRV_GATESTEPERROR",
    20093: "DRV_USB_INTERRUPT_ENDPOINT_ERROR",
    20094: "DRV_RANDOM_TRACK_ERROR",
    20095: "DRV_INVALID_TRIGGER_MODE",
    20096: "DRV_LOAD_FIRMWARE_ERROR",
    20097: "DRV_DIVIDE_BY_ZERO_ERROR",
    20098: "DRV_INVALID_RINGEXPOSURES",
    20099: "DRV_BINNING_ERROR",
    20100: "DRV_INVALID_AMPLIFIER",
    20101: "DRV_INVALID_COUNTCONVERT_MODE",
    20990: "DRV_ERROR_NOCAMERA",
    20991: "DRV_NOT_SUPPORTED",
    20992: "DRV_NOT_AVAILABLE",
    20115: "DRV_ERROR_MAP",
    20116: "DRV_ERROR_UNMAP",
    20117: "DRV_ERROR_MDL",
    20118: "DRV_ERROR_UNMDL",
    20119: "DRV_ERROR_BUFFSIZE",
    20121: "DRV_ERROR_NOHANDLE",
    20130: "DRV_GATING_NOT_AVAILABLE",
    20131: "DRV_FPGA_VOLTAGE_ERROR",
    20150: "DRV_OW_CMD_FAIL",
    20151: "DRV_OWMEMORY_BAD_ADDR",
    20152: "DRV_OWCMD_NOT_AVAILABLE",
    20153: "DRV_OW_NO_SLAVES",
    20154: "DRV_OW_NOT_INITIALIZED",
    20155: "DRV_OW_ERROR_SLAVE_NUM",
    20156: "DRV_MSTIMINGS_ERROR",
    20173: "DRV_OA_NULL_ERROR",
    20174: "DRV_OA_PARSE_DTD_ERROR",
    20175: "DRV_OA_DTD_VALIDATE_ERROR",
    20176: "DRV_OA_FILE_ACCESS_ERROR",
    20177: "DRV_OA_FILE_DOES_NOT_EXIST",
    20178: "DRV_OA_XML_INVALID_OR_NOT_FOUND_ERROR",
    20179: "DRV_OA_PRESET_FILE_NOT_LOADED",
    20180: "DRV_OA_USER_FILE_NOT_LOADED",
    20181: "DRV_OA_PRESET_AND_USER_FILE_NOT_LOADED",
    20182: "DRV_OA_INVALID_FILE",
    20183: "DRV_OA_FILE_HAS_BEEN_MODIFIED",
    20184: "DRV_OA_BUFFER_FULL",
    20185: "DRV_OA_INVALID_STRING_LENGTH",
    20186: "DRV_OA_INVALID_CHARS_IN_NAME",
    20187: "DRV_OA_INVALID_NAMING",
    20188: "DRV_OA_GET_CAMERA_ERROR",
    20189: "DRV_OA_MODE_ALREADY_EXISTS",
    20190: "DRV_OA_STRINGS_NOT_EQUAL",
    20191: "DRV_OA_NO_USER_DATA",
    20192: "DRV_OA_VALUE_NOT_SUPPORTED",
    20193: "DRV_OA_MODE_DOES_NOT_EXIST",
    20194: "DRV_OA_CAMERA_NOT_SUPPORTED",
    20195: "DRV_OA_FAILED_TO_GET_MODE",
    20211: "DRV_PROCESSING_FAILED",
}

SUCCESS_CODE = 20002


class AndorCamera:
    def __init__(self):
        lib_dir = Path("/usr/local/lib/")
        lib_path = lib_dir / "libandor.so"
        self.__libandor__ = ctypes.cdll.LoadLibrary(lib_path)

        # Internal parameter references
        self.status: str = ""
        self.temperature: float = 0
        self.target_temperature: float = 0
        self.cooling_status: str = ""
        self.exposure_time: float = 0
        self.accumulate_time: float = 0
        self.kinetic_time: float = 0
        self.hbin: float = 0
        self.vbin: float = 0
        self.hstart: float = 0
        self.vstart: float = 0
        self.hend: float = 0
        self.vend: float = 0
        self.read_mode: int = 0
        self.acquisition_mode: int = 0
        self.n_kinetic: int = 1
        self.n_accumulation: int = 0
        self.temperature_min: int = 0
        self.temperature_max: int = 0
        self.is_connected: bool = False

    ## Wrapping methods from SDK

    def CancelWait(self):
        err_code = self.__libandor__.CancelWait()
        return ANDOR_CODES[err_code]

    def GetAvailableCameras(self) -> Tuple[int, str]:
        """
        GetAvailableCameras returns the total number of Andor cameras currently installed. It is
        possible to call this function before any of the cameras are initialized.
        """
        totalCameras = ctypes.c_long()
        err_code = self.__libandor__.GetAvailableCameras(ctypes.byref(totalCameras))
        return totalCameras.value, ANDOR_CODES[err_code]

    def GetTemperature(self) -> Tuple[float, str]:
        """
        GetTemperature This function returns the temperature of the detector to the nearest degree.
        It also gives the status of cooling process.


        Returns
        -------
        Tuple[float, str]
            TemperatureCamera

            Andor errror code, possible values
                DRV_NOT_INITIALIZED : System not initialized.
                DRV_ACQUIRING : Acquisition in progress.
                DRV_ERROR_ACK : Unable to communicate with card.
                DRV_TEMP_OFF : Temperature is OFF.
                DRV_TEMP_STABILIZED : Temperature has stabilized at set point.
                DRV_TEMP_NOT_REACHED : Temperature has not reached set point.
                DRV_TEMP_DRIFT : Temperature had stabilized but has since drifted
                DRV_TEMP_NOT_STABILIZED : Temperature reached but not stabilized
        """
        temp = ctypes.c_int()
        err_code = self.__libandor__.GetTemperature(ctypes.byref(temp))
        self.temperature = temp.value
        self.cooling_status = ANDOR_CODES[err_code]
        return temp.value, ANDOR_CODES[err_code]

    def GetNumberVSSpeeds(self):
        speeds = ctypes.c_int()
        err_code = self.__libandor__.GetNumberVSSpeeds(ctypes.byref(speeds))
        return speeds.value, ANDOR_CODES[err_code]

    def GetHSSpeed(self):
        speed = ctypes.c_float()
        err_code = self.__libandor__.GetHSSpeed(0, 0, 0, ctypes.byref(speed))
        return speed.value, ANDOR_CODES[err_code]

    def GetVSSpeed(self):
        speed = ctypes.c_float()
        err_code = self.__libandor__.GetVSSpeed(0, ctypes.byref(speed))
        return speed.value, ANDOR_CODES[err_code]

    def GetAcquisitionTimings(self):
        exposure = ctypes.c_float()
        accumulate = ctypes.c_float()
        kinetic = ctypes.c_float()
        err_code = self.__libandor__.GetAcquisitionTimings(
            ctypes.byref(exposure), ctypes.byref(accumulate), ctypes.byref(kinetic)
        )
        exposure = 1000 * exposure.value
        accumulate = 1000 * accumulate.value
        kinetic = 1000 * kinetic.value
        if err_code == SUCCESS_CODE:
            self.exposure_time = exposure
            self.accumulate_time = accumulate
            self.kinetic_time = kinetic
        return exposure, accumulate, kinetic, ANDOR_CODES[err_code]

    def GetDetector(self):
        """Returns Detector Size of the camera in a tuple

        Return format : (xpixel:int, ypixel:int)
        """
        xpixel = ctypes.c_int()
        ypixel = ctypes.c_int()
        err_code = self.__libandor__.GetDetector(
            ctypes.byref(xpixel), ctypes.byref(ypixel)
        )
        return xpixel.value, ypixel.value, ANDOR_CODES[err_code]

    def GetNumberHSSpeeds(self):
        channel = ctypes.c_int(0)
        typ = ctypes.c_int()
        speeds = ctypes.c_int()
        err_code = self.__libandor__.GetNumberHSSpeeds(
            channel, ctypes.byref(typ), ctypes.byref(speeds)
        )
        return typ.value, speeds.value, ANDOR_CODES[err_code]

    def GetTemperatureRange(self):
        minTemp = ctypes.c_int()
        maxTemp = ctypes.c_int()
        err_code = self.__libandor__.GetTemperatureRange(
            ctypes.byref(minTemp), ctypes.byref(maxTemp)
        )
        if err_code == SUCCESS_CODE:
            self.temperature_max = int(maxTemp.value)
            self.temperature_min = int(minTemp.value)

        return minTemp.value, maxTemp.value, ANDOR_CODES[err_code]

    def GetStatus(self):
        status = ctypes.c_int()
        err_code = self.__libandor__.GetStatus(ctypes.byref(status))
        if err_code == SUCCESS_CODE:
            status = ANDOR_CODES[int(status.value)]
            self.status = status
        else:
            status = ANDOR_CODES[err_code]
        return status, ANDOR_CODES[err_code]

    def IsCoolerOn(self):
        iCoolerStatus = ctypes.c_int()
        err_code = self.__libandor__.IsCoolerOn(ctypes.byref(iCoolerStatus))
        return iCoolerStatus.value, ANDOR_CODES[err_code]

    def GetAcquisitionProgress(self):
        acc = ctypes.c_int()
        series = ctypes.c_int()
        err_code = self.__libandor__.GetAcquisitionProgress(
            ctypes.byref(acc), ctypes.byref(series)
        )
        return acc.value, series.value, ANDOR_CODES[err_code]

    def GetHeadModel(self):
        name = ctypes.create_string_buffer(100)
        err_code = self.__libandor__.GetHeadModel(name)
        return name.value.decode(), ANDOR_CODES[err_code]

    def GetAcquiredData(self, size):
        InArray = (ctypes.c_int * size)()
        size = ctypes.c_int(size)
        err_code = self.__libandor__.GetAcquiredData((InArray), size)
        return InArray, ANDOR_CODES[err_code]

    def GetNumberPreAmpGains(self):
        nGain = ctypes.c_int()
        err_code = self.__libandor__.GetNumberPreAmpGains(ctypes.byref(nGain))
        return nGain.value, ANDOR_CODES[err_code]

    def GetCurrentPreAmpGain(self):
        gainIndex = ctypes.c_int()
        gainstr = ctypes.create_string_buffer(30)
        err_code = self.__libandor__.GetCurrentPreAmpGain(
            gainIndex, ctypes.byref(gainstr)
        )
        return gainIndex.value, gainstr.value.decode("utf-8"), ANDOR_CODES[err_code]

    def GetPreAmpGain(self):
        gainFactor = ctypes.c_int()
        err_code = self.__libandor__.GetPreAmpGain(0, ctypes.byref(gainFactor))
        return gainFactor.value, ANDOR_CODES[err_code]

    ## Setters

    def SetAcquisitionMode(self, mode):
        mode = mode + 1  # Weird choice, acquisition mode starts at 1...
        err_code = self.__libandor__.SetAcquisitionMode(mode)
        if err_code == SUCCESS_CODE:
            self.acquisition_mode = mode
        return ANDOR_CODES[err_code]

    def SetReadMode(self, mode):
        err_code = self.__libandor__.SetReadMode(mode)
        if err_code == SUCCESS_CODE:
            self.read_mode = mode
        return ANDOR_CODES[err_code]

    def SetShutter(self, TTLtype, mode, closingtime, openingtime):
        err_code = self.__libandor__.SetShutter(TTLtype, mode, closingtime, openingtime)
        return ANDOR_CODES[err_code]

    def SetExposureTime(self, time_ms):
        time_s = ctypes.c_float(time_ms / 1000)
        err_code = self.__libandor__.SetExposureTime(time_s)
        if err_code == SUCCESS_CODE:
            self.exposure_time = time_ms
        return ANDOR_CODES[err_code]

    def SetTriggerMode(self, mode):
        err_code = self.__libandor__.SetTriggerMode(mode)
        return ANDOR_CODES[err_code]

    def SetAccumulationCycleTime(self, time_ms):
        time_s = ctypes.c_float(time_ms / 1000)
        err_code = self.__libandor__.SetAccumulationCycleTime(time_s)
        return ANDOR_CODES[err_code]

    def SetNumberAccumulations(self, number):
        number = ctypes.c_int(number)
        err_code = self.__libandor__.SetNumberAccumulations(number)
        if err_code == SUCCESS_CODE:
            self.n_accumulation = int(number)
        return ANDOR_CODES[err_code]

    def SetNumberKinetics(self, number):
        number = ctypes.c_int(number)
        err_code = self.__libandor__.SetNumberKinetics(number)
        if err_code == SUCCESS_CODE:
            self.n_kinetic = number.value
        return ANDOR_CODES[err_code]

    def SetKineticCycleTime(self, cycle_time):
        err_code = self.__libandor__.SetKineticCycleTime(
            ctypes.c_float(cycle_time / 1000)
        )
        if err_code == SUCCESS_CODE:
            self.kinetic_time = cycle_time
        return ANDOR_CODES[err_code]

    def SetHSSpeed(self, amp, index):
        amp = ctypes.c_int(amp)
        index = ctypes.c_int(index)
        err_code = self.__libandor__.SetHSSpeed(amp, index)
        return ANDOR_CODES[err_code]

    def SetVSSpeed(self, index):
        index = ctypes.c_int(index)
        err_code = self.__libandor__.SetVSSpeed(index)
        return ANDOR_CODES[err_code]

    def SetImage(
        self, hbin: int, vbin: int, hstart: int, hend: int, vstart: int, vend: int
    ):
        hbin = ctypes.c_int(hbin)
        vbin = ctypes.c_int(vbin)
        hstart = ctypes.c_int(hstart)
        hend = ctypes.c_int(hend)
        vstart = ctypes.c_int(vstart)
        vend = ctypes.c_int(vend)
        err_code = self.__libandor__.SetImage(hbin, vbin, hstart, hend, vstart, vend)
        if err_code == SUCCESS_CODE:
            self.hbin = int(hbin.value)
            self.vbin = int(vbin.value)
            self.hstart = int(hstart.value)
            self.vstart = int(vstart.value)
            self.hend = int(hend.value)
            self.vend = int(vend.value)
        return ANDOR_CODES[err_code]

    def SetTemperature(self, temperature):
        temperature = ctypes.c_int(temperature)
        err_code = self.__libandor__.SetTemperature(temperature)
        if err_code == SUCCESS_CODE:
            self.target_temperature = temperature.value
        return ANDOR_CODES[err_code]

    def SetSingleTrack(self, center, height):
        center = ctypes.c_int(center)
        height = ctypes.c_int(height)
        err_code = self.__libandor__.SetSingleTrack(center, height)
        return ANDOR_CODES[err_code]

    def SetPreAmpGain(self, gainIndex):
        gain = ctypes.c_int(gainIndex)
        err_code = self.__libandor__.SetPreAmpGain((gain))
        return ANDOR_CODES[err_code]

    ## Camera actions

    def AbortAcquisition(self):
        err_code = self.__libandor__.AbortAcquisition()
        return ANDOR_CODES[err_code]

    def CoolerOn(self):
        err_code = self.__libandor__.CoolerON()
        return ANDOR_CODES[err_code]

    def CoolerOFF(self):
        err_code = self.__libandor__.CoolerOFF()
        return ANDOR_CODES[err_code]

    def Initialize(self):
        err_code = self.__libandor__.Initialize("/usr/local/etc/andor".encode("utf8"))
        error = ANDOR_CODES[err_code]
        return error

    def StartAcquisition(self):
        err_code = self.__libandor__.StartAcquisition()
        return ANDOR_CODES[err_code]

    def WaitForAcquisition(self):
        err_code = self.__libandor__.WaitForAcquisition()
        return ANDOR_CODES[err_code]

    def ShutDown(self):
        err_code = self.__libandor__.ShutDown()
        return ANDOR_CODES[err_code]

    ## Added methods for streamlining control of instruments

    def connect(self) -> str:
        n_camera_connected, error = self.GetAvailableCameras()

        if n_camera_connected != 1:
            return "No camera available"

        error = self.Initialize()

        if error == "DRV_SUCCESS":
            self.is_connected = True

        if self.is_connected:
            self.update_info()

        return error

    def disconnect(self) -> str:
        error = self.ShutDown()

        if error == "DRV_SUCCESS":
            self.is_connected = False
            self.status = "Disconnected"

        return error

    def update_info(self):
        self.GetTemperature()
        self.GetAcquisitionTimings()
        self.GetStatus()

    def get_info(self) -> dict:
        info_dict = {}

        info_dict["status"] = self.status

        info_dict["temperature"] = {
            "cooling_status": self.cooling_status,
            "current_temperature": self.temperature,
            "target_temperature": self.target_temperature,
        }

        info_dict["timing"] = {
            "exposure_time": self.exposure_time,
            "accumulate_time": self.accumulate_time,
            "kinetic_time": self.kinetic_time,
        }

        info_dict["acquisition_setting"] = {
            "acquisition_mode": self.acquisition_mode,
            "n_accumulation": self.n_accumulation,
            "n_kinetic": self.n_kinetic,
        }

        info_dict["read_setting"] = {
            "read_mode": self.read_mode,
        }

        return info_dict


class AndorAcquisition:
    def __init__(self, camera: AndorCamera):
        self.camera = camera

        # Get acquisition parameters from camera
        self.read_mode = camera.read_mode
        self.acquisition_mode = camera.acquisition_mode
        self.width = camera.hend - camera.hstart + 1
        self.height = camera.vend - camera.vstart + 1
        self.n_kinetic = camera.n_kinetic
        (
            exposure,
            accumulate,
            kinetic,
            _,
        ) = camera.GetAcquisitionTimings()
        self.valid_exposure = exposure
        self.valid_accumulation = accumulate
        self.valid_kinetic = kinetic

        self.data = None
        self.acquisition_progress = 0
        if self.acquisition_mode == 3:  # Kinetic
            self.n_scans = self.n_kinetic
        else:
            self.n_scans = 1

    def take_acquisition(self):
        logger.info("Starting acquisition")
        self.camera.StartAcquisition()
        self.camera.update_info()
        self.acquisition_progress = 0
        self.wait_for_acquisition()
        self.get_acquired_data()

    def wait_for_acquisition(self):
        logger.info("Waiting for acquisition")
        for i in range(self.n_scans):
            self.acquisition_progress = i
            msg = self.camera.WaitForAcquisition()
            if msg != "DRV_SUCCESS":
                msg = "ABORTED"
            logger.info(
                "Completed accumulation %i of %i - %s", i + 1, self.n_scans, msg
            )

    def abort_acquisition(self):
        n_abort = self.n_scans - self.acquisition_progress
        for _ in range(n_abort + 1):
            self.camera.CancelWait()
            self.camera.AbortAcquisition()
            self.camera.update_info()

    def get_acquired_data(self):
        logger.info("Getting data from camera")
        # get data
        size = self.get_data_size()
        self.data, _ = self.camera.GetAcquiredData(size)

    def get_data_size(self):
        if self.read_mode == 4:  # image mode
            size = self.width * self.height
        else:
            size = self.width

        if self.acquisition_mode == 3:  # kinetic
            size = size * self.n_kinetic

        return size

    def get_data(self):
        if not self.data:
            return None

        data = np.array(self.data)

        if self.read_mode == 4:  # image mode
            if self.acquisition_mode == 3:  # kinetic series
                # Reshape into [n_kinetic x (width*height)]
                images = data.reshape(
                    (self.n_kinetic, self.width * self.height), order="c"
                )
                data = []
                for image in images:
                    image = image.reshape((self.width, self.height), order="f")
                    data.append(image)

                data = np.stack(data)

            else:
                data = data.reshape((self.width, self.height), order="f")

        else:
            if self.camera.acquisition_mode == 3:
                data = data.reshape((self.width, self.n_kinetic), order="f")
                if self.n_kinetic > 1:
                    data = data.T
                else:
                    data = data.flatten()

        return data
