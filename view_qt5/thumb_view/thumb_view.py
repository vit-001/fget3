# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from data_format.url import URL
from data_format.history_data import HistoryData

from view_qt5.base_view import BaseView
from view_qt5.widgets.thumb_widget import ThumbWidgetVS


class ThumbView(BaseView):
    def get_main_content(self, parent:QWidget)->QWidget:
        self.thumbs=ThumbWidgetVS(parent)
        return self.thumbs

    def prepare_content(self):
        self.thumbs.clear()
        if self.flags:
            self.thumbs.context=self.flags.get('context', None)
        self.progress.add_progress('thumbs',Qt.darkBlue)
        self.progress.set_autohide_bar_name('thumbs')

    def prepare_content_to_close(self):
        self.thumbs.clear()

    def set_url(self, url: URL):
        super().set_url(url)
        self.view_manager.on_thumb_tab_url_changed(self)

    def set_title(self, title: str, tooltip=''):
        index=self.parent.indexOf(self.tab)
        self.parent.setTabText(index, title)
        self.parent.setTabToolTip(index, tooltip)

    def add_thumb(self, picture_filename: str, href: URL, popup: str = '', labels=list):
        self.thumbs.add(picture_filename, lambda :self.view_manager.goto_url(href), popup, labels)
        self.progress.set_value('thumbs',self.thumbs.count)

    def history_event(self):
        history_data = HistoryData(self.url,self.thumbs.context)
        self.history_handler(history_data)

if __name__ == "__main__":
    pass