# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5 import QtCore, QtGui, QtWidgets

from common.url import URL
from view.base_view import ThumbViewFromModelInterface

from view.widgets.thumb_widget import ThumbWidgetVS

class ThumbView(ThumbViewFromModelInterface):
    def __init__(self,parent_tab:QtWidgets.QWidget, name:str):

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        parent_tab.addTab(self.tab, name)

        self.widget=ThumbWidgetVS(parent_tab)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.widget)

        self.widget.show()


    def add_thumb(self, picture_filename: str, href: URL, popup: str = '', labels=list):
        # print('Thumb filename:', picture_filename, 'added')
        # print('           url:', href)
        # print('         popup:', popup)
        # print('        labels:', labels)
        self.widget.add(picture_filename,lambda :None, popup,labels)



if __name__ == "__main__":
    pass