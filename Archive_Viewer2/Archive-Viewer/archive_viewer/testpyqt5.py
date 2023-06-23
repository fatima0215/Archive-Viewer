import typing
from pydm import Display
from qtpy import QtCore
from qtpy.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QTabWidget, QGroupBox,
    QScrollArea, QSizePolicy, QPushButton, QCheckBox, QColorDialog, QComboBox, QSlider,
    QLineEdit, QSpacerItem, QTableWidget, QTableWidgetItem, QCalendarWidget, QSpinBox
)
from qtpy.QtGui import QIcon
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
from pydm.widgets import PyDMArchiverTimePlot, PyDMWaveformPlot
from pv_table import PyDMPVTable
from functools import partial
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap


class ArchiveViewerLogic():
    pass
 
class ArchiveViewer(Display):
    """
    PyDM version of the Archive Viewer.
    """
    def __init__(self, parent=None, args=None, macros=None):
        super(ArchiveViewer, self).__init__(parent=parent, args=args, macros=macros)
        self.app = QApplication.instance()
        self.setup_ui()

    def fetch_data_from_table(self):
        columns = self.input_table.table.columnCount()
        rows = self.input_table.table.rowCount()

        print(self.input_table.data[0]())
        print(rows, columns)

        for row_index in range(0, rows):
            for column_index in range(0, columns):
                print(row_index, column_index)
                #print(self.input_table.table.cellWidget(row_index, column_index))

                if column_index == 0:
                    print(self.input_table.table.cellWidget(row_index, column_index).text)

    def update_plot(self):
        print("landing here")
        print(self.input_table.data[0][7](), self.input_table.data[0][0]())
        print(len(self.input_table.data))

        try:
            for index in range(0, len(self.input_table.data)):
                print(self.input_table.data[index][0])
                self.time_plots.addYChannel(
                    y_channel="archiver://" + self.input_table.data[index][0](),
                    lineWidth=self.input_table.data[index][7]()
                )
        except Exception:
            print("error")



        '''
        color=self.input_table.data[index][5],

        lineStyle=self.input_table.data[index][6],

        self.input_table.data[index][2](),
        self.input_table.data[index][3](),
        self.input_table.data[index][4]()
        '''

    def minimumSizeHint(self):
        """

        """
        return QtCore.QSize(1050, 600)

    def setup_ui(self):
        """

        """
        # main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # plot widgets
        self.time_plots = PyDMArchiverTimePlot()
        self.waveforms = PyDMWaveformPlot()
        self.correlations = PyDMWaveformPlot()  # needs changing

        # tab widget to hold plots
        plot_tab_widget = QTabWidget()
        plot_tab_widget.addTab(self.time_plots, "Time Plots")
        plot_tab_widget.addTab(self.waveforms, "Waveforms")
        plot_tab_widget.addTab(self.correlations, "Correlations")

        #Data Table 
        self.input_table = PyDMPVTable(
            table_headers=["PV NAME", "TIME AXIS", "RANGE AXIS", "VISIBLE", "RAW", "COLOR", "TYPE", "WIDTH"],
            number_columns=8,
            col_widths=[100])
        
        self.input_data_tab = QWidget()
        self.input_data_layout = QHBoxLayout()
        self.input_data_layout.addWidget(self.input_table)
        self.input_data_layout.setContentsMargins(0, 0, 0, 0)

        # Range Menu
        min_label = QLabel("Min:")
        max_label = QLabel("Max:")
        min_input = QLineEdit()
        max_input = QLineEdit()
        keep_range_label = QLabel("Keep Ranges")
        keep_range_check_box = QCheckBox()
        type_lable = QLabel("Type")

        range_tab = QWidget()
        range_layout = QGridLayout()
        range_layout.setVerticalSpacing(0)
        range_layout.addWidget(min_label)
        range_layout.addWidget(min_input,  0, 1)
        range_layout.addWidget(max_label)
        range_layout.addWidget(max_input,  1, 1)
        range_layout.addWidget(keep_range_check_box)
        range_layout.addWidget(keep_range_label)
        range_layout.addWidget(type_lable, 1, 2)

        # # time Menu
        # min_label_time = QLabel("Start:")
        # max_label_time = QLabel("End:")
        # min_input_time = QLineEdit()
        # max_input_time = QLineEdit()
        # keep_range_label_time = QLabel("Keep Ranges")
        # keep_range_check_box_time = QCheckBox()
        # type_label_time = QLabel("Type")


        time_tab = QWidget()

            # Create the time axis table widget
        time_axis_table = QTableWidget()
        time_axis_table.setColumnCount(6)
        time_axis_table.setHorizontalHeaderLabels(["Axis Name", "Start", "End", "Calendar", "Slider", "Position"])

        # Add rows to the table
        time_axis_table.setRowCount(3)

        # Populate the cells with widgets and data
        axis_name_item = QTableWidgetItem("Main Time Axis")
        time_axis_table.setItem(0, 0, axis_name_item)

        start_item = QTableWidgetItem("")
        time_axis_table.setItem(0, 1, start_item)

        end_item = QTableWidgetItem("")
        time_axis_table.setItem(0, 2, end_item)

        # Create a QPushButton with a calendar icon
        calendar_button = QPushButton()
        icon_path = "Users/fatima-osman/projects/Archive_Viewer2/Archive-Viewer/archive_viewer/calendar_icon.png"
        calendar_icon = QIcon(icon_path)
        calendar_button.setIcon(calendar_icon)
        calendar_button.setIconSize(QtCore.QSize(16, 16))
        calendar_button.setFixedSize(20, 20)
        calendar_button.clicked.connect(self.open_calendar_tab)

        time_axis_table.setCellWidget(0, 3, calendar_button)

        slider = QSlider(QtCore.Qt.Horizontal)
        time_axis_table.setCellWidget(0, 4, slider)

        position_spinbox = QSpinBox()
        time_axis_table.setCellWidget(0, 5, position_spinbox)

        # Add more rows and customize the slider
        for row in range(1, 3):
            time_axis_table.setRowHeight(row, 30)
            time_axis_table.setCellWidget(row, 4, QSlider(QtCore.Qt.Horizontal))
            time_axis_table.setCellWidget(row, 5, QSpinBox())

        # Create a tab widget to hold the calendar widget
        calendar_tab_widget = QTabWidget()
        calendar_tab_widget.addTab(QCalendarWidget(), "Calendar")

        # Create the layout for the time tab
        time_layout = QVBoxLayout()
        time_layout.addWidget(time_axis_table)

        # Create the main layout for the time tab
        time_tab_layout = QVBoxLayout()
        time_tab_layout.addLayout(time_layout)
        time_tab_layout.addWidget(calendar_tab_widget)

        # Create the time tab widget and set the layout
        time_tab = QWidget()
        time_tab.setLayout(time_tab_layout)

        # time_layout.addWidget(min_label_time)
        # time_layout.addWidget(min_input_time,  0, 1)
        # time_layout.addWidget(max_label_time)
        # time_layout.addWidget(max_input_time,  1, 1)
        # time_layout.addWidget(keep_range_check_box_time)
        # time_layout.addWidget(keep_range_label_time)
        # time_layout.addWidget(type_label_time, 1, 2)
        
        self.input_data_tab.setLayout(self.input_data_layout)
        range_tab.setLayout(range_layout)
        time_tab.setLayout(time_layout)


        self.settings_tab_widget = QTabWidget()
        self.settings_tab_widget.addTab(self.input_data_tab, "Input Data")
        self.settings_tab_widget.addTab(range_tab, "Range")
        self.settings_tab_widget.addTab(time_tab, "Time Axis")
        

        #set up time toggle buttons 
        self.time_toggle_buttons = []
        time_toggle_layout = QHBoxLayout()

        #horizontal spacer for toggle buttons
        horizontal_spacer = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        time_toggle_layout.addItem(horizontal_spacer)

        self.time_toggle = [('30s', None), ('1m', None), ('1h', None), ('1w', None), ('1m', None)]
        for index in range(0, len(self.time_toggle)):
            self.time_toggle_buttons.append(QPushButton(self.time_toggle[index][0], self))
            self.time_toggle_buttons[index].setGeometry(200, 150, 100, 40)
            self.time_toggle_buttons[index].setCheckable(True)
            self.time_toggle_buttons[index].clicked.connect(partial(self.time_toggle_button_action, index))
            time_toggle_layout.addWidget(self.time_toggle_buttons[index])

        #set up misc toggle buttons 
        self.misc_button = []
        misc_toggle_layout = QHBoxLayout()

        self.misc_toggle = [('curser', None), ('Y axis autoscale', None), ('Live', None)]
        for index in range(0, len(self.misc_toggle)):
            self.misc_button.append(QPushButton(self.misc_toggle[index][0], self))
            self.misc_button[index].setGeometry(200, 150, 100, 40)
            self.misc_button[index].setCheckable(True)
            self.misc_button[index].clicked.connect(partial(self.misc_toggle_button_action, index))
            misc_toggle_layout.addWidget(self.misc_button[index])

        time_misc_boxes_layout = QHBoxLayout()
        time_misc_boxes_layout.addLayout(time_toggle_layout)
        time_misc_boxes_layout.addLayout(misc_toggle_layout)

        main_layout.addLayout(time_misc_boxes_layout)
        main_layout.addWidget(plot_tab_widget)
        main_layout.addWidget(self.settings_tab_widget)

        self.input_table.send_data_change_signal.connect(self.update_plot)

    def open_calendar_tab(self):
        calendar_tab = QWidget()
        calendar_layout = QVBoxLayout()
        calendar_widget = QCalendarWidget()
        calendar_layout.addWidget(calendar_widget)
        calendar_tab.setLayout(calendar_layout)
        self.settings_tab_widget.addTab(calendar_tab, "Calendar")

    def time_toggle_button_action(self, index):            
        for i in range(0, len(self.time_toggle_buttons)):
            if i != index: 
                self.time_toggle_buttons[i].setChecked(False)

        #self.time_toggle[index][1]
    
    def misc_toggle_button_action(self, index):
        pass

    