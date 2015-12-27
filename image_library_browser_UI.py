import PySide.QtCore as qc
import PySide.QtGui as qg

import os
# import functools

# Global variable to store the UI status, if it's open or closed
image_library_browser_ui = None


class FlowLayout(qg.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setMargin(margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return qc.Qt.Orientations(qc.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(qc.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = qc.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        # size += qc.QSize(2 * self.margin(), 2 * self.margin())
        return size

    def enterEvent(self, *args, **kwargs):
        """

        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        print("......Entered the Fucking browser.......")

    def mouseDoubleClickEvent(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        print(args)

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(qg.QSizePolicy.PushButton, qg.QSizePolicy.PushButton, qc.Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(qg.QSizePolicy.PushButton, qg.QSizePolicy.PushButton, qc.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(qc.QRect(qc.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


class CustomWidget(qg.QWidget):
    mouse_entered = qc.Signal(qg.QWidget)

    def __init__(self, parent=None):
        """

        :param parent:
        :return:
        """
        super(CustomWidget, self).__init__(parent)

    def enterEvent(self, *args, **kwargs):
        """

        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        print("......Entered the Fucking browser.......")

    def mouseDoubleClickEvent(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        print(args)


class ImageLibraryMainWindow(qg.QWidget):
    def __init__(self, parent=None):
        """

        :param parent:
        :return:
        """
        super(ImageLibraryMainWindow, self).__init__(parent)

        self.image_path = "/Users/alij/GoogleDrive/insparation"

        self.list_of_images = self._get_images()

        self.max_image_height = 200
        self.max_image_width = 300

        self.resize(1300, 700)

        # Setting Core Ui Attributes ------------------------------------------
        self.acceptDrops()
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Image Library Browser")

        # MainLayout ----------------------------------------------------------
        self.MAIN_LAYOUT = qg.QVBoxLayout()
        self.MAIN_LAYOUT.setSpacing(0)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setAlignment(qc.Qt.AlignTop)

        self.setLayout(self.MAIN_LAYOUT)

        # Search Widgets and Layout -------------------------------------------
        self.search_widgets_layout = qg.QHBoxLayout()
        self.search_widgets_layout.setContentsMargins(0, 0, 0, 0)
        self.search_widgets_layout.setSpacing(1)

        self.option_icon = qg.QPixmap('./icons/options_icon.png')
        self.option_button = qg.QPushButton('')
        self.option_button.setStyleSheet('background-color: transparent;'
                                         'outline: none;')
        self.option_button.setIcon(self.option_icon)
        self.option_button.setMinimumHeight(45)
        self.option_button.setMinimumWidth(40)

        self.search_icon = qg.QPixmap('./icons/search_icon.png')
        self.search_label = qg.QLabel('Search: ')
        self.search_label.setMinimumHeight(45)
        self.search_label.setPixmap(self.search_icon)

        self.search_tags = qg.QLineEdit()
        self.search_tags.setFixedHeight(34)
        self.search_tags.setMinimumWidth(500)

        self.heart_icon = qg.QPixmap('./icons/heart_blue_icon.png')
        self.heart_icon_number = 0
        self.heart_button = qg.QPushButton('')
        self.heart_button.setStyleSheet('background-color: transparent;'
                                        'outline: none;')
        self.heart_button.setMinimumHeight(45)
        self.heart_button.setMinimumWidth(40)
        self.heart_button.setIcon(self.heart_icon)

        self.search_widgets_layout.addWidget(self.option_button)
        self.search_widgets_layout.addWidget(self.search_label)
        self.search_widgets_layout.addWidget(self.search_tags)
        self.search_widgets_layout.addWidget(self.heart_button)

        self.MAIN_LAYOUT.addLayout(self.search_widgets_layout)

        # Browser Frame and Layout --------------------------------------------
        self.browser_frame_layout = FlowLayout()

        self.browser_widget = CustomWidget()
        self.browser_widget.setMouseTracking(True)
        self.browser_widget.setLayout(self.browser_frame_layout)

        # Loading the images into the browser frame --------------------------
        self._load_images()

        self.browser_scroll = qg.QScrollArea()
        self.browser_scroll.setStyleSheet("background-color: black;")
        self.browser_scroll.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOn)
        self.browser_scroll.setWidgetResizable(True)
        self.browser_scroll.acceptDrops()
        self.browser_scroll.setWidget(self.browser_widget)

        self.MAIN_LAYOUT.addWidget(self.browser_scroll)

        # Connecting the Widgets to the Slots----------------------------------
        self._creating_connections()

    # Widget Connect Setup ----------------------------------------------------
    def _creating_connections(self):
        """

        :return:
        """
        # self.browser_widget.enterEvent(self._enter_browser_handler)
        self.option_button.clicked.connect(self._open_option_ui)
        self.heart_button.clicked.connect(self._show_heart_images)
        self.search_tags.returnPressed.connect(self._search_tags)
        self.search_tags.textEdited.connect(self._search_tags_edited)

    # -------------------------------------------------------------------------
    # SLOTS
    # -------------------------------------------------------------------------
    def _open_option_ui(self, *args, **kwargs):
        """

        :return:
        """
        print ("Open Option UI")
        print(self.sender())

    def _show_heart_images(self, *args, **kwargs):
        """

        :return:
        """
        if self.heart_icon_number == 0:
            self.heart_button.setIcon(qg.QPixmap(
                    './icons/heart_red_icon.png'))
            self.heart_icon_number = 1
        else:
            self.heart_button.setIcon(qg.QPixmap(
                    './icons/heart_blue_icon.png'))
            self.heart_icon_number = 0

    def _search_tags(self, *args, **kwargs):
        """

        :return:
        """
        print("Search the DB")

    def _search_tags_edited(self, *args, **kwargs):
        """

        :return:
        """
        print args
        if not self.search_tags.text():
            print("No Tags No Images....")

    def _get_images(self, *args, **kwargs):
        """

        :return:
        """
        return os.listdir(self.image_path)

    def _load_images(self):
        """

        :return:
        """
        list_of_img = self.list_of_images

        for img in list_of_img:
            try:

                image = qg.QPixmap(os.path.join(self.image_path, img))
                image = image.scaledToWidth(self.max_image_width)

                image_label = qg.QLabel(img)
                image_label.setPixmap(image)

                self.browser_frame_layout.addWidget(image_label)
            except Exception as e:
                    print e
        self.update()


def create_ui():
    """
    Create a instance of the PrmanProjectionUi and shows the window
    :return: QDialog
    """

    global image_library_browser_ui
    if image_library_browser_ui is None:
        image_library_browser_ui = ImageLibraryMainWindow()
    image_library_browser_ui.show()


def delete_ui():
    """
    If the UI exists in memory, delete it.
    :return: None
    """

    global image_library_browser_ui
    if image_library_browser_ui is None:
        return

    image_library_browser_ui.deleteLater()
    image_library_browser_ui = None

if __name__ == '__main__':
    """

    """
    import sys

    app = qg.QApplication(sys.argv)
    image_library_browser = ImageLibraryMainWindow()
    image_library_browser.show()
    sys.exit(app.exec_())
