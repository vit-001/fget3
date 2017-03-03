# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtWidgets import QMainWindow

from common.url import URL

from view.qt_ui.thumb_widget import Ui_MainWindow
from view.widgets.thumb_widget import ThumbWidgetVS
from view.widgets.button_line import ButtonLine,TextButton,ImageButton


from controller.controller import ControllerFromViewInterface

class MainWindow(QMainWindow):
    def __init__(self, parent=None, controller: ControllerFromViewInterface=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller=controller
        self.resize(454, 779)
        print(self.geometry())
        self.create_widgets()

    def create_widgets(self):
        self.sites=ButtonLine(self.ui.top_frame)
        self.ui.top_frame_layout.addWidget(self.sites)

        b=TextButton('Ver','1',lambda: self.controller.goto_url(URL("https://www.veronicca.com/videos?o=mr*", test_string='Veronicca')))
        self.sites.add_button(b)
        b=TextButton('CBP','2',lambda: self.controller.goto_url(URL("http://collectionofbestporn.com/most-recent*", test_string='Collection')))
        self.sites.add_button(b)



    def closeEvent(self, *args, **kwargs):
        self.controller.on_exit()


if __name__ == "__main__":
    pass