import ctypes
import logging
from dataclasses import dataclass
from pathlib import Path

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


@dataclass(kw_only=True)
class AndorInfo:
    # Basic confing
    model: str = ""
    serial_number: str = ""
    is_connected: bool = False
    temperature: float = float("nan")
    exposure_time: float = float("nan")  # [ms]
    # Normal config
    accumulate_time: float = float("nan")  # [ms]
    kinetic_time: float = float("nan")  # [ms]
    read_mode: float = float("nan")
    acquisition_mode: float = float("nan")
    n_accumulation: float = float("nan")
    n_kinetic: float = float("nan")
    is_cooler_on: float = False
    # Expert Config
    hbin: float = float("nan")
    vbin: float = float("nan")
    hstart: float = float("nan")
    vstart: float = float("nan")
    hend: float = float("nan")
    vend: float = float("nan")
    n_preamp_gains: float = float("nan")
    current_gain_index: float = float("nan")
    current_gain_desc: str = ""


@dataclass(kw_only=True)
class ShutterProfile:
    ttl_type: bool
    mode: int
    closing_time: int
    opening_time: int


@dataclass(kw_only=True)
class ImageConfig:
    hbin: int
    vbin: int
    hstart: int
    hend: int
    vstart: int
    vend: int


@dataclass(kw_only=True)
class SingleTrack:
    center: int = 0
    height: int = 0


class AndorCamera:
    def __init__(self):
        lib_dir = Path("/usr/local/lib/")
        lib_path = lib_dir / "libandor.so"
        self.__libandor__ = ctypes.cdll.LoadLibrary(lib_path)

        # Internal parameter references
        self.last_error_code = float("nan")
        self.last_error_msg = ""
        self.acquisition_mode: int = 0
        self.read_mode: int = 0
        self.shutter_profile: ShutterProfile
        self.trigger_mode: int = 0
        self.target_exposure_time: int = 0
        self.target_accumulation_time: int = 0
        self.target_kinetic_time: int = 0
        self.n_accumulation: int = 0
        self.n_kinetics: int = 0
        self.image_config: ImageConfig
        self.target_temperature: int = 0
        self.single_track: SingleTrack

    ## Wrapping methods from SDK

    ## Getters

    def GetAvailableCameras(self) -> int:
        """
        GetAvailableCameras returns the total number of Andor cameras currently installed. It is
        possible to call this function before any of the cameras are initialized.
        """
        totalCameras = ctypes.c_long()
        err_code = self.__libandor__.GetAvailableCameras(ctypes.byref(totalCameras))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(totalCameras.value)

    def GetTemperature(self) -> int:
        """
        GetTemperature This function returns the temperature of the detector to the nearest degree.
        It also gives the status of cooling process.


        Returns
        -------
        tuple[float, str]
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

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(temp.value)

    def GetNumberHSSpeeds(self) -> int:
        channel = ctypes.c_int(0)
        _type = ctypes.c_int()
        speeds = ctypes.c_int()
        err_code = self.__libandor__.GetNumberHSSpeeds(
            channel, ctypes.byref(_type), ctypes.byref(speeds)
        )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(speeds.value)

    def GetNumberVSSpeeds(self) -> int:
        speeds = ctypes.c_int()
        err_code = self.__libandor__.GetNumberVSSpeeds(ctypes.byref(speeds))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(speeds.value)

    def GetHSSpeed(self) -> float:
        speed = ctypes.c_float()
        err_code = self.__libandor__.GetHSSpeed(0, 0, 0, ctypes.byref(speed))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return float(speed.value)

    def GetVSSpeed(self) -> float:
        speed = ctypes.c_float()
        err_code = self.__libandor__.GetVSSpeed(0, ctypes.byref(speed))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return float(speed.value)

    def GetAcquisitionTimings(self) -> tuple[float, float, float]:
        exposure_time = ctypes.c_float()
        accumulate_cycle = ctypes.c_float()
        kinetic_cycle = ctypes.c_float()

        err_code = self.__libandor__.GetAcquisitionTimings(
            ctypes.byref(exposure_time),
            ctypes.byref(accumulate_cycle),
            ctypes.byref(kinetic_cycle),
        )

        exposure_time = 1000 * float(exposure_time.value)
        accumulate_cycle = 1000 * float(accumulate_cycle.value)
        kinetic_cycle = 1000 * float(kinetic_cycle.value)

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return exposure_time, accumulate_cycle, kinetic_cycle

    def GetDetector(self) -> tuple[int, int]:
        """Returns Detector Size of the camera in a tuple

        Return format : (xpixel:int, ypixel:int)
        """
        xpixel = ctypes.c_int()
        ypixel = ctypes.c_int()
        err_code = self.__libandor__.GetDetector(
            ctypes.byref(xpixel), ctypes.byref(ypixel)
        )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(xpixel.value), int(ypixel.value)

    def GetTemperatureRange(self) -> tuple[int, int]:
        minTemp = ctypes.c_int()
        maxTemp = ctypes.c_int()
        err_code = self.__libandor__.GetTemperatureRange(
            ctypes.byref(minTemp), ctypes.byref(maxTemp)
        )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(minTemp.value), int(maxTemp.value)

    def GetStatus(self) -> int:
        status = ctypes.c_int()
        err_code = self.__libandor__.GetStatus(ctypes.byref(status))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(status.value)

    def IsCoolerOn(self) -> bool:
        cooler_on = ctypes.c_int()
        err_code = self.__libandor__.IsCoolerOn(ctypes.byref(cooler_on))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return cooler_on.value == 1

    def GetAcquisitionProgress(self) -> tuple[int, int]:
        acc = ctypes.c_int()
        series = ctypes.c_int()
        err_code = self.__libandor__.GetAcquisitionProgress(
            ctypes.byref(acc), ctypes.byref(series)
        )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(acc.value), int(series.value)

    def GetHeadModel(self) -> str:
        name = ctypes.create_string_buffer(260)
        err_code = self.__libandor__.GetHeadModel(name)

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return str(name.value.decode())

    def GetAcquiredData(self, size):
        InArray = (ctypes.c_int * size)()
        size = ctypes.c_int(size)
        err_code = self.__libandor__.GetAcquiredData((InArray), size)

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return InArray

    def GetNumberPreAmpGains(self) -> int:
        nGain = ctypes.c_int()
        err_code = self.__libandor__.GetNumberPreAmpGains(ctypes.byref(nGain))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(nGain.value)

    def GetCurrentPreAmpGain(self) -> tuple[int, str]:
        gainIndex = ctypes.c_int()
        gainstr = ctypes.create_string_buffer(30)
        err_code = self.__libandor__.GetCurrentPreAmpGain(
            gainIndex, ctypes.byref(gainstr)
        )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return int(gainIndex.value), str(gainstr.value.decode("utf-8"))

    def GetPreAmpGain(self, gain_index=0) -> float:
        gain_index = ctypes.c_int(gain_index)
        gain_factor = ctypes.c_float()
        err_code = self.__libandor__.GetPreAmpGain(
            gain_index, ctypes.byref(gain_factor)
        )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

        return float(gain_factor.value)

    ## Setters

    def SetAcquisitionMode(self, mode: int = 1) -> None:
        err_code = self.__libandor__.SetAcquisitionMode(mode)

        if err_code == SUCCESS_CODE:
            self.acquisition_mode = mode

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetReadMode(self, mode: int = 0) -> None:
        err_code = self.__libandor__.SetReadMode(mode)

        if err_code == SUCCESS_CODE:
            self.read_mode = mode

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetShutter(
        self,
        TTLtype: int = 1,
        mode: int = 0,
        closing_time: int = 0,
        opening_time: int = 0,
    ) -> None:
        err_code = self.__libandor__.SetShutter(
            TTLtype, mode, closing_time, opening_time
        )

        if err_code == SUCCESS_CODE:
            self.shutter_profile = ShutterProfile(
                ttl_type=TTLtype,
                mode=mode,
                closing_time=closing_time,
                opening_time=opening_time,
            )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetExposureTime(self, time_ms: int) -> None:
        time_s = ctypes.c_float(time_ms / 1000)
        err_code = self.__libandor__.SetExposureTime(time_s)

        if err_code == SUCCESS_CODE:
            self.target_exposure_time = time_ms

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetTriggerMode(self, mode: int) -> None:
        err_code = self.__libandor__.SetTriggerMode(mode)

        if err_code == SUCCESS_CODE:
            self.trigger_mode = mode

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetAccumulationCycleTime(self, time_ms: int) -> None:
        time_s = ctypes.c_float(time_ms / 1000)
        err_code = self.__libandor__.SetAccumulationCycleTime(time_s)

        if err_code == SUCCESS_CODE:
            self.target_accumulation_time = time_ms

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetNumberAccumulations(self, n_accumulations: int) -> None:
        n = ctypes.c_int(n_accumulations)
        err_code = self.__libandor__.SetNumberAccumulations(n)

        if err_code == SUCCESS_CODE:
            self.n_accumulation = n_accumulations

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetNumberKinetics(self, n_kinetics: int) -> None:
        n = ctypes.c_int(n_kinetics)
        err_code = self.__libandor__.SetNumberKinetics(n)

        if err_code == SUCCESS_CODE:
            self.n_kinetics = n_kinetics

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetKineticCycleTime(self, time_ms: int) -> None:
        time_s = ctypes.c_float(time_ms / 1000)
        err_code = self.__libandor__.SetKineticCycleTime(time_s)

        if err_code == SUCCESS_CODE:
            self.target_kinetic_time = time_ms

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetHSSpeed(self, typ: int, index: int) -> None:
        amp = ctypes.c_int(typ)
        index = ctypes.c_int(index)
        err_code = self.__libandor__.SetHSSpeed(amp, index)

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetVSSpeed(self, index: int):
        index = ctypes.c_int(index)
        err_code = self.__libandor__.SetVSSpeed(index)

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetImage(
        self, hbin: int, vbin: int, hstart: int, hend: int, vstart: int, vend: int
    ) -> None:
        hbin = ctypes.c_int(hbin)
        vbin = ctypes.c_int(vbin)
        hstart = ctypes.c_int(hstart)
        hend = ctypes.c_int(hend)
        vstart = ctypes.c_int(vstart)
        vend = ctypes.c_int(vend)
        err_code = self.__libandor__.SetImage(hbin, vbin, hstart, hend, vstart, vend)

        if err_code == SUCCESS_CODE:
            self.image_config = ImageConfig(
                hbin=hbin, vbin=vbin, hstart=hstart, vstart=vstart, hend=hend, vend=vend
            )

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetTemperature(self, temperature: int):
        t = ctypes.c_int(temperature)
        err_code = self.__libandor__.SetTemperature(t)

        if err_code == SUCCESS_CODE:
            self.target_temperature = temperature

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetSingleTrack(self, center: int, height: int):
        c = ctypes.c_int(center)
        h = ctypes.c_int(height)
        err_code = self.__libandor__.SetSingleTrack(c, h)

        if err_code == SUCCESS_CODE:
            self.single_track = SingleTrack(center=center, height=height)

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def SetPreAmpGain(self, gainIndex: int):
        gain = ctypes.c_int(gainIndex)
        err_code = self.__libandor__.SetPreAmpGain((gain))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    ## Camera actions

    def AbortAcquisition(self) -> None:
        err_code = self.__libandor__.AbortAcquisition()

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def CancelWait(self) -> None:
        err_code = self.__libandor__.CancelWait()

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def CoolerOn(self) -> None:
        err_code = self.__libandor__.CoolerON()

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def CoolerOFF(self) -> None:
        err_code = self.__libandor__.CoolerOFF()

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def Initialize(self) -> None:
        err_code = self.__libandor__.Initialize("/usr/local/etc/andor".encode("utf8"))

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def StartAcquisition(self) -> None:
        err_code = self.__libandor__.StartAcquisition()

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def WaitForAcquisition(self) -> None:
        err_code = self.__libandor__.WaitForAcquisition()

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    def ShutDown(self) -> None:
        err_code = self.__libandor__.ShutDown()

        self.last_error_code = err_code
        self.last_error_msg = ANDOR_CODES[err_code]
        logger.debug("%i, %s", self.last_error_code, self.last_error_msg)

    ## compound methods

    def connect(self) -> None:
        self.Initialize()
        self.apply_default_settings()

    def disconnect(self) -> None:
        self.apply_default_settings()
        self.ShutDown()

    def apply_default_settings(self) -> None:

        self.SetAcquisitionMode()
        self.SetReadMode()
        self.SetShutter()
        self.SetExposureTime(0)
        self.SetTriggerMode(0)

        self.SetAccumulationCycleTime(0)
        self.SetNumberAccumulations(1)
        self.SetNumberKinetics(1)
        self.SetKineticCycleTime(0)

        _, maxTemp = self.GetTemperatureRange()
        self.SetTemperature(maxTemp)
        self.CoolerOn()

        # Image binning
        xpixel, ypixel = self.GetDetector()
        self.SetImage(hbin=1, vbin=1, hstart=1, vstart=1, hend=xpixel, vend=ypixel)
        self.SetSingleTrack(ypixel // 2, ypixel // 2)

    def get_info(self) -> dict:
        pass


if __name__ == "__main__":

    LOG_FORMAT = (
        "%(asctime)s - %(levelname)s"
        "(%(filename)s:%(funcName)s)"
        "(%(filename)s:%(lineno)d) - "
        "%(message)s"
    )
    formatter = logging.Formatter(LOG_FORMAT)
    terminal_handler = logging.StreamHandler()
    terminal_handler.setFormatter(formatter)
    logger.addHandler(terminal_handler)
    logger.setLevel(logging.DEBUG)

    camera = AndorCamera()

    camera.connect()
    camera.disconnect()
