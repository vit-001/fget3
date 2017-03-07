# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtWidgets import QWidget

from data_format.url import URL

from view.base_view import BaseView
from view.widgets.thumb_widget import ThumbWidgetVS


class ThumbView(BaseView):
    def get_main_content(self, parent:QWidget)->QWidget:
        self.thumbs=ThumbWidgetVS(parent)
        return self.thumbs

    def content_clear(self):
        self.thumbs.clear()

    def set_context(self,context):
        self.thumbs.context=context

    def set_title(self, title: str, tooltip=''):
        index=self.parent.indexOf(self.tab)
        self.parent.setTabText(index, title)
        self.parent.setTabToolTip(index, tooltip)

    def add_thumb(self, picture_filename: str, href: URL, popup: str = '', labels=list):
        self.thumbs.add(picture_filename, lambda :self.view_manager.goto_url(href), popup, labels)

    def history_event(self):
        history_data=dict()
        history_data['url']=self.url
        history_data['context']=self.thumbs.context
        # print('history event', history_data)
        self.history_handler(history_data)

if __name__ == "__main__":
    pass