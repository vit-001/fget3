# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/repo/fget3/view/qt_design/video_player_widget.ui'
#
# Created: Thu Mar 23 18:43:06 2017
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VideoPlayerWidget(object):
    def setupUi(self, VideoPlayerWidget):
        VideoPlayerWidget.setObjectName("VideoPlayerWidget")
        VideoPlayerWidget.resize(686, 527)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(150, 150, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(150, 150, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(150, 150, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(150, 150, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        VideoPlayerWidget.setPalette(palette)
        VideoPlayerWidget.setStyleSheet("#Form {\n"
"                background: white;\n"
"                }\n"
"\n"
"                QProgressBar {\n"
"                border: 1px solid black;\n"
"                text-align: top;\n"
"                padding: 1px;\n"
"                border-bottom-right-radius: 7px;\n"
"                border-bottom-left-radius: 7px;\n"
"                background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fff, stop: 0.4999 #eee, stop: 0.5\n"
"                #ddd, stop: 1 #eee );\n"
"                width: 15px;\n"
"                }\n"
"\n"
"                QProgressBar::chunk {\n"
"                background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #78d, stop: 0.4999 #46a, stop:\n"
"                0.5 #45a, stop: 1 #238 );\n"
"                border-bottom-right-radius: 7px;\n"
"                border-bottom-left-radius: 7px;\n"
"                border: 1px solid black;\n"
"                }\n"
"            ")
        self.main_layout = QtWidgets.QVBoxLayout(VideoPlayerWidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        self.top_frame = QtWidgets.QFrame(VideoPlayerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_frame.sizePolicy().hasHeightForWidth())
        self.top_frame.setSizePolicy(sizePolicy)
        self.top_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame.setObjectName("top_frame")
        self.top_frame_layout = QtWidgets.QVBoxLayout(self.top_frame)
        self.top_frame_layout.setSpacing(0)
        self.top_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.top_frame_layout.setObjectName("top_frame_layout")
        self.main_layout.addWidget(self.top_frame)
        self.bottom_frame = QtWidgets.QFrame(VideoPlayerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_frame.sizePolicy().hasHeightForWidth())
        self.bottom_frame.setSizePolicy(sizePolicy)
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom_frame.setObjectName("bottom_frame")
        self.bottom_frame_layout = QtWidgets.QHBoxLayout(self.bottom_frame)
        self.bottom_frame_layout.setSpacing(0)
        self.bottom_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_frame_layout.setObjectName("bottom_frame_layout")
        self.bn_play = QtWidgets.QToolButton(self.bottom_frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resource/icons/ic_play_arrow_black_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_play.setIcon(icon)
        self.bn_play.setIconSize(QtCore.QSize(32, 32))
        self.bn_play.setAutoRaise(True)
        self.bn_play.setObjectName("bn_play")
        self.bottom_frame_layout.addWidget(self.bn_play)
        self.bn_pause = QtWidgets.QToolButton(self.bottom_frame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../resource/icons/ic_pause_black_24dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_pause.setIcon(icon1)
        self.bn_pause.setIconSize(QtCore.QSize(32, 32))
        self.bn_pause.setAutoRaise(True)
        self.bn_pause.setObjectName("bn_pause")
        self.bottom_frame_layout.addWidget(self.bn_pause)
        self.bn_stop = QtWidgets.QToolButton(self.bottom_frame)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../resource/icons/ic_stop_black_24dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_stop.setIcon(icon2)
        self.bn_stop.setIconSize(QtCore.QSize(32, 32))
        self.bn_stop.setAutoRaise(True)
        self.bn_stop.setObjectName("bn_stop")
        self.bottom_frame_layout.addWidget(self.bn_stop)
        self.bn_mute = QtWidgets.QToolButton(self.bottom_frame)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../resource/icons/ic_volume_up_black_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap("../resource/icons/ic_volume_off_black_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bn_mute.setIcon(icon3)
        self.bn_mute.setIconSize(QtCore.QSize(32, 32))
        self.bn_mute.setCheckable(True)
        self.bn_mute.setChecked(True)
        self.bn_mute.setAutoRaise(True)
        self.bn_mute.setObjectName("bn_mute")
        self.bottom_frame_layout.addWidget(self.bn_mute)
        self.bn_quality = QtWidgets.QToolButton(self.bottom_frame)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../resource/icons/ic_high_quality_black_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_quality.setIcon(icon4)
        self.bn_quality.setIconSize(QtCore.QSize(32, 32))
        self.bn_quality.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.bn_quality.setAutoRaise(True)
        self.bn_quality.setArrowType(QtCore.Qt.NoArrow)
        self.bn_quality.setObjectName("bn_quality")
        self.bottom_frame_layout.addWidget(self.bn_quality)
        self.progress = QtWidgets.QSlider(self.bottom_frame)
        self.progress.setOrientation(QtCore.Qt.Horizontal)
        self.progress.setObjectName("progress")
        self.bottom_frame_layout.addWidget(self.progress)
        self.lb_time = QtWidgets.QLabel(self.bottom_frame)
        self.lb_time.setTextFormat(QtCore.Qt.AutoText)
        self.lb_time.setContentsMargins(2, 2, 2, 2)
        self.lb_time.setObjectName("lb_time")
        self.bottom_frame_layout.addWidget(self.lb_time)
        self.volume = QtWidgets.QDial(self.bottom_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume.sizePolicy().hasHeightForWidth())
        self.volume.setSizePolicy(sizePolicy)
        self.volume.setMinimumSize(QtCore.QSize(48, 48))
        self.volume.setMaximumSize(QtCore.QSize(48, 48))
        self.volume.setMaximum(100)
        self.volume.setSingleStep(5)
        self.volume.setPageStep(5)
        self.volume.setOrientation(QtCore.Qt.Horizontal)
        self.volume.setObjectName("volume")
        self.bottom_frame_layout.addWidget(self.volume)
        self.buffer = QtWidgets.QProgressBar(self.bottom_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buffer.sizePolicy().hasHeightForWidth())
        self.buffer.setSizePolicy(sizePolicy)
        self.buffer.setMaximumSize(QtCore.QSize(48, 48))
        self.buffer.setProperty("value", 24)
        self.buffer.setTextVisible(False)
        self.buffer.setOrientation(QtCore.Qt.Vertical)
        self.buffer.setObjectName("buffer")
        self.bottom_frame_layout.addWidget(self.buffer)
        self.main_layout.addWidget(self.bottom_frame)

        self.retranslateUi(VideoPlayerWidget)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayerWidget)

    def retranslateUi(self, VideoPlayerWidget):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayerWidget.setWindowTitle(_translate("VideoPlayerWidget", "Form"))
        self.bn_play.setText(_translate("VideoPlayerWidget", "..."))
        self.bn_pause.setText(_translate("VideoPlayerWidget", "..."))
        self.bn_stop.setText(_translate("VideoPlayerWidget", "..."))
        self.bn_mute.setText(_translate("VideoPlayerWidget", "..."))
        self.bn_quality.setText(_translate("VideoPlayerWidget", "HQ"))
        self.lb_time.setText(_translate("VideoPlayerWidget", "0:00"))

