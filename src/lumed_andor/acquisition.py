import logging
from dataclasses import dataclass, field

import numpy as np
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from lumed_andor.andor_control import AndorCamera, AndorInfo, AndorSettings

logger = logging.getLogger()


@dataclass
class AcquisitionResult:
    data = np.ndarray
    camera_info: AndorInfo = field(default_factory=AndorInfo)
    camera_settings: AndorSettings = field(default_factory=AndorSettings)


class AcquisitionSignals(QObject):
    progress = pyqtSignal(float)
    started = pyqtSignal(bool)
    finished = pyqtSignal(bool)


class AndorAcquisition(QRunnable):

    def __init__(self, camera: AndorCamera):
        super().__init__()
        self.camera: AndorCamera = camera
        self.result: AcquisitionResult = AcquisitionResult()
        self.result.camera_settings = camera.get_settings()
        self.signals: AcquisitionSignals = AcquisitionSignals()
        self.in_progress: bool = False
        self.acquisition_progress: int = 0
        self.n_scans: int = 1

    def apply_settings(self, settings: AndorSettings):
        logger.info("Applying camera settings %s", settings)
        self.camera.apply_settings(settings)
        # logger.info("")
        self.result.camera_settings = self.camera.get_settings()

    @pyqtSlot()
    def run(self):
        logger.info("Starting acquisition")
        if self.result.camera_settings.acquisition_mode == 3:  # Kinetic Series
            self.n_scans = self.camera.number_kinetics
        else:
            self.n_scans = 1

        self.acquisition_progress = 0
        self.camera.StartAcquisition()
        self.in_progress = True
        self.wait_for_acquisition()
        self.in_progress = False
        self.get_camera_info()
        n_kinetic, width, height = self.get_data_size()
        self.get_data(n_kinetic, width, height)
        self.signals.finished.emit(True)

    def wait_for_acquisition(self):
        logger.info("Waiting for acquisition")

        n_scans = self.n_scans

        for i in range(n_scans):
            self.signals.progress.emit(i / n_scans)
            self.camera.get_info()
            self.camera.WaitForAcquisition()
            self.acquisition_progress = self.acquisition_progress + 1

            last_error = self.camera.last_error
            if not last_error.is_success:
                msg = "ACQUISITION ABORTED"
            else:
                msg = last_error.message
            logger.info("Completed accumulation %i of %i - %s", i + 1, n_scans, msg)

    def get_camera_info(self):
        self.camera.get_info()
        self.result.camera_info = self.camera.info

    def abort_acquisition(self):
        while self.in_progress:
            self.camera.AbortAcquisition()
            self.camera.CancelWait()

    def get_data_size(self):
        camera_settings = self.result.camera_settings
        camera_info = self.result.camera_info
        read_mode = camera_settings.read_mode
        acquisition_mode = camera_settings.acquisition_mode

        if acquisition_mode == 3:  # kinetic series
            n_kinetic = camera_settings.number_kinetic
        else:
            n_kinetic = 1

        if read_mode == 0:  # FVB
            width = camera_info.xpixels
            height = 1
        elif read_mode == 1:  # Multi-Track TODO
            width = camera_info.xpixels
            height = camera_settings.multi_track.number
        elif read_mode == 2:  # Random-Track TODO
            width = camera_info.xpixels
            height = len(camera_settings.random_track.tracks) // 2
        elif read_mode == 3:  # Single-Track
            width = camera_info.xpixels
            height = 1
        elif read_mode == 4:  # image mode
            image_config = camera_settings.image_config
            width = (image_config.hend - image_config.hstart + 1) // image_config.hbin
            height = (image_config.vend - image_config.vstart + 1) // image_config.vbin

        return n_kinetic, width, height

    def get_data(self, n_kinetic, width, height):

        data: np.ndarray = np.array(
            self.camera.GetAcquiredData(size=n_kinetic * width * height)
        )

        # Reshaping data
        data = data.reshape((n_kinetic, height, width))
        self.result.data = data
