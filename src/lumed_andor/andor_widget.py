import ast
import logging
from dataclasses import asdict
from pathlib import Path

import tomli_w
from PyQt5.QtCore import QThreadPool, QTimer
from PyQt5.QtWidgets import QFileDialog, QWidget

from lumed_andor.acquisition import AndorAcquisition
from lumed_andor.andor_control import AndorCamera
from lumed_andor.device_worker import DeviceWorker
from lumed_andor.fileio import export_setting, import_setting
from lumed_andor.plotting import AndorPlot
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
        self.last_image_plot: None | AndorPlot = None

        # ui configuration
        self.set_default_ui()
        self.connect_ui_signals()
        self.setup_update_timer()

        self.update_ui()
        logger.info("Widget initialization complete")

    # Default ui and setup

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
        self.comboBoxReadMode.addItems(
            [
                "Full Vertical Binning",
                "Multi-Track",
                "Random-Track",
                "Single-Track",
                "Image",
            ]
        )

        # acquisitionModes
        self.comboBoxAcquisitionMode.addItems(
            ["Single Scan", "Accumulate", "Kinetics", "Fast Kinetics", "Run till abort"]
        )

        # Disabling not implemented options
        self.comboBoxAcquisitionMode.model().item(1).setEnabled(False)
        self.comboBoxAcquisitionMode.model().item(3).setEnabled(False)
        self.comboBoxAcquisitionMode.model().item(4).setEnabled(False)

        # Misc
        self.checkBoxShowRegion.setCheckable(True)
        self.pushButtonReadModeOptimize.setEnabled(False)

    def connect_ui_signals(self):
        logger.info("Connecting Slots to UI signals")
        self.pushButtonConnect.clicked.connect(self.connectBtnClicked)
        self.pushButtonDisconnect.clicked.connect(self.disconnectBtnClicked)

        self.spinBoxTargetTemperature.valueChanged.connect(self.set_target_temperature)
        self.spinBoxTargetExposureTime.valueChanged.connect(self.set_exposure_time)

        ## Read Mode
        self.comboBoxReadMode.currentIndexChanged.connect(self.set_readmode)
        self.pushButtonReadModeDefault.clicked.connect(self.restore_readmode_default)
        self.checkBoxShowRegion.clicked.connect(self.update_readmode_region)

        # Multi Track
        self.spinBoxMultiTrackNumber.valueChanged.connect(self.set_multi_track)
        self.spinBoxMultiTrackHeight.valueChanged.connect(self.set_multi_track)
        self.spinBoxMultiTrackOffset.valueChanged.connect(self.set_multi_track)

        # Random Track
        # self.spinBoxRandomTrackHBinning.valueChanged.connect(self.)
        self.plainTextEditRandomTracks.textChanged.connect(self.set_random_track)

        # Single Track
        self.spinBoxsingleTrackCenter.valueChanged.connect(self.set_single_track)
        self.spinBoxsingleTrackHeight.valueChanged.connect(self.set_single_track)

        # Image
        self.spinBoxImageHBin.valueChanged.connect(self.set_image)
        self.spinBoxImageHStart.valueChanged.connect(self.set_image)
        self.spinBoxImageHEnd.valueChanged.connect(self.set_image)
        self.spinBoxImageVBin.valueChanged.connect(self.set_image)
        self.spinBoxImageVStart.valueChanged.connect(self.set_image)
        self.spinBoxImageVEnd.valueChanged.connect(self.set_image)

        ## Acquisition Mode
        self.comboBoxAcquisitionMode.currentIndexChanged.connect(
            self.set_acquisition_mode
        )
        self.spinBoxkineticNumber.valueChanged.connect(self.set_kinetic_number)
        self.spinBoxkineticTime.valueChanged.connect(self.set_kinetic_cycle)

        # Test acquisition
        self.pushButtonTestAcquisition.clicked.connect(self.acquisitionBtnClicked)
        self.pushButtonAbortAcquisition.clicked.connect(self.abort_acquisition)

        # Settings import export
        self.pushButtonImportSettings.clicked.connect(self.import_settings)
        self.pushButtonExportSettings.clicked.connect(self.export_settings)

    # Updates and timers

    def trigger_camera_update(self):
        worker = DeviceWorker(self.camera.get_info)
        self.threadpool.start(worker)

    def update_ui(self):

        # Enable/disable controls if camera is connected or not
        self.pushButtonConnect.setEnabled(not self.camera.is_connected)
        self.pushButtonDisconnect.setEnabled(self.camera.is_connected)
        self.groupBoxBasicControl.setEnabled(self.camera.is_connected)
        self.tabAdvancedControl.setEnabled(self.camera.is_connected)
        self.pushButtonTestAcquisition.setEnabled(
            not self.current_acquisition.in_progress
        )
        self.pushButtonAbortAcquisition.setEnabled(self.current_acquisition.in_progress)

        self.update_readmode_tab()

        # info txtbox
        info_str = tomli_w.dumps(asdict(self.camera.info))
        if self.plainTxtInfo.toPlainText() != info_str:
            self.plainTxtInfo.setPlainText(info_str)

        # current settings txtbox
        settings_str = tomli_w.dumps(asdict(self.camera.get_settings()))
        if self.plainTxtCurrentSettings.toPlainText() != settings_str:
            self.plainTxtCurrentSettings.setPlainText(settings_str)

        # General camera info
        self.labelCameraStatus.setText(self.camera.info.status.message)
        self.labelCurrentTemperature.setText(str(self.camera.info.temperature))
        self.labelCoolingStatus.setText(self.camera.info.cooling_status)
        self.spinBoxTargetExposureTime.setValue(int(self.camera.target_exposure_time))
        self.spinBoxTargetTemperature.setValue(int(self.camera.target_temperature))

        # Acquisition Mode Box
        if not self.comboBoxAcquisitionMode.hasFocus():
            self.comboBoxAcquisitionMode.setCurrentIndex(
                self.camera.acquisition_mode - 1
            )
        if not self.spinBoxkineticNumber.hasFocus():
            self.spinBoxkineticNumber.setValue(int(self.camera.number_kinetics))
        if not self.spinBoxkineticTime.hasFocus():
            self.spinBoxkineticTime.setValue(int(self.camera.target_kinetic_time))

    def update_readmode_tab(self):
        # Read Modes
        # 0 : FVB
        # 1 : Multi Track
        # 2 : Random Track
        # 3 : Single Track
        # 4 : Image
        read_mode = self.camera.read_mode

        if not self.comboBoxReadMode.hasFocus():
            self.comboBoxReadMode.setCurrentIndex(read_mode)

        # show/hide read mode controls

        if read_mode == 1:
            self.groupBoxMultiTrackSettings.show()
            self.groupBoxRandomTrackSettings.hide()
            self.groupBoxSingleTrackSettings.hide()
            self.groupBoxImageSettings.hide()
        elif read_mode == 2:
            self.groupBoxMultiTrackSettings.hide()
            self.groupBoxRandomTrackSettings.show()
            self.groupBoxSingleTrackSettings.hide()
            self.groupBoxImageSettings.hide()
        elif read_mode == 3:
            self.groupBoxMultiTrackSettings.hide()
            self.groupBoxRandomTrackSettings.hide()
            self.groupBoxSingleTrackSettings.show()
            self.groupBoxImageSettings.hide()
        elif read_mode == 4:
            self.groupBoxMultiTrackSettings.hide()
            self.groupBoxRandomTrackSettings.hide()
            self.groupBoxSingleTrackSettings.hide()
            self.groupBoxImageSettings.show()
        else:
            self.groupBoxMultiTrackSettings.hide()
            self.groupBoxRandomTrackSettings.hide()
            self.groupBoxSingleTrackSettings.hide()
            self.groupBoxImageSettings.hide()

        # Multi Track
        if not self.spinBoxMultiTrackNumber.hasFocus():
            self.spinBoxMultiTrackNumber.setValue(self.camera.multi_track.number)
        if not self.spinBoxMultiTrackHeight.hasFocus():
            self.spinBoxMultiTrackHeight.setValue(self.camera.multi_track.height)
        if not self.spinBoxMultiTrackOffset.hasFocus():
            self.spinBoxMultiTrackOffset.setValue(self.camera.multi_track.offset)

        # Random Track
        if not self.plainTextEditRandomTracks.hasFocus():
            new_tracks = self.camera.random_track.tracks
            if str(new_tracks) != self.plainTextEditRandomTracks.toPlainText():
                self.plainTextEditRandomTracks.setPlainText(str(new_tracks))

        # Single Track
        if not self.spinBoxsingleTrackCenter.hasFocus():
            self.spinBoxsingleTrackCenter.setValue(int(self.camera.single_track.center))
        if not self.spinBoxsingleTrackHeight.hasFocus():
            self.spinBoxsingleTrackHeight.setValue(int(self.camera.single_track.height))

        # Image
        image_config = self.camera.image_config

        if not self.spinBoxImageHBin.hasFocus():
            self.spinBoxImageHBin.setValue(image_config.hbin)
        if not self.spinBoxImageHStart.hasFocus():
            self.spinBoxImageHStart.setValue(image_config.hstart)
        if not self.spinBoxImageHEnd.hasFocus():
            self.spinBoxImageHEnd.setValue(image_config.hend)
        if not self.spinBoxImageVBin.hasFocus():
            self.spinBoxImageVBin.setValue(image_config.vbin)
        if not self.spinBoxImageVStart.hasFocus():
            self.spinBoxImageVStart.setValue(image_config.vstart)
        if not self.spinBoxImageVEnd.hasFocus():
            self.spinBoxImageVEnd.setValue(image_config.vend)

        # Buttons
        if read_mode == 0:
            self.pushButtonReadModeDefault.hide()
            self.checkBoxShowRegion.hide()
            self.pushButtonReadModeOptimize.hide()
        else:
            self.pushButtonReadModeDefault.show()
            self.checkBoxShowRegion.show()
            self.pushButtonReadModeOptimize.show()

    # Connect and disconnect

    def connectBtnClicked(self):
        logger.info("Connecting to Andor camera")
        self.pushButtonConnect.setEnabled(False)

        worker = DeviceWorker(self.camera.connect)
        worker.signals.finished.connect(self.post_camera_connection)
        self.threadpool.start(worker)

    def post_camera_connection(self):
        print("post connection")
        error = self.camera.last_error
        if error.is_success:
            logger.info(
                "Successfully connected to Andor Camera - %i - %s",
                error.code,
                error.message,
            )
            self.set_control_bounds()
            print("after control bounds")
            self.update_timer.start()
        self.update_ui()

    def set_control_bounds(self):
        # Temperature
        self.spinBoxTargetTemperature.setMinimum(self.camera.info.min_temperature)
        self.spinBoxTargetTemperature.setMaximum(self.camera.info.max_temperature)

        # Multi Track
        self.spinBoxMultiTrackNumber.setMaximum(self.camera.info.ypixels)
        self.spinBoxMultiTrackHeight.setMaximum(self.camera.info.ypixels)
        self.spinBoxMultiTrackOffset.setMaximum(self.camera.info.ypixels)
        self.spinBoxMultiTrackNumber.setMinimum(1)
        self.spinBoxMultiTrackHeight.setMinimum(1)
        self.spinBoxMultiTrackOffset.setMinimum(0)

        # Random Track

        # Single Track settings
        self.spinBoxsingleTrackCenter.setMaximum(self.camera.info.ypixels)
        self.spinBoxsingleTrackHeight.setMaximum(self.camera.info.ypixels)
        self.spinBoxsingleTrackCenter.setMinimum(1)
        self.spinBoxsingleTrackHeight.setMinimum(1)

        # Image
        self.spinBoxImageHBin.setMaximum(self.camera.info.xpixels)
        self.spinBoxImageHStart.setMaximum(self.camera.info.xpixels)
        self.spinBoxImageHEnd.setMaximum(self.camera.info.xpixels)
        self.spinBoxImageVBin.setMaximum(self.camera.info.ypixels)
        self.spinBoxImageVStart.setMaximum(self.camera.info.ypixels)
        self.spinBoxImageVEnd.setMaximum(self.camera.info.ypixels)
        self.spinBoxImageHBin.setMinimum(1)
        self.spinBoxImageHStart.setMinimum(1)
        self.spinBoxImageHEnd.setMinimum(1)
        self.spinBoxImageVBin.setMinimum(1)
        self.spinBoxImageVStart.setMinimum(1)
        self.spinBoxImageVEnd.setMinimum(1)

        # Timings
        self.spinBoxTargetExposureTime.setMinimum(10)

    def disconnectBtnClicked(self):
        logger.info("Disconnecting Andor camera")
        self.pushButtonDisconnect.setEnabled(False)
        self.update_timer.stop()

        worker = DeviceWorker(self.camera.disconnect)
        worker.signals.finished.connect(self.post_camera_disconnection)
        self.threadpool.start(worker)

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
            self.pushButtonDisconnect.setEnabled(True)

    # Camera control

    def set_target_temperature(self):
        new_target_temp = self.spinBoxTargetTemperature.value()
        if new_target_temp == self.camera.target_temperature:
            return

        self.camera.SetTemperature(new_target_temp)
        andor_msg = self.camera.last_error.message
        logger.info("target temperature changed - %i - %s", new_target_temp, andor_msg)

    def set_exposure_time(self):
        new_exposure_time = self.spinBoxTargetExposureTime.value()
        if new_exposure_time == self.camera.target_exposure_time:
            return

        self.camera.SetExposureTime(new_exposure_time)
        andor_msg = self.camera.last_error.message
        logger.info("exposure time changed - %i ms - %s", new_exposure_time, andor_msg)

    # Read mode control

    def set_readmode(self):
        new_readMode_index = self.comboBoxReadMode.currentIndex()
        new_readMode = self.comboBoxReadMode.currentText()
        if new_readMode_index == self.camera.read_mode:
            return

        self.camera.SetReadMode(new_readMode_index)
        andor_msg = self.camera.last_error.message
        logger.info("readMode changed to - %s - %s", new_readMode, andor_msg)

        self.update_readmode_region()

    def restore_readmode_default(self):

        # Multi Track
        self.spinBoxMultiTrackNumber.setValue(1)
        self.spinBoxMultiTrackOffset.setValue(0)
        self.spinBoxMultiTrackHeight.setValue(self.camera.info.ypixels)

        # Random Track
        self.plainTextEditRandomTracks.setPlainText(str([1, self.camera.info.ypixels]))

        # Single Track
        self.spinBoxsingleTrackCenter.setValue(self.camera.info.ypixels // 2)
        self.spinBoxsingleTrackHeight.setValue(self.camera.info.ypixels // 2)

        # Image
        self.spinBoxImageHBin.setValue(1)
        self.spinBoxImageVBin.setValue(1)
        self.spinBoxImageHStart.setValue(1)
        self.spinBoxImageVStart.setValue(1)
        self.spinBoxImageHEnd.setValue(self.camera.info.xpixels)
        self.spinBoxImageVEnd.setValue(self.camera.info.ypixels)

        self.update_readmode_region()

    def set_multi_track(self):
        new_number = self.spinBoxMultiTrackNumber.value()
        new_height = self.spinBoxMultiTrackHeight.value()
        new_offset = self.spinBoxMultiTrackOffset.value()

        self.camera.SetMultiTrack(new_number, new_height, new_offset)
        andor_msg = self.camera.last_error.message

        logger.info("Multi Track changed - %s - %s", self.camera.multi_track, andor_msg)

        self.update_readmode_region()

    def set_random_track(self):
        try:
            new_tracks = ast.literal_eval(self.plainTextEditRandomTracks.toPlainText())
            if not isinstance(new_tracks, list):
                return
            if len(new_tracks) % 2 > 0:
                return
        except:
            return

        numTracks = len(new_tracks) // 2
        self.camera.SetRandomTracks(numTracks=numTracks, areas=new_tracks)
        andor_msg = self.camera.last_error.message

        logger.info(
            "Random Track changed - %s - %s", self.camera.random_track, andor_msg
        )

        self.update_readmode_region()

    def set_single_track(self):
        new_center = self.spinBoxsingleTrackCenter.value()
        new_height = self.spinBoxsingleTrackHeight.value()

        self.camera.SetSingleTrack(new_center, new_height)
        andor_msg = self.camera.last_error.message

        logger.info(
            "Single Track changed - %s - %s",
            self.camera.single_track,
            andor_msg,
        )

        self.update_readmode_region()

    def set_image(self):
        hbin = self.spinBoxImageHBin.value()
        vbin = self.spinBoxImageVBin.value()
        hstart = self.spinBoxImageHStart.value()
        hend = self.spinBoxImageHEnd.value()
        vstart = self.spinBoxImageVStart.value()
        vend = self.spinBoxImageVEnd.value()

        self.camera.SetImage(hbin, vbin, hstart, hend, vstart, vend)
        andor_msg = self.camera.last_error.message
        logger.info(
            "Image changed - %s - %s",
            self.camera.image_config,
            andor_msg,
        )

        self.update_readmode_region()

    # Acquisition mode control

    def set_acquisition_mode(self):
        new_acquiMode_index = self.comboBoxAcquisitionMode.currentIndex()
        new_acquiMode = self.comboBoxAcquisitionMode.currentText()

        if new_acquiMode_index == self.camera.acquisition_mode - 1:
            return

        self.camera.SetAcquisitionMode(new_acquiMode_index + 1)
        andor_msg = self.camera.last_error.message
        logger.info("readMode changed to - %s - %s", new_acquiMode, andor_msg)

    def set_kinetic_number(self):
        new_kineticNumber = self.spinBoxkineticNumber.value()
        if new_kineticNumber == self.camera.number_kinetics:
            return

        self.camera.SetNumberKinetics(new_kineticNumber)
        andor_msg = self.camera.last_error.message
        logger.info("kinetic number changed - %i - %s", new_kineticNumber, andor_msg)

    def set_kinetic_cycle(self):
        new_kineticTime = self.spinBoxkineticTime.value()
        if new_kineticTime == self.camera.info.kinetic_cycle:
            return

        self.camera.SetKineticCycleTime(new_kineticTime)
        andor_msg = self.camera.last_error.message
        logger.info("kinetic time changed - %i - %s", new_kineticTime, andor_msg)

    # Test acquisition

    def acquisitionBtnClicked(self):

        self.current_acquisition = AndorAcquisition(self.camera)
        self.current_acquisition.signals.finished.connect(self.plot_acquisition_results)
        logger.info("Starting test acquisition")
        self.threadpool.start(self.current_acquisition)

    def abort_acquisition(self):
        logger.warning("Abborting acquisition")
        self.current_acquisition.abort_acquisition()

    def plot_acquisition_results(self):

        logger.info("Test Acquisition completed - Plotting results")
        logger.info(tomli_w.dumps(asdict(self.current_acquisition.result)))

        result = self.current_acquisition.result
        data = result.data

        andor_plot = AndorPlot(data)
        andor_plot.plot_data()

        if andor_plot.is_image_plot:
            self.last_image_plot = andor_plot

    def update_readmode_region(self):
        if not self.checkBoxShowRegion.isChecked():
            return

        if self.last_image_plot is None:
            return

        if self.camera.read_mode == 0:
            logger.info("Updating FVB region on last image plot")
            self.last_image_plot.plot_fvb_bounds()
        elif self.camera.read_mode == 1:
            logger.info("Updating Multi Track region on last image plot")
            self.last_image_plot.plot_multitrack_bounds(self.camera.multi_track)
        elif self.camera.read_mode == 2:
            logger.info("Updating Random Track region on last image plot")
            self.last_image_plot.plot_randomtrack_bounds(self.camera.random_track)
        elif self.camera.read_mode == 3:
            logger.info("Updating Single Track region on last image plot")
            self.last_image_plot.plot_singletrack_bounds(self.camera.single_track)

    # Camera settings

    def export_settings(self):
        logger.info("Getting file path for Andor setting export")
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            caption="Export Andor settings",
            directory=str(Path.home()),
            filter="TOML Files (*.toml);;All Files (*)",
        )

        if not filepath:
            logger.info("No filepath selected, aborting setting export")
            return

        filepath = Path(filepath).with_suffix(".toml")
        setting = self.camera.get_settings()

        logger.info("Exporting current camera settings - %s", setting)
        export_setting(setting=setting, filepath=filepath)

    def import_settings(self):
        logger.info("Getting file path for Andor setting import")
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            caption="Import Andor settings",
            directory=str(Path.home()),
            filter="TOML Files (*.toml);;All Files (*)",
        )

        if not filepath:
            logger.info("No filepath selected, aborting setting import")
            return

        filepath = Path(filepath).with_suffix(".toml")
        logger.info("Loading settings from file")
        setting = import_setting(filepath=filepath)

        logger.info("Applying settings to camera - %s", setting)
        self.camera.apply_settings(setting)
