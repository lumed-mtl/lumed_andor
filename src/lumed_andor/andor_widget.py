import logging

import matplotlib.pyplot as plt
from PyQt5.QtCore import QThreadPool, QTimer
from PyQt5.QtWidgets import QWidget

from lumed_andor.andor_control import AndorAcquisition, AndorCamera
from lumed_andor.ui.andor_ui import Ui_andorCameraWidget
from lumed_andor.workerthreads import Worker

logger = logging.getLogger(__name__)


class AndorCameraWidget(QWidget, Ui_andorCameraWidget):
    def __init__(self):
        super().__init__()
        logger.info("initializing andorCameraWidget")
        self.setupUi(self)

        self.connectingToAndorDrivers()
        if not self.camera:
            self.setEnabled(False)
            return

        self.threadpool = QThreadPool(parent=self)

        # Only 1 thread at a time to talk to camera!!!
        # More can cause seg faults
        self.threadpool.setMaxThreadCount(1)

        # Backend refs
        self.current_acquisition: AndorAcquisition = None

        # UI stuff
        self.setDefaultUI()
        self.connectSlots()

        # Create update timer
        self.update_camera_info()
        self.updateStatusTimer = QTimer()
        self.updateStatusTimer.setInterval(100)
        self.updateStatusTimer.timeout.connect(self.update_camera_info)
        self.updateStatusTimer.start()

        self.sync_delay = self.syncDelaySpinBox.value()

    def connectingToAndorDrivers(self):
        # Attempts to create an AndorCamera.
        # If the andor drivers are not installed, this will fail!
        try:
            self.camera = AndorCamera()
            logger.info("Andor camera drivers successfully loaded")
        except OSError as e:
            self.camera = None
            logger.warning("%s Cannot load Andor camera drivers.", e)

    def setDefaultUI(self):
        # readModes
        self.readModeComboBox.addItems(
            [
                "Full Vertical Binning",
                "Multi-Track",
                "Random-Track",
                "Single-Track",
                "Image",
            ]
        )
        # Disabeling not implemented options
        self.readModeComboBox.model().item(1).setEnabled(False)
        self.readModeComboBox.model().item(2).setEnabled(False)

        # acquisitionModes
        self.acquisitionModeComboBox.addItems(
            ["Single Scan", "Accumulate", "Kinetics", "Fast Kinetics", "Run till abort"]
        )
        # Disabeling not implemented options

        self.acquisitionModeComboBox.model().item(1).setEnabled(False)
        self.acquisitionModeComboBox.model().item(3).setEnabled(False)
        self.acquisitionModeComboBox.model().item(4).setEnabled(False)

        self.abortButton.setEnabled(False)

    def connectSlots(self):
        logger.info("Connecting Slots")
        self.initializeButton.clicked.connect(self.initializedButtonClicked)
        self.closeButton.clicked.connect(self.closeButtonClicked)
        self.temperatureSpinBox.valueChanged.connect(self.temperatureChanged)
        self.exposureTimeSpinBox.valueChanged.connect(self.exposureChanged)
        self.acquisitionButton.clicked.connect(self.acquisitionButtonClicked)
        self.abortButton.clicked.connect(self.abort_acquisition)
        self.syncDelaySpinBox.valueChanged.connect(self.syncDelayChanged)

        # Read Mode
        self.readModeComboBox.currentIndexChanged.connect(self.readModeChanged)
        self.singleTrackNumSpinBox.valueChanged.connect(self.singleTrackChanged)
        self.singleTrackWidthSpinBox.valueChanged.connect(self.singleTrackChanged)

        # Acquisition Mode
        self.acquisitionModeComboBox.currentIndexChanged.connect(
            self.acquisitionModeChanged
        )
        self.kineticNumberSpinBox.valueChanged.connect(self.kineticNumberChanged)
        self.kineticTimeSpinBox.valueChanged.connect(self.kineticTimeChanged)

    def updateUI(self):
        if not self.camera:
            self.initializeButton.setEnabled(True)
            self.closeButton.setEnabled(False)
            return

        if self.camera.is_connected:
            self.initializeButton.setEnabled(False)
            self.closeButton.setEnabled(True)
            self.temperatureSpinBox.setEnabled(True)
            self.exposureTimeSpinBox.setEnabled(True)
            self.acquisitionButton.setEnabled(True)
            self.readModeComboBox.setEnabled(True)
            self.singleTrackNumSpinBox.setEnabled(True)
            self.singleTrackWidthSpinBox.setEnabled(True)
            self.acquisitionModeComboBox.setEnabled(True)
            self.kineticNumberSpinBox.setEnabled(True)
            self.kineticTimeSpinBox.setEnabled(True)
            self.syncDelaySpinBox.setEnabled(True)

        else:  # not connected
            self.initializeButton.setEnabled(True)
            self.closeButton.setEnabled(False)
            self.temperatureSpinBox.setEnabled(False)
            self.exposureTimeSpinBox.setEnabled(False)
            self.acquisitionButton.setEnabled(False)
            self.readModeComboBox.setEnabled(False)
            self.singleTrackNumSpinBox.setEnabled(False)
            self.singleTrackWidthSpinBox.setEnabled(False)
            self.acquisitionModeComboBox.setEnabled(False)
            self.kineticNumberSpinBox.setEnabled(False)
            self.kineticTimeSpinBox.setEnabled(False)
            self.syncDelaySpinBox.setEnabled(False)

        # General camera info
        self.cameraStatus.setText(self.camera.status)
        self.temperatureLabel.setText(str(self.camera.temperature))
        self.coolingStatusLabel.setText(self.camera.cooling_status)
        self.exposureTimeSpinBox.setValue(int(self.camera.exposure_time))
        # Read Mode Box
        self.readModeComboBox.setCurrentIndex(self.camera.read_mode)
        # Acquisition Mode Box
        self.acquisitionModeComboBox.setCurrentIndex(self.camera.acquisition_mode - 1)
        self.kineticNumberSpinBox.setValue(int(self.camera.n_kinetic))
        self.kineticTimeSpinBox.setValue(int(self.camera.kinetic_time))

    # Callbacks

    def initializedButtonClicked(self):
        # initializing camera
        worker = Worker(self.initialize_camera)
        self.threadpool.start(worker)

    def closeButtonClicked(self):
        # Closing camera
        worker = Worker(self.close_camera)
        self.threadpool.start(worker)

    def temperatureChanged(self):
        new_target_temp = self.temperatureSpinBox.value()
        if new_target_temp == self.camera.target_temperature:
            return

        self.threadpool.waitForDone()
        andor_msg = self.camera.SetTemperature(new_target_temp)
        logger.info("target temperature changed - %i - %s", new_target_temp, andor_msg)

    def exposureChanged(self):
        new_exposure_time = self.exposureTimeSpinBox.value()
        if new_exposure_time == self.camera.exposure_time:
            return

        self.threadpool.waitForDone()
        andor_msg = self.camera.SetExposureTime(new_exposure_time)
        logger.info("exposure time changed - %i ms - %s", new_exposure_time, andor_msg)

    def updateAcquisitionTiming(self):
        # updating acquisition timings
        exposure_time, _, kinetic_time, _ = self.camera.GetAcquisitionTimings()
        self.exposureTimeSpinBox.setValue(int(exposure_time))
        self.kineticTimeSpinBox.setValue(int(kinetic_time))

    def acquisitionButtonClicked(self):
        self.updateAcquisitionTiming()
        self.abortButton.setEnabled(True)
        self.acquisitionButton.setEnabled(False)
        # Test acquisition
        worker = Worker(self.test_acquisition)
        worker.signals.result.connect(self.post_test_acquisition)
        self.threadpool.start(worker)

    def abort_acquisition(self):
        logger.warning("Abborting acquisition")
        self.current_acquisition.abort_acquisition()

    def syncDelayChanged(self):
        new_sync_delay = self.syncDelaySpinBox.value()
        self.sync_delay = new_sync_delay
        logger.info("sync delay changed - %i", new_sync_delay)

    def readModeChanged(self):
        new_readMode_index = self.readModeComboBox.currentIndex()
        new_readMode = self.readModeComboBox.currentText()
        if new_readMode_index == self.camera.read_mode:
            return

        self.threadpool.waitForDone()
        andor_msg = self.camera.SetReadMode(new_readMode_index)
        logger.info("readMode changed to - %s - %s", new_readMode, andor_msg)

    def singleTrackChanged(self):
        new_num = self.singleTrackNumSpinBox.value()
        new_width = self.singleTrackWidthSpinBox.value()

        self.threadpool.waitForDone()
        andor_msg = self.camera.SetSingleTrack(new_num, new_width)
        logger.info(
            "Single Track changed - center:%i, width:%i - %s",
            new_num,
            new_width,
            andor_msg,
        )

    def acquisitionModeChanged(self):
        new_acquiMode_index = self.acquisitionModeComboBox.currentIndex()
        new_acquiMode = self.acquisitionModeComboBox.currentText()

        if new_acquiMode_index == self.camera.acquisition_mode - 1:
            return

        self.threadpool.waitForDone()
        andor_msg = self.camera.SetAcquisitionMode(new_acquiMode_index)
        logger.info("readMode changed to - %s - %s", new_acquiMode, andor_msg)

    def kineticNumberChanged(self):
        new_kineticNumber = self.kineticNumberSpinBox.value()
        if new_kineticNumber == self.camera.n_kinetic:
            return

        self.threadpool.waitForDone()
        andor_msg = self.camera.SetNumberKinetics(new_kineticNumber)
        logger.info("kinetic number changed - %i - %s", new_kineticNumber, andor_msg)

    def kineticTimeChanged(self):
        new_kineticTime = self.kineticTimeSpinBox.value()
        if new_kineticTime == self.camera.kinetic_time:
            return

        self.threadpool.waitForDone()
        andor_msg = self.camera.SetKineticCycleTime(new_kineticTime)
        logger.info("kinetic time changed - %i - %s", new_kineticTime, andor_msg)

    # Backend

    def initialize_camera(self):
        """
        initialize_camera creates an AndorCamera object, add a reference to andorCameraWidget.camera
        and runs the initialization procedure for the andor camera.
        """
        logger.info("initializing camera")
        self.connectingToAndorDrivers()

        if not self.camera:
            return

        # Initializing steps
        andor_msg = self.camera.connect()
        if self.camera.is_connected:
            logger.info("Connected andor camera - %s", andor_msg)
        else:
            logger.warning("Failed to connect camera - %s", andor_msg)
            return

        # Detector sizing
        width, height, andor_msg = self.camera.GetDetector()
        andor_msg = self.camera.SetImage(1, 1, 1, width, 1, height)
        self.singleTrackNumSpinBox.setRange(1, height)
        self.singleTrackWidthSpinBox.setRange(1, int(height / 2))
        logger.info("setted image size to detector size - %s", andor_msg)

        # Temperature Range
        temp_min, temp_max, andor_msg = self.camera.GetTemperatureRange()
        logger.info("Temperature range - %i : %i - %s", temp_min, temp_max, andor_msg)

        andor_msg = self.camera.SetReadMode(0)  # FVB
        logger.info("setted ReadMode - %s", andor_msg)

        andor_msg = self.camera.SetAcquisitionMode(0)  # single scan
        logger.info("setted acquisition mode to single scan - %s", andor_msg)

        andor_msg = self.camera.SetShutter(1, 0, 0, 0)
        logger.info("setted shutter - %s", andor_msg)

        andor_msg = self.camera.SetTriggerMode(0)
        logger.info("setted trigger mode - %s", andor_msg)

        andor_msg = self.camera.CoolerOn()
        logger.info("turned cooler ON - %s", andor_msg)

        _, _, _, andor_msg = self.camera.GetAcquisitionTimings()
        logger.info("turned cooler ON - %s", andor_msg)

    def update_status(self):
        if self.threadpool.activeThreadCount() > 0:
            # This skip prevents 2 different thread attempting to poll the camera
            # which would result in a crash
            return
        elif not self.camera:
            self.updateUI()
            return

        if self.camera.is_connected:
            # Update camera info
            self.camera.GetStatus()
            self.temperatureSpinBox.setRange(
                self.camera.temperature_min, self.camera.temperature_max
            )
            self.camera.GetTemperature()

        self.updateUI()

    def test_acquisition(self):
        self.current_acquisition = AndorAcquisition(self.camera)
        self.current_acquisition.take_acquisition()

    def post_test_acquisition(self):
        logger.info("Test Acquisition completed - Plotting results")
        self.abortButton.setEnabled(False)
        # Create figure
        fig = plt.figure()

        acquisition_mode = self.current_acquisition.acquisition_mode
        read_mode = self.current_acquisition.read_mode
        data = self.current_acquisition.get_data()

        # Kinetic image
        if read_mode == 4 and acquisition_mode == 3:
            for i, image in enumerate(data):
                plt.subplot(data.shape[0], 1, i + 1)
                plt.imshow(image.T)

        # Single scan image
        elif read_mode == 4:
            plt.imshow(data.T)

        elif data.ndim > 1:
            for signal in data:
                plt.plot(signal)
        else:
            plt.plot(data)

        plt.tight_layout()
        fig.show()

    def close_camera(self):
        # Turn cooler off
        andor_msg = self.camera.CoolerOFF()
        logger.info("turned cooler OFF - %s", andor_msg)

        # Shutdown camera
        andor_msg = self.camera.disconnect()
        logger.info("closed camera - %s", andor_msg)
