import logging
from dataclasses import asdict

import matplotlib.pyplot as plt
import tomli_w
from PyQt5.QtCore import QThreadPool, QTimer
from PyQt5.QtWidgets import QWidget

from lumed_andor.acquisition import AndorAcquisition
from lumed_andor.andor_control import AndorCamera
from lumed_andor.device_worker import DeviceWorker
from lumed_andor.ui.andor_ui import Ui_andorCameraWidget

logger = logging.getLogger(__name__)


class AndorCameraWidget(QWidget, Ui_andorCameraWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Widget intialization")
        self.setupUi(self)

        # Threadpool
        self.threadpool = QThreadPool(parent=self)
        self.threadpool.setMaxThreadCount(1)
        # Only 1 thread at a time to talk to camera!!!
        # More can cause seg faults

        # Connecting to device
        self.connectingToAndorDrivers()
        if not self.camera:
            self.setEnabled(False)
            return

        # Backend refs
        self.current_acquisition: AndorAcquisition = AndorAcquisition(self.camera)

        # ui configuration
        self.set_default_ui()
        self.connect_ui_signals()
        self.setup_update_timer()

        self.update_ui()
        logger.info("Widget initialization complete")

    def setup_update_timer(self):
        """Creates the PyQt Timer and connects it to the function that updates
        the UI and gets the laser infos."""
        self.update_timer = QTimer()
        self.update_timer.setInterval(100)

        self.update_timer.timeout.connect(self.trigger_camera_update)
        self.update_timer.timeout.connect(self.update_ui)

    def connectingToAndorDrivers(self):
        # Attempts to create an AndorCamera.
        # If the andor drivers are not installed, this will fail!
        try:
            self.camera = AndorCamera()
            logger.info("Andor camera drivers successfully loaded")
        except OSError as e:
            self.camera = None
            logger.warning("%s Cannot load Andor camera drivers.", e)

    def set_default_ui(self):
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

        # Disabling not implemented options
        self.readModeComboBox.model().item(1).setEnabled(False)
        self.readModeComboBox.model().item(2).setEnabled(False)

        # acquisitionModes
        self.acquisitionModeComboBox.addItems(
            ["Single Scan", "Accumulate", "Kinetics", "Fast Kinetics", "Run till abort"]
        )
        # Disabling not implemented options
        self.acquisitionModeComboBox.model().item(1).setEnabled(False)
        self.acquisitionModeComboBox.model().item(3).setEnabled(False)
        self.acquisitionModeComboBox.model().item(4).setEnabled(False)

    def connect_ui_signals(self):
        logger.info("Connecting Slots to UI signals")
        self.pushbtnConnect.clicked.connect(self.connectBtnClicked)
        self.pushbtnDisconnect.clicked.connect(self.disconnectBtnClicked)

        self.temperatureSpinBox.valueChanged.connect(self.set_target_temperature)
        self.exposureTimeSpinBox.valueChanged.connect(self.set_exposure_time)

        # Read Mode
        self.readModeComboBox.currentIndexChanged.connect(self.set_readmode)
        self.singleTrackCenterSpinBox.valueChanged.connect(self.set_single_track)
        self.singleTrackHeightSpinBox.valueChanged.connect(self.set_single_track)

        # Acquisition Mode
        self.acquisitionModeComboBox.currentIndexChanged.connect(
            self.set_acquisition_mode
        )
        self.kineticNumberSpinBox.valueChanged.connect(self.set_kinetic_number)
        self.kineticTimeSpinBox.valueChanged.connect(self.set_kinetic_cycle)

        # Test acquisition
        self.testAcquisitionBtn.clicked.connect(self.acquisitionBtnClicked)
        self.abortTestAcquisitionBtn.clicked.connect(self.abort_acquisition)

    def trigger_camera_update(self):
        worker = DeviceWorker(self.camera.get_info)
        self.threadpool.start(worker)

    def update_ui(self):

        # Enable/disable controls if camera is connected or not
        self.pushbtnConnect.setEnabled(not self.camera.is_connected)
        self.pushbtnDisconnect.setEnabled(self.camera.is_connected)
        self.groupBoxBasicControl.setEnabled(self.camera.is_connected)
        self.tabAdvancedControl.setEnabled(self.camera.is_connected)
        self.testAcquisitionBtn.setEnabled(not self.current_acquisition.in_progress)
        self.abortTestAcquisitionBtn.setEnabled(self.current_acquisition.in_progress)

        # info txtbox
        self.plainTxtInfo.setPlainText(tomli_w.dumps(asdict(self.camera.info)))

        # current settings txtbox
        self.plainTxtCurrentSettings.setPlainText(
            tomli_w.dumps(asdict(self.camera.get_settings()))
        )

        # General camera info
        self.cameraStatus.setText(self.camera.info.status.message)
        self.temperatureLabel.setText(str(self.camera.info.temperature))
        self.coolingStatusLabel.setText(self.camera.info.cooling_status)
        self.exposureTimeSpinBox.setValue(int(self.camera.target_exposure_time))

        # Read Mode Box
        self.readModeComboBox.setCurrentIndex(self.camera.read_mode)
        self.singleTrackCenterSpinBox.setValue(int(self.camera.single_track.center))
        self.singleTrackHeightSpinBox.setValue(int(self.camera.single_track.height))

        # Acquisition Mode Box
        self.acquisitionModeComboBox.setCurrentIndex(self.camera.acquisition_mode - 1)
        self.kineticNumberSpinBox.setValue(int(self.camera.number_kinetics))
        self.kineticTimeSpinBox.setValue(int(self.camera.target_kinetic_time))

    def connectBtnClicked(self):
        logger.info("Connecting to Andor camera")
        self.pushbtnConnect.setEnabled(False)

        worker = DeviceWorker(self.camera.connect)
        worker.signals.finished.connect(self.post_camera_connection)
        self.threadpool.start(worker)

    def disconnectBtnClicked(self):
        logger.info("Disconnecting Andor camera")
        self.pushbtnDisconnect.setEnabled(False)
        self.update_timer.stop()

        worker = DeviceWorker(self.camera.disconnect)
        worker.signals.finished.connect(self.post_camera_disconnection)
        self.threadpool.start(worker)

    def post_camera_connection(self):
        error = self.camera.last_error
        if error.is_success:
            logger.info(
                "Successfully connected to Andor Camera - %i - %s",
                error.code,
                error.message,
            )
            self.set_control_bounds()
            self.update_timer.start()

    def set_control_bounds(self):
        # Temperature
        self.temperatureSpinBox.setMinimum(self.camera.info.min_temperature)
        self.temperatureSpinBox.setMaximum(self.camera.info.max_temperature)

        # Single Track settings
        self.singleTrackCenterSpinBox.setMinimum(1)
        self.singleTrackCenterSpinBox.setMaximum(self.camera.info.ypixels)
        self.singleTrackHeightSpinBox.setMinimum(1)
        self.singleTrackHeightSpinBox.setMaximum(self.camera.info.ypixels)

        # Timings
        self.exposureTimeSpinBox.setMinimum(10)

    def post_camera_disconnection(self):
        error = self.camera.last_error
        if error.is_success:
            logger.info(
                "Successfully disconnected Andor Camera - %i - %s",
                error.code,
                error.message,
            )
            self.update_ui()
        else:
            self.update_timer.start()
            self.pushbtnDisconnect.setEnabled(True)

    def set_target_temperature(self):
        new_target_temp = self.temperatureSpinBox.value()
        if new_target_temp == self.camera.target_temperature:
            return

        self.camera.SetTemperature(new_target_temp)
        andor_msg = self.camera.last_error.message
        logger.info("target temperature changed - %i - %s", new_target_temp, andor_msg)

    def set_exposure_time(self):
        new_exposure_time = self.exposureTimeSpinBox.value()
        if new_exposure_time == self.camera.target_exposure_time:
            return

        self.camera.SetExposureTime(new_exposure_time)
        andor_msg = self.camera.last_error.message
        logger.info("exposure time changed - %i ms - %s", new_exposure_time, andor_msg)

    def abort_acquisition(self):
        logger.warning("Abborting acquisition")
        self.current_acquisition.abort_acquisition()

    def set_readmode(self):
        new_readMode_index = self.readModeComboBox.currentIndex()
        new_readMode = self.readModeComboBox.currentText()
        if new_readMode_index == self.camera.read_mode:
            return

        self.camera.SetReadMode(new_readMode_index)
        andor_msg = self.camera.last_error.message
        logger.info("readMode changed to - %s - %s", new_readMode, andor_msg)

    def set_single_track(self):
        new_center = self.singleTrackCenterSpinBox.value()
        new_height = self.singleTrackHeightSpinBox.value()

        self.camera.SetSingleTrack(new_center, new_height)
        andor_msg = self.camera.last_error.message

        logger.info(
            "Single Track changed - center:%i, width:%i - %s",
            new_center,
            new_height,
            andor_msg,
        )

    def set_acquisition_mode(self):
        new_acquiMode_index = self.acquisitionModeComboBox.currentIndex()
        new_acquiMode = self.acquisitionModeComboBox.currentText()

        if new_acquiMode_index == self.camera.acquisition_mode - 1:
            return

        self.camera.SetAcquisitionMode(new_acquiMode_index + 1)
        andor_msg = self.camera.last_error.message
        logger.info("readMode changed to - %s - %s", new_acquiMode, andor_msg)

    def set_kinetic_number(self):
        new_kineticNumber = self.kineticNumberSpinBox.value()
        if new_kineticNumber == self.camera.number_kinetics:
            return

        self.camera.SetNumberKinetics(new_kineticNumber)
        andor_msg = self.camera.last_error.message
        logger.info("kinetic number changed - %i - %s", new_kineticNumber, andor_msg)

    def set_kinetic_cycle(self):
        new_kineticTime = self.kineticTimeSpinBox.value()
        if new_kineticTime == self.camera.info.kinetic_cycle:
            return

        self.camera.SetKineticCycleTime(new_kineticTime)
        andor_msg = self.camera.last_error.message
        logger.info("kinetic time changed - %i - %s", new_kineticTime, andor_msg)

    def acquisitionBtnClicked(self):

        self.current_acquisition = AndorAcquisition(self.camera)
        self.current_acquisition.signals.finished.connect(self.plot_acquisition_results)
        logger.info("Starting test acquisition")
        self.threadpool.start(self.current_acquisition)

    def plot_acquisition_results(self):

        logger.info("Test Acquisition completed - Plotting results")
        logger.info(tomli_w.dumps(asdict(self.current_acquisition.result)))

        # Create figure
        fig = plt.figure()

        result = self.current_acquisition.result
        data = result.data

        n, y, _ = data.shape

        for i in range(n):
            if y > 1:  # Image
                plt.subplot(n, 1, i + 1)
                plt.imshow(data[i, :, :])
            else:
                plt.plot(data[i, 0, :])

        plt.tight_layout()
        fig.show()
