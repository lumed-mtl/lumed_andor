# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/lumed_andor/ui/andor_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_andorCameraWidget(object):
    def setupUi(self, andorCameraWidget):
        andorCameraWidget.setObjectName("andorCameraWidget")
        andorCameraWidget.resize(935, 715)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(andorCameraWidget.sizePolicy().hasHeightForWidth())
        andorCameraWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(andorCameraWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widgetBasicControl = QtWidgets.QWidget(andorCameraWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetBasicControl.sizePolicy().hasHeightForWidth())
        self.widgetBasicControl.setSizePolicy(sizePolicy)
        self.widgetBasicControl.setObjectName("widgetBasicControl")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widgetBasicControl)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.pushButtonConnect = QtWidgets.QPushButton(self.widgetBasicControl)
        self.pushButtonConnect.setObjectName("pushButtonConnect")
        self.gridLayout_7.addWidget(self.pushButtonConnect, 0, 0, 1, 1)
        self.pushButtonDisconnect = QtWidgets.QPushButton(self.widgetBasicControl)
        self.pushButtonDisconnect.setObjectName("pushButtonDisconnect")
        self.gridLayout_7.addWidget(self.pushButtonDisconnect, 0, 1, 1, 1)
        self.labelCameraStatus = QtWidgets.QLabel(self.widgetBasicControl)
        self.labelCameraStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.labelCameraStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCameraStatus.setObjectName("labelCameraStatus")
        self.gridLayout_7.addWidget(self.labelCameraStatus, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widgetBasicControl)
        self.label.setObjectName("label")
        self.gridLayout_7.addWidget(self.label, 1, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_7)
        self.groupBoxBasicControl = QtWidgets.QGroupBox(self.widgetBasicControl)
        self.groupBoxBasicControl.setTitle("")
        self.groupBoxBasicControl.setObjectName("groupBoxBasicControl")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBoxBasicControl)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tempControlLayout = QtWidgets.QGroupBox(self.groupBoxBasicControl)
        self.tempControlLayout.setObjectName("tempControlLayout")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tempControlLayout)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_6 = QtWidgets.QLabel(self.tempControlLayout)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)
        self.spinBoxTargetTemperature = QtWidgets.QSpinBox(self.tempControlLayout)
        self.spinBoxTargetTemperature.setMinimum(-100)
        self.spinBoxTargetTemperature.setMaximum(30)
        self.spinBoxTargetTemperature.setObjectName("spinBoxTargetTemperature")
        self.gridLayout_6.addWidget(self.spinBoxTargetTemperature, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tempControlLayout)
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 1, 0, 1, 1)
        self.labelCurrentTemperature = QtWidgets.QLabel(self.tempControlLayout)
        self.labelCurrentTemperature.setMinimumSize(QtCore.QSize(75, 0))
        self.labelCurrentTemperature.setAcceptDrops(False)
        self.labelCurrentTemperature.setAutoFillBackground(True)
        self.labelCurrentTemperature.setFrameShape(QtWidgets.QFrame.Box)
        self.labelCurrentTemperature.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCurrentTemperature.setObjectName("labelCurrentTemperature")
        self.gridLayout_6.addWidget(self.labelCurrentTemperature, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tempControlLayout)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 2, 0, 1, 1)
        self.labelCoolingStatus = QtWidgets.QLabel(self.tempControlLayout)
        self.labelCoolingStatus.setMinimumSize(QtCore.QSize(75, 0))
        self.labelCoolingStatus.setAutoFillBackground(True)
        self.labelCoolingStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.labelCoolingStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCoolingStatus.setObjectName("labelCoolingStatus")
        self.gridLayout_6.addWidget(self.labelCoolingStatus, 2, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.tempControlLayout)
        self.exposureTestLayout = QtWidgets.QHBoxLayout()
        self.exposureTestLayout.setObjectName("exposureTestLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBoxBasicControl)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.spinBoxTargetExposureTime = QtWidgets.QSpinBox(self.groupBoxBasicControl)
        self.spinBoxTargetExposureTime.setMinimumSize(QtCore.QSize(150, 30))
        self.spinBoxTargetExposureTime.setMaximum(65536)
        self.spinBoxTargetExposureTime.setObjectName("spinBoxTargetExposureTime")
        self.horizontalLayout_4.addWidget(self.spinBoxTargetExposureTime)
        self.exposureTestLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addLayout(self.exposureTestLayout)
        self.testAcquisitionLayout = QtWidgets.QHBoxLayout()
        self.testAcquisitionLayout.setObjectName("testAcquisitionLayout")
        self.pushButtonTestAcquisition = QtWidgets.QPushButton(self.groupBoxBasicControl)
        self.pushButtonTestAcquisition.setObjectName("pushButtonTestAcquisition")
        self.testAcquisitionLayout.addWidget(self.pushButtonTestAcquisition)
        self.pushButtonAbortAcquisition = QtWidgets.QPushButton(self.groupBoxBasicControl)
        self.pushButtonAbortAcquisition.setObjectName("pushButtonAbortAcquisition")
        self.testAcquisitionLayout.addWidget(self.pushButtonAbortAcquisition)
        self.testAcquisitionLayout.setStretch(0, 5)
        self.testAcquisitionLayout.setStretch(1, 1)
        self.verticalLayout_4.addLayout(self.testAcquisitionLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.settingsIOGroupBox = QtWidgets.QGroupBox(self.groupBoxBasicControl)
        self.settingsIOGroupBox.setObjectName("settingsIOGroupBox")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.settingsIOGroupBox)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButtonImportSettings = QtWidgets.QPushButton(self.settingsIOGroupBox)
        self.pushButtonImportSettings.setObjectName("pushButtonImportSettings")
        self.horizontalLayout_11.addWidget(self.pushButtonImportSettings)
        self.pushButtonExportSettings = QtWidgets.QPushButton(self.settingsIOGroupBox)
        self.pushButtonExportSettings.setObjectName("pushButtonExportSettings")
        self.horizontalLayout_11.addWidget(self.pushButtonExportSettings)
        self.verticalLayout_4.addWidget(self.settingsIOGroupBox)
        self.verticalLayout_6.addWidget(self.groupBoxBasicControl)
        self.horizontalLayout_3.addWidget(self.widgetBasicControl)
        self.tabAdvancedControl = QtWidgets.QTabWidget(andorCameraWidget)
        self.tabAdvancedControl.setUsesScrollButtons(False)
        self.tabAdvancedControl.setObjectName("tabAdvancedControl")
        self.tabReadMode = QtWidgets.QWidget()
        self.tabReadMode.setObjectName("tabReadMode")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabReadMode)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.tabReadMode)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.comboBoxReadMode = QtWidgets.QComboBox(self.tabReadMode)
        self.comboBoxReadMode.setObjectName("comboBoxReadMode")
        self.horizontalLayout_5.addWidget(self.comboBoxReadMode)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.groupBoxSingleTrackSettings = QtWidgets.QGroupBox(self.tabReadMode)
        self.groupBoxSingleTrackSettings.setObjectName("groupBoxSingleTrackSettings")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxSingleTrackSettings)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.spinBoxsingleTrackCenter = QtWidgets.QSpinBox(self.groupBoxSingleTrackSettings)
        self.spinBoxsingleTrackCenter.setMinimum(1)
        self.spinBoxsingleTrackCenter.setMaximum(255)
        self.spinBoxsingleTrackCenter.setObjectName("spinBoxsingleTrackCenter")
        self.gridLayout_4.addWidget(self.spinBoxsingleTrackCenter, 0, 1, 1, 1)
        self.spinBoxsingleTrackHeight = QtWidgets.QSpinBox(self.groupBoxSingleTrackSettings)
        self.spinBoxsingleTrackHeight.setMinimum(1)
        self.spinBoxsingleTrackHeight.setMaximum(255)
        self.spinBoxsingleTrackHeight.setObjectName("spinBoxsingleTrackHeight")
        self.gridLayout_4.addWidget(self.spinBoxsingleTrackHeight, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBoxSingleTrackSettings)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBoxSingleTrackSettings)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxSingleTrackSettings)
        self.groupBoxMultiTrackSettings = QtWidgets.QGroupBox(self.tabReadMode)
        self.groupBoxMultiTrackSettings.setObjectName("groupBoxMultiTrackSettings")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxMultiTrackSettings)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_12 = QtWidgets.QLabel(self.groupBoxMultiTrackSettings)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1)
        self.spinBoxMultiTrackOffset = QtWidgets.QSpinBox(self.groupBoxMultiTrackSettings)
        self.spinBoxMultiTrackOffset.setObjectName("spinBoxMultiTrackOffset")
        self.gridLayout_3.addWidget(self.spinBoxMultiTrackOffset, 2, 1, 1, 1)
        self.spinBoxMultiTrackNumber = QtWidgets.QSpinBox(self.groupBoxMultiTrackSettings)
        self.spinBoxMultiTrackNumber.setObjectName("spinBoxMultiTrackNumber")
        self.gridLayout_3.addWidget(self.spinBoxMultiTrackNumber, 0, 1, 1, 1)
        self.spinBoxMultiTrackHeight = QtWidgets.QSpinBox(self.groupBoxMultiTrackSettings)
        self.spinBoxMultiTrackHeight.setObjectName("spinBoxMultiTrackHeight")
        self.gridLayout_3.addWidget(self.spinBoxMultiTrackHeight, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBoxMultiTrackSettings)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBoxMultiTrackSettings)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxMultiTrackSettings)
        self.groupBoxRandomTrackSettings = QtWidgets.QGroupBox(self.tabReadMode)
        self.groupBoxRandomTrackSettings.setObjectName("groupBoxRandomTrackSettings")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxRandomTrackSettings)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_16 = QtWidgets.QLabel(self.groupBoxRandomTrackSettings)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 1, 0, 1, 1)
        self.plainTextEditRandomTracks = QtWidgets.QPlainTextEdit(self.groupBoxRandomTrackSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEditRandomTracks.sizePolicy().hasHeightForWidth())
        self.plainTextEditRandomTracks.setSizePolicy(sizePolicy)
        self.plainTextEditRandomTracks.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEditRandomTracks.setObjectName("plainTextEditRandomTracks")
        self.gridLayout_2.addWidget(self.plainTextEditRandomTracks, 1, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBoxRandomTrackSettings)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)
        self.spinBoxRandomTrackHBinning = QtWidgets.QSpinBox(self.groupBoxRandomTrackSettings)
        self.spinBoxRandomTrackHBinning.setObjectName("spinBoxRandomTrackHBinning")
        self.gridLayout_2.addWidget(self.spinBoxRandomTrackHBinning, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxRandomTrackSettings)
        self.groupBoxImageSettings = QtWidgets.QGroupBox(self.tabReadMode)
        self.groupBoxImageSettings.setObjectName("groupBoxImageSettings")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxImageSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.label_19 = QtWidgets.QLabel(self.groupBoxImageSettings)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 2, 2, 1, 1)
        self.spinBoxImageHEnd = QtWidgets.QSpinBox(self.groupBoxImageSettings)
        self.spinBoxImageHEnd.setObjectName("spinBoxImageHEnd")
        self.gridLayout.addWidget(self.spinBoxImageHEnd, 3, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBoxImageSettings)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 2, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBoxImageSettings)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 1, 0, 1, 1)
        self.spinBoxImageHBin = QtWidgets.QSpinBox(self.groupBoxImageSettings)
        self.spinBoxImageHBin.setObjectName("spinBoxImageHBin")
        self.gridLayout.addWidget(self.spinBoxImageHBin, 1, 1, 1, 1)
        self.spinBoxImageVStart = QtWidgets.QSpinBox(self.groupBoxImageSettings)
        self.spinBoxImageVStart.setObjectName("spinBoxImageVStart")
        self.gridLayout.addWidget(self.spinBoxImageVStart, 2, 3, 1, 1)
        self.spinBoxImageVEnd = QtWidgets.QSpinBox(self.groupBoxImageSettings)
        self.spinBoxImageVEnd.setObjectName("spinBoxImageVEnd")
        self.gridLayout.addWidget(self.spinBoxImageVEnd, 3, 3, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBoxImageSettings)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 3, 2, 1, 1)
        self.spinBoxImageVBin = QtWidgets.QSpinBox(self.groupBoxImageSettings)
        self.spinBoxImageVBin.setObjectName("spinBoxImageVBin")
        self.gridLayout.addWidget(self.spinBoxImageVBin, 1, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBoxImageSettings)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 1, 2, 1, 1)
        self.spinBoxImageHStart = QtWidgets.QSpinBox(self.groupBoxImageSettings)
        self.spinBoxImageHStart.setObjectName("spinBoxImageHStart")
        self.gridLayout.addWidget(self.spinBoxImageHStart, 2, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBoxImageSettings)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 3, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxImageSettings)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBoxShowRegion = QtWidgets.QCheckBox(self.tabReadMode)
        self.checkBoxShowRegion.setObjectName("checkBoxShowRegion")
        self.horizontalLayout_6.addWidget(self.checkBoxShowRegion)
        self.pushButtonReadModeDefault = QtWidgets.QPushButton(self.tabReadMode)
        self.pushButtonReadModeDefault.setObjectName("pushButtonReadModeDefault")
        self.horizontalLayout_6.addWidget(self.pushButtonReadModeDefault)
        self.pushButtonReadModeOptimize = QtWidgets.QPushButton(self.tabReadMode)
        self.pushButtonReadModeOptimize.setObjectName("pushButtonReadModeOptimize")
        self.horizontalLayout_6.addWidget(self.pushButtonReadModeOptimize)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.tabAdvancedControl.addTab(self.tabReadMode, "")
        self.tabAcquisitionMode = QtWidgets.QWidget()
        self.tabAcquisitionMode.setObjectName("tabAcquisitionMode")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabAcquisitionMode)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_9 = QtWidgets.QLabel(self.tabAcquisitionMode)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.comboBoxAcquisitionMode = QtWidgets.QComboBox(self.tabAcquisitionMode)
        self.comboBoxAcquisitionMode.setObjectName("comboBoxAcquisitionMode")
        self.horizontalLayout.addWidget(self.comboBoxAcquisitionMode)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tabAcquisitionMode)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_10 = QtWidgets.QLabel(self.groupBox_6)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)
        self.spinBoxkineticNumber = QtWidgets.QSpinBox(self.groupBox_6)
        self.spinBoxkineticNumber.setMinimum(1)
        self.spinBoxkineticNumber.setMaximum(65536)
        self.spinBoxkineticNumber.setObjectName("spinBoxkineticNumber")
        self.gridLayout_5.addWidget(self.spinBoxkineticNumber, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_6)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 1, 0, 1, 1)
        self.spinBoxkineticTime = QtWidgets.QSpinBox(self.groupBox_6)
        self.spinBoxkineticTime.setMaximum(65536)
        self.spinBoxkineticTime.setObjectName("spinBoxkineticTime")
        self.gridLayout_5.addWidget(self.spinBoxkineticTime, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.tabAdvancedControl.addTab(self.tabAcquisitionMode, "")
        self.tabInfo = QtWidgets.QWidget()
        self.tabInfo.setObjectName("tabInfo")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tabInfo)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plainTxtInfo = QtWidgets.QPlainTextEdit(self.tabInfo)
        self.plainTxtInfo.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.plainTxtInfo.setObjectName("plainTxtInfo")
        self.horizontalLayout_2.addWidget(self.plainTxtInfo)
        self.tabAdvancedControl.addTab(self.tabInfo, "")
        self.tabCurrentSettings = QtWidgets.QWidget()
        self.tabCurrentSettings.setObjectName("tabCurrentSettings")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.tabCurrentSettings)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.plainTxtCurrentSettings = QtWidgets.QPlainTextEdit(self.tabCurrentSettings)
        self.plainTxtCurrentSettings.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.plainTxtCurrentSettings.setObjectName("plainTxtCurrentSettings")
        self.horizontalLayout_14.addWidget(self.plainTxtCurrentSettings)
        self.tabAdvancedControl.addTab(self.tabCurrentSettings, "")
        self.horizontalLayout_3.addWidget(self.tabAdvancedControl)

        self.retranslateUi(andorCameraWidget)
        self.tabAdvancedControl.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(andorCameraWidget)

    def retranslateUi(self, andorCameraWidget):
        _translate = QtCore.QCoreApplication.translate
        andorCameraWidget.setWindowTitle(_translate("andorCameraWidget", "andorCameraWidget"))
        self.pushButtonConnect.setText(_translate("andorCameraWidget", "Connect"))
        self.pushButtonDisconnect.setText(_translate("andorCameraWidget", "Disconnect"))
        self.labelCameraStatus.setText(_translate("andorCameraWidget", "Not Connected"))
        self.label.setText(_translate("andorCameraWidget", "Camera Status :"))
        self.tempControlLayout.setTitle(_translate("andorCameraWidget", "Temperature Control"))
        self.label_6.setText(_translate("andorCameraWidget", "Target Temperature [C]:"))
        self.label_7.setText(_translate("andorCameraWidget", "Current Temperature [C] :"))
        self.labelCurrentTemperature.setText(_translate("andorCameraWidget", "NA"))
        self.label_8.setText(_translate("andorCameraWidget", "Status :"))
        self.labelCoolingStatus.setText(_translate("andorCameraWidget", "NA"))
        self.label_2.setText(_translate("andorCameraWidget", "Exposure Time [ms]"))
        self.pushButtonTestAcquisition.setText(_translate("andorCameraWidget", "Test Acquisition"))
        self.pushButtonAbortAcquisition.setText(_translate("andorCameraWidget", "Abort"))
        self.settingsIOGroupBox.setTitle(_translate("andorCameraWidget", "Settings"))
        self.pushButtonImportSettings.setText(_translate("andorCameraWidget", "Import"))
        self.pushButtonExportSettings.setText(_translate("andorCameraWidget", "Export"))
        self.label_3.setText(_translate("andorCameraWidget", "Read Mode :"))
        self.groupBoxSingleTrackSettings.setTitle(_translate("andorCameraWidget", "Single Track Setting"))
        self.label_5.setText(_translate("andorCameraWidget", "Height"))
        self.label_4.setText(_translate("andorCameraWidget", "Center"))
        self.groupBoxMultiTrackSettings.setTitle(_translate("andorCameraWidget", "Multi Track Settings"))
        self.label_12.setText(_translate("andorCameraWidget", "Number"))
        self.label_13.setText(_translate("andorCameraWidget", "Height"))
        self.label_14.setText(_translate("andorCameraWidget", "Offset"))
        self.groupBoxRandomTrackSettings.setTitle(_translate("andorCameraWidget", "Random Track Settings"))
        self.label_16.setText(_translate("andorCameraWidget", "Random Tracks"))
        self.plainTextEditRandomTracks.setPlainText(_translate("andorCameraWidget", "[]"))
        self.label_15.setText(_translate("andorCameraWidget", "Horizontal Binning"))
        self.groupBoxImageSettings.setTitle(_translate("andorCameraWidget", "Image Settings"))
        self.label_19.setText(_translate("andorCameraWidget", "Vertical Start"))
        self.label_20.setText(_translate("andorCameraWidget", "Horizontal Start"))
        self.label_17.setText(_translate("andorCameraWidget", "Horizontal Binning"))
        self.label_22.setText(_translate("andorCameraWidget", "Vertical End"))
        self.label_18.setText(_translate("andorCameraWidget", "Vertical Binning"))
        self.label_21.setText(_translate("andorCameraWidget", "Horizontal End"))
        self.checkBoxShowRegion.setText(_translate("andorCameraWidget", "Show Region"))
        self.pushButtonReadModeDefault.setText(_translate("andorCameraWidget", "Restore Default"))
        self.pushButtonReadModeOptimize.setText(_translate("andorCameraWidget", "Optimize"))
        self.tabAdvancedControl.setTabText(self.tabAdvancedControl.indexOf(self.tabReadMode), _translate("andorCameraWidget", "Read Mode"))
        self.label_9.setText(_translate("andorCameraWidget", "Acquisition Mode"))
        self.groupBox_6.setTitle(_translate("andorCameraWidget", "Kinetic Setting"))
        self.label_10.setText(_translate("andorCameraWidget", "Number"))
        self.label_11.setText(_translate("andorCameraWidget", "Cycle Time [ms]"))
        self.tabAdvancedControl.setTabText(self.tabAdvancedControl.indexOf(self.tabAcquisitionMode), _translate("andorCameraWidget", "Acquisition Mode"))
        self.tabAdvancedControl.setTabText(self.tabAdvancedControl.indexOf(self.tabInfo), _translate("andorCameraWidget", "Info"))
        self.tabAdvancedControl.setTabText(self.tabAdvancedControl.indexOf(self.tabCurrentSettings), _translate("andorCameraWidget", "Current Settings"))
