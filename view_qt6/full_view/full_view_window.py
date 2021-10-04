# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon, QPixmap

from interface.view_interface import ViewFromModelInterface
from interface.view_manager_interface import ViewManagerFromViewInterface

from view_qt6.full_view.full_view import FullView
from view_qt6.qt_ui.ui_full_view_window import Ui_FullViewWindow


class FullViewWindow(QWidget):
    def __init__(self, view_manager: ViewManagerFromViewInterface=None):
        QWidget.__init__(self, None)
        self.view_manager=view_manager
        # create interface
        self.ui = Ui_FullViewWindow()
        self.ui.setupUi(self)

        self.create_widgets()

        pixmap = QPixmap('view_qt5/resource/icons_my/icon.png')
        icon = QIcon()
        icon.addPixmap(pixmap, QIcon.Mode.Normal, QIcon.State.Off)

        self.setWindowTitle('P Browser - thumbnail view_qt5')
        self.setWindowIcon(icon)


        # define variables
        self.full_views=list()
        self.global_muted=True
        self.global_volume=10

        #all  binding
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.currentChanged.connect(self.change_tab)
        self.ui.tabWidget.tabBarClicked.connect(self.click_tab)

        self.view_manager.add_keyboard_shortcut(self, 'Space', lambda: self.little_forvard(30))
        self.view_manager.add_keyboard_shortcut(self, 'Ctrl+Space', lambda: self.little_forvard(180))

        self.set_visible()

    def create_widgets(self):
        pass

    def set_visible(self):
        self.setVisible(bool(self.full_views))

    def get_new_full_view(self) -> FullView:
        view = FullView(self.ui.tabWidget,self.view_manager)
        self.full_views.append(view)
        view.mute(self.global_muted)
        view.set_volume(self.global_volume)
        self.set_visible()
        return view

    def get_current_full_view(self)->FullView:
        index = self.ui.tabWidget.currentIndex()
        if index >= 0:
            return self.full_views[index]
        else:
            return None

    def set_tab_text(self, view,text:str, tooltip:str=''):
        try:
            index=self.full_views.index(view)
            self.ui.tabWidget.setTabText(index,text)
            self.ui.tabWidget.setTabToolTip(index,tooltip)
        except ValueError:
            pass

    def close_tab(self,index:int):
        view=self.full_views[index]
        view.prepare_to_close()
        if index == self.ui.tabWidget.currentIndex(): #Close active tab
            self.global_muted=view.is_muted()
            self.global_volume=view.get_volume()
        view.destroy()

        self.full_views.pop(index)
        self.ui.tabWidget.removeTab(index)
        self.update()
        self.set_visible()

    def change_tab(self,index:int):
        self.do_method_with_all_tab('pause')
        self.do_method_with_current_tab('play', muted=self.global_muted, volume=self.global_volume)

    def click_tab(self, index):
        self.global_muted = self.full_views[self.ui.tabWidget.currentIndex()].is_muted()
        self.global_volume= self.full_views[self.ui.tabWidget.currentIndex()].get_volume()

    def is_tab_active(self,full_view: ViewFromModelInterface):
        index=self.full_views.index(full_view)
        return index == self.ui.tabWidget.currentIndex()

    def little_forvard(self, seconds=30):
        self.do_method_with_current_tab('little_forward', seconds)

    def panic(self):
        self.global_muted=True
        self.do_method_with_all_tab('mute',True)
        self.do_method_with_current_tab('pause')
        self.showMinimized()

    def on_exit(self):
        for view in self.full_views:
            view.destroy()

    def do_method_with_all_tab(self, method_name:str, *args, **options):
        for view in self.full_views:
            view.__getattribute__(method_name)(*args,**options)

    def do_method_with_current_tab(self, method_name:str, *args, **options):
        current_tab_index=self.ui.tabWidget.currentIndex()
        if current_tab_index>=0 and len(self.full_views)>0:
            self.full_views[current_tab_index].__getattribute__(method_name)(*args,**options)

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        for view in self.full_views:
            view.resize_event()

if __name__ == "__main__":
    pass