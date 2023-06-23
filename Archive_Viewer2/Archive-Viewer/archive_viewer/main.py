import typing
from pydm import Display
from qtpy import QtCore
from qtpy.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QTabWidget, QGroupBox,
                            QScrollArea, QSizePolicy, QPushButton, QCheckBox, QColorDialog, QComboBox, QSlider,
                            QLineEdit, QSpacerItem, QTableWidget, QTableWidgetItem, QCalendarWidget, QSpinBox)
from pydm.widgets import PyDMArchiverTimePlot, PyDMWaveformPlot
from pv_table import PyDMPVTable
from time_menu_table import TimeMenuWidget
from functools import partial


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

        # time Menu
        time_tab = QWidget()

        # Create the time menu widget
        time_menu_widget = TimeMenuWidget()

        # Add the time menu widget to the layout
        time_layout = QVBoxLayout()
        time_layout.addWidget(time_menu_widget)

        time_tab.setLayout(time_layout)
        
        # time_tab = QWidget()

        # # Create the time axis table widget
        # time_axis_table = QTableWidget()
        # time_axis_table.setColumnCount(6)
        # time_axis_table.setHorizontalHeaderLabels(["AXIS NAME", "START", "END", "CALENDAR", "SLIDER", "POSITION"])

        # # Add rows to the table
        # time_axis_table.setRowCount(3)

        # # Populate the cells with widgets and data
        # axis_name_item = QTableWidgetItem("Main Time Axis")
        # time_axis_table.setItem(0, 0, axis_name_item)

        # start_item = QTableWidgetItem("")
        # time_axis_table.setItem(0, 1, start_item)

        # end_item = QTableWidgetItem("")
        # time_axis_table.setItem(0, 2, end_item)

        # calendar_widget = QCalendarWidget()
        # time_axis_table.setCellWidget(0, 3, calendar_widget)

        # slider = QSlider(QtCore.Qt.Horizontal)
        # time_axis_table.setCellWidget(0, 4, slider)

        # position_spinbox = QSpinBox()
        # time_axis_table.setCellWidget(0, 5, position_spinbox)

        # # Add more rows and customize the slider
        # for row in range(1, 3):
        #     time_axis_table.setRowHeight(row, 30)

        #     # Add widgets and data to the new rows
        #     time_axis_table.setCellWidget(row, 4, QSlider(QtCore.Qt.Horizontal))
        #     time_axis_table.setCellWidget(row, 5, QSpinBox())

        # # Add the time axis table to the layout
        # time_layout = QVBoxLayout()
        # time_layout.addWidget(time_axis_table)

        # time_tab.setLayout(time_layout)

        
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

    def time_toggle_button_action(self, index):            
        for i in range(0, len(self.time_toggle_buttons)):
            if i != index: 
                self.time_toggle_buttons[i].setChecked(False)

        #self.time_toggle[index][1]
    
    def misc_toggle_button_action(self, index):            
        pass

        # self.misc_toggle[index][1]
# The code you provided is a partial implementation of an Archive Viewer application using PyDM (Python Display Manager) for creating graphical user interfaces (GUIs) with PyQt. It seems to be a work in progress, as some parts are missing or not fully implemented.

# Here's a breakdown of the code:

# The necessary imports are made, including typing for type hints, various PyQt modules, and other required dependencies.

# There is an empty ArchiveViewerLogic class, which you can use to implement the logic for your application.

# The ArchiveViewer class is defined, which inherits from Display class provided by PyDM. This class represents the main window of the Archive Viewer application.

# The __init__ method initializes the ArchiveViewer object and calls the setup_ui method to set up the user interface.

# The fetch_data_from_table method retrieves data from the input table and prints it. It iterates over each cell in the table and retrieves the text from the cell widget if it exists.

# The update_plot method is responsible for updating the plot based on the data in the input table. It prints some debug information and attempts to add Y channels to the time_plots object based on the data in the input table. However, some parts of the code related to setting properties of the plots are commented out.

# The minimumSizeHint method returns the recommended minimum size for the ArchiveViewer window.

# The setup_ui method sets up the user interface of the application. It creates various widgets, layouts, and tabs. The main layout is a QVBoxLayout that contains the toggle buttons layout, the plot tab widget, and the settings tab widget.

# The input_table object is an instance of PyDMPVTable, which is a custom table widget provided by PyDM for displaying process variable (PV) data. It is initialized with column headers and some other parameters.

# The input_data_tab is a QWidget that holds the input table. It uses a QHBoxLayout as its layout.

# The range_tab is a QWidget that represents the "Range" tab in the settings tab widget. It contains a grid layout (QGridLayout) with labels, input fields, and checkboxes for specifying range-related settings.

# The time_tab is a QWidget that represents the "Time Axis" tab in the settings tab widget. It contains a QTableWidget for specifying time axis settings.

# The settings_tab_widget is a QTabWidget that holds the different tabs related to settings.

# The time_toggle_buttons and misc_buttons are lists of QPushButton objects representing the time and misc toggle buttons, respectively. They are created dynamically based on the data in time_toggle and misc_toggle lists.

# The time_toggle_button_action and misc_toggle_button_action are callback functions for handling button clicks. Currently, they don't perform any specific actions.

# The main_layout is populated with the toggle buttons, plot tab widget, and settings tab widget.

# The input_table.send_data_change_signal signal is connected to the update_plot method.

# There are some comments and commented-out code that suggest additional features and functionalities that could be implemented, such as calendar selection and dynamic slider/spinbox creation.

# Please note that this is only a partial implementation, and some parts of the code may be missing or incomplete. You'll need to fill in the missing parts and implement the desired functionalities to make the application fully functional.
    
