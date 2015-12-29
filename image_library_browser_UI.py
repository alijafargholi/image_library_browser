"""
Image Library Browser - v0.9

Ali Jafargholi
www.alijafargholi.com
ali.jafargholi@gmail.com
"""

import PySide.QtCore as qc
import PySide.QtGui as qg

import os
# import functools

# Global variable to store the UI status, if it's open or closed
image_library_browser_ui = None
add_images_window = None
options_window = None


class AddToLibrary(qg.QDialog):
    """

    """

    def __init__(self, parent=None):
        """

        :param parent:
        :return:
        """
        super(AddToLibrary, self).__init__(parent)

        self.setWindowTitle("Add Images to Library")
        self.setModal(True)
        self.setFixedWidth(400)
        self.setFixedHeight(190)
        self.setContentsMargins(3, 3, 3, 3)

        self.MAIN_LAYOUT = qg.QFormLayout()
        self.MAIN_LAYOUT.setContentsMargins(3, 3, 3, 3)
        self.MAIN_LAYOUT.setSpacing(2)
        self.setLayout(self.MAIN_LAYOUT)

        # Creating the widgets ------------------------------------------------
        # Pick Image Button
        self.pick_images = qg.QPushButton('Pick Images')
        self.pick_images.setToolTip('Select one or more images to add to the '
                                    'library')
        self.pick_images.setMinimumHeight(35)
        self.pick_images.setMinimumWidth(125)
        self.pick_images.setStyleSheet('background-color: #666699;')
        # Pick Directory Button
        self.pick_directory = qg.QPushButton('Pick Directory')
        self.pick_directory.setToolTip('Pick a directory of images to add to '
                                       'library. Any item that is not an image'
                                       ' will be ignored.')
        self.pick_directory.setMinimumHeight(35)
        self.pick_directory.setMinimumWidth(125)
        self.pick_directory.setStyleSheet('background-color: #666699;')

        self.pick_layout = qg.QHBoxLayout()
        self.pick_layout.setSpacing(15)
        self.pick_layout.setContentsMargins(1, 1, 1, 1)
        self.pick_layout.addWidget(self.pick_images)
        self.pick_layout.addWidget(self.pick_directory)
        # Options Check Boxes
        self.check_nested_directory = qg.QCheckBox('Include Nested Directory?')
        self.check_nested_directory.setToolTip('When this check box is \n'
                                               'checked, all the directories\n'
                                               'inside the selected folder '
                                               '\nwill be checked for images '
                                               'and\nif it finds more images,'
                                               '\nit\'ll add them to the '
                                               'library')
        self.dir_name_album = qg.QCheckBox('Add directory name as an Album?')
        self.dir_name_album.setToolTip('If it\'s check, the name of the\n '
                                       'folder will be consider as an album')

        self.check_layout = qg.QVBoxLayout()
        self.check_layout.setContentsMargins(0, 0, 0, 0)
        self.check_layout.setSpacing(2)
        self.check_layout.addWidget(self.check_nested_directory)
        self.check_layout.addWidget(self.dir_name_album)
        # Tags
        self.tags_label = qg.QLabel('Tags: ')
        self.tags = qg.QLineEdit()
        self.tags.setPlaceholderText('Separate Tags with "," - No Space')
        self.tags.setMinimumWidth(250)
        # Album
        self.album_label = qg.QLabel('Albums: ')
        self.album = qg.QLineEdit()
        self.album.setPlaceholderText('Separate Names with "," - No Space')
        self.album.setMinimumWidth(250)
        # Action Buttons
        self.create = qg.QPushButton('OK')
        self.create.setStyleSheet('background-color: green;')
        self.create.setMinimumWidth(170)
        self.create.setMinimumHeight(35)

        self.cancel = qg.QPushButton('Cancel')
        self.cancel.setStyleSheet('background-color: #808080;')
        self.cancel.setMinimumHeight(35)
        self.cancel.setMinimumWidth(60)

        self.final_layout = qg.QHBoxLayout()
        self.final_layout.setSpacing(15)
        self.final_layout.addWidget(self.create)
        self.final_layout.addWidget(self.cancel)

        # Adding all the widgets and layouts to the main layout ---------------
        self.MAIN_LAYOUT.addRow(qg.QLabel(), self.pick_layout)
        self.MAIN_LAYOUT.addRow(qg.QLabel(), self.check_layout)
        self.MAIN_LAYOUT.addRow(self.tags_label, self.tags)
        self.MAIN_LAYOUT.addRow(self.album_label, self.album)
        self.MAIN_LAYOUT.addRow(qg.QLabel(), self.final_layout)

        # Connecting the Widgets to the Slots ---------------------------------
        self._create_connections()

    def _create_connections(self):
        """
        """
        self.pick_images.clicked.connect(self.pick_images_action)
        self.pick_directory.clicked.connect(self.pick_directory_action)
        self.create.clicked.connect(self.add_to_db)
        self.cancel.clicked.connect(self.close)

    # -------------------------------------------------------------------------
    # SLOTS
    # -------------------------------------------------------------------------
    def pick_images_action(self, *args, **kwargs):
        """
        """
        print args
        print "Pick Images"

    def pick_directory_action(self, *args, **kwargs):
        """
        """
        print "Pick Directory"

    def add_to_db(self, *args, **kwargs):
        """
        """
        print "Add to DataBase"


class OptionWindow(qg.QDialog):
    """

    """

    def __init__(self, parent=None):
        """

        :param parent:
        :return:
        """
        super(OptionWindow, self).__init__(parent)

        self.main_window = parent

        self.setWindowTitle("Options")
        self.setModal(True)
        self.setFixedWidth(200)
        self.setMinimumHeight(350)
        self.setContentsMargins(1, 1, 1, 1)

        self.MAIN_LAYOUT = qg.QVBoxLayout()
        self.MAIN_LAYOUT.setContentsMargins(1, 1, 1, 1)
        self.MAIN_LAYOUT.setSpacing(2)
        # self.MAIN_LAYOUT.setAlignment(qc.Qt.AlignTop)
        self.setLayout(self.MAIN_LAYOUT)

        # Creating the widgets ------------------------------------------------
        # Sort By
        self.sort_label = qg.QLabel('Sort By:')
        self.sort_label.setMaximumHeight(25)
        self.sort_by_name = qg.QRadioButton('Name')
        self.sort_by_name.setChecked(True)
        self.sort_by_date = qg.QRadioButton('Date')
        self.sort_by_size = qg.QRadioButton('Size')
        # Sort By Layout
        self.sort_layout = qg.QHBoxLayout()
        self.sort_layout.setContentsMargins(1, 1, 1, 1)
        self.sort_layout.setSpacing(1)
        self.sort_layout.addWidget(self.sort_by_name)
        self.sort_layout.addWidget(self.sort_by_date)
        self.sort_layout.addWidget(self.sort_by_size)
        # Separator 1
        self.separator_01 = qg.QFrame()
        self.separator_01.setFrameStyle(qg.QFrame.HLine)
        # Buttons
        self.add_to_library = qg.QPushButton('Add Images to Library')
        self.add_to_library.setMinimumHeight(40)
        self.remove_tags = qg.QPushButton('Remove Tags from Selection')
        self.remove_tags.setMinimumHeight(40)
        # Separator 2
        self.separator_02 = qg.QFrame()
        self.separator_02.setFrameStyle(qg.QFrame.HLine)
        # Buttons
        self.settings_window = qg.QPushButton('Settings')
        self.settings_window.setMinimumHeight(40)
        self.refresh_db = qg.QPushButton('Refresh Data Base')
        self.refresh_db.setMinimumHeight(40)
        # Separator 3
        self.separator_03 = qg.QFrame()
        self.separator_03.setFrameStyle(qg.QFrame.HLine)
        # Buttons
        self.help_wiki = qg.QPushButton('Help')
        self.help_wiki.setMinimumHeight(40)
        self.about_window = qg.QPushButton('About')
        self.about_window.setMinimumHeight(40)
        # Separator 4
        self.separator_04 = qg.QFrame()
        self.separator_04.setFrameStyle(qg.QFrame.HLine)
        # Buttons
        self.close_library = qg.QPushButton('Close Library Window')
        self.close_library.setMinimumHeight(40)

        # Adding all the widgets and layouts to the main layout ---------------
        self.MAIN_LAYOUT.addWidget(self.sort_label)
        self.MAIN_LAYOUT.addLayout(self.sort_layout)
        self.MAIN_LAYOUT.addWidget(self.separator_01)
        self.MAIN_LAYOUT.addWidget(self.add_to_library)
        self.MAIN_LAYOUT.addWidget(self.remove_tags)
        self.MAIN_LAYOUT.addWidget(self.separator_02)
        self.MAIN_LAYOUT.addWidget(self.settings_window)
        self.MAIN_LAYOUT.addWidget(self.refresh_db)
        self.MAIN_LAYOUT.addWidget(self.separator_03)
        self.MAIN_LAYOUT.addWidget(self.help_wiki)
        self.MAIN_LAYOUT.addWidget(self.about_window)
        self.MAIN_LAYOUT.addWidget(self.separator_04)
        self.MAIN_LAYOUT.addWidget(self.close_library)

        # Connecting the Widgets to the Slots----------------------------------
        self._create_connections()

    def _create_connections(self):
        """
        """
        self.add_to_library.clicked.connect(self.add_to_library_action)
        self.remove_tags.clicked.connect(self.remove_tags_action)
        self.settings_window.clicked.connect(self.settings_window_action)
        self.refresh_db.clicked.connect(self.refresh_db_action)
        self.help_wiki.clicked.connect(self.help_wiki_action)
        self.about_window.clicked.connect(self.about_window_action)
        self.close_library.clicked.connect(self.close_library_action)

    # -------------------------------------------------------------------------
    # SLOTS
    # -------------------------------------------------------------------------
    def add_to_library_action(self):
        """
        """
        global add_images_window
        print("add_to_library_action")
        # print(self.sender())
        add_images_window = AddToLibrary(parent=self)
        add_images_window_result = add_images_window.exec_()
        if add_images_window_result:
            print "Oked"
        else:
            print "Got Canceled"
            add_images_window.deleteLater()
            add_images_window = None

    def remove_tags_action(self):
        """
        """
        print("remove_tags_action")

    def settings_window_action(self):
        """
        """
        print("settings_window_action")

    def refresh_db_action(self):
        """
        """
        print("refresh_db_action")

    def help_wiki_action(self):
        """
        """
        print("help_wiki_action")

    def about_window_action(self):
        """
        """
        print("about_window_action")

    def close_library_action(self):
        """
        """
        print("close_library_action")
        self.close()
        self.main_window.close()


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
        self.search_layout_height = 40

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
        self.search_widgets_layout.setSpacing(5)

        self.option_icon = qg.QPixmap('./icons/options_icon.png')
        self.option_button = qg.QPushButton('')
        self.option_button.setStyleSheet('background-color: transparent;'
                                         'outline: none;'
                                         'border: 0;')
        self.option_button.setIcon(self.option_icon)
        self.option_button.setAutoFillBackground(True)
        self.option_button.setMinimumHeight(self.search_layout_height)
        self.option_button.setMinimumWidth(self.search_layout_height)
        self.option_button.setIconSize(qc.QSize(self.search_layout_height,
                                                self.search_layout_height))

        self.search_tags = qg.QLineEdit()
        self.search_tags.setFixedHeight(self.search_layout_height)
        self.search_tags.setMinimumWidth(500)

        self.heart_icon = qg.QPixmap('./icons/heart_blue_icon.png')
        self.heart_icon_number = 0
        self.heart_button = qg.QPushButton('')
        self.heart_button.setStyleSheet('background-color: transparent;'
                                        'outline: none;'
                                        'border: 0;')
        self.heart_button.setMinimumHeight(self.search_layout_height)
        self.heart_button.setMinimumWidth(self.search_layout_height)
        self.heart_button.setIcon(self.heart_icon)
        self.heart_button.setIconSize(qc.QSize(self.search_layout_height,
                                               self.search_layout_height))

        self.user_icon = qg.QPixmap('./icons/user_off.png')
        self.user_icon_number = 0
        self.user_button = qg.QPushButton()
        self.user_button.setStyleSheet('background-color: transparent;'
                                       'outline: none;'
                                       'border: 0;')
        self.user_button.setMinimumHeight(self.search_layout_height)
        self.user_button.setMinimumWidth(self.search_layout_height)
        self.user_button.setIcon(self.user_icon)
        self.user_button.setIconSize(qc.QSize(self.search_layout_height,
                                              self.search_layout_height))

        self.search_widgets_layout.addWidget(self.option_button)
        self.search_widgets_layout.addWidget(self.search_tags)
        self.search_widgets_layout.addWidget(self.heart_button)
        self.search_widgets_layout.addWidget(self.user_button)

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
        self.user_button.clicked.connect(self._show_user_images)
        self.search_tags.returnPressed.connect(self._search_tags)
        # self.search_tags.textEdited.connect(self._search_tags_edited)

    # -------------------------------------------------------------------------
    # SLOTS
    # -------------------------------------------------------------------------
    def _show_user_images(self):
        """

        :return:
        """
        if self.user_icon_number == 0:
            self.user_button.setIcon(qg.QPixmap('./icons/user_on.png'))
            self.user_icon_number = 1
        else:
            self.user_button.setIcon(qg.QPixmap('./icons/user_off.png'))
            self.user_icon_number = 0

    def _open_option_ui(self, *args, **kwargs):
        """

        :return:
        """
        global options_window
        print ("Open Option UI")
        print(qg.QCursor.pos())
        # print(self.sender())
        options_window = OptionWindow(parent=self)
        options_window.move(qg.QCursor.pos())
        options_window_result = options_window.exec_()
        if options_window_result:
            print "Oked"
        else:
            print "Got Canceled"
            options_window.deleteLater()
            options_window = None

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
        if not self.search_tags.text():
            print("No Tags No Images....")
        else:
            if "," in self.search_tags.text():
                print(self.search_tags.text())

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
