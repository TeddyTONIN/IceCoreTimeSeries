# Teddy Tonin
# Copyrights are given to LSCE and CentraleSupélec

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QLabel, QStyle,QDesktopWidget, QVBoxLayout, QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QFrame,QTreeWidget, QTreeWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor


import numpy as np
from functools import partial


class WorkSheet(QtWidgets.QMainWindow):

    def __init__(self,dataframe, parent =None) -> None:
        super().__init__()
        self.df = dataframe
        self.columns = list(self.df)
        self.is_increasing = {}
        self.linagefolderscount = 0
        self.newsamplinfolderscount = 0
        self.tree_widget = None
        self.abcissas = None
        self.detect_monotony()

        self.setWindowTitle('Organize your Worksheet')
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(
            screen_geometry.center().x() - self.width() // 2,
            screen_geometry.center().y() - self.height() // 2,
            self.width(),
            self.height()
        )
        self.setFixedSize(self.size())
        self.setWindowTitle('Organize your Worksheet')
        main_layout = QVBoxLayout()

      # create a frame to organize the worksheet
        self.dataBox = QFrame()
        self.dataBox.setFrameShape(QFrame.Box)
        self.dataBoxLayout = QVBoxLayout(self.dataBox)
        self.VBoxes = {}
        self.abcissas = {}
        self.monotonic_colums = []
        for i in range(len(self.columns)):
            self.VBoxes[i] = QHBoxLayout()
            self.VBoxes[i].addWidget(QLabel(f'{i+1}'))
            
            if self.is_increasing[self.columns[i]]:
                self.monotonic_colums.append(QLineEdit())
                self.monotonic_colums[-1].setText(self.columns[i])
                self.columnname = self.monotonic_colums[-1].text()
                #self.monotonic_colums[-1].textChanged.connect(self.update_abscissas)
                self.monotonic_colums[-1].setFixedSize(self.monotonic_colums[-1].sizeHint())
                self.VBoxes[i].addWidget(self.monotonic_colums[-1])

                self.abcissas[self.columns[i]]= None
            else:
                self.chooseAbcissa = QLineEdit()
                self.abcissas[self.columns[i]] = self.columnname
                self.chooseAbcissa.setText(self.columns[i])
                self.VBoxes[i].addWidget(self.chooseAbcissa)
                

            self.dataBoxLayout.addLayout(self.VBoxes[i])

        main_layout.addWidget(self.dataBox)
        #add exit or cancel buttons
        cancelok = QHBoxLayout()
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.close_window)
        cancel.setFixedSize(50, 25)
        ok = QPushButton('OK')
        ok.clicked.connect(self.displayWorksheet)
        ok.setFixedSize(50, 25)
        cancelok.addWidget(cancel)
        cancelok.addWidget(ok)

        main_layout.addLayout(cancelok)
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()
    
    def close_window(self):
        self.close()
        
    def detect_monotony(self):
        for col in self.columns:
            cleaned_col = self.df[col].to_numpy()
            cleaned_col = cleaned_col[~np.isnan(cleaned_col)]
            if is_monotonic_increasing(cleaned_col):
                self.is_increasing[col]= True
            else:
                self.is_increasing[col]=False


    def displayWorksheet(self):
        self.worksheet = QtWidgets.QMainWindow()
        self.worksheet.setWindowTitle('Worksheet')

        
        central_widget = QtWidgets.QWidget(self.worksheet)
        self.worksheet.setCentralWidget(central_widget)
        self.worksheetlayout = QVBoxLayout(central_widget)
        


        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Series Name")
        
        
        self.worksheetlayout.addWidget(self.tree_widget)

        if self.abcissas:
            self.add_columns_to_tree()

        self.worksheet.show()
 

    def add_columns_to_tree(self):
        for column_name in self.columns:
            
            # Set icon based on whether it's a file or folder (you can customize the icons)
            if self.abcissas[column_name] is None:
                item_group = QTreeWidgetItem(self.tree_widget, [column_name])
                icon_group = self.style().standardIcon(QStyle.SP_DirIcon)
                item_group.setIcon(0, icon_group)
            else:
                icon = self.style().standardIcon(QStyle.SP_FileIcon)
                item = QTreeWidgetItem(item_group, [''])
                item.setIcon(0, icon)
                item.setText(0, ' ' * 10 + column_name+ ' '+ self.abcissas[column_name])
    
    def add_Linage(self,pointers,agescale, sedimentationrate, overlapping_windows):
        self.linagefolderscount+=1
        item_group = QTreeWidgetItem(self.tree_widget, [f'Linage {self.linagefolderscount}'])
        icon_group = self.style().standardIcon(QStyle.SP_DirIcon)
        item_group.setIcon(0, icon_group)

        for title in ['pointers','agescale','sedimentation_rate', 'overlapped']:
            item = QTreeWidgetItem(item_group, ['Linage'])
            icon = self.style().standardIcon(QStyle.SP_FileIcon)
            item.setIcon(0, icon)
            item.setText(0, ' ' * 10 + title)
            self.tree_widget.itemClicked.connect(partial(self.drawlinage,item,title,pointers,agescale, sedimentationrate, overlapping_windows))


        return None
    def drawlinage(self,clicked_item,title,pointers,agescale, sedimentationrate, overlapping_windows,item,column):
        if clicked_item == item:
            if title == 'overlapped':
                for w in overlapping_windows:
                    w.show()

        return None
    
    def add_NewSampling(self,title, savedwindow,new_x,new_y):
        self.newsamplinfolderscount+=1
        item_group = QTreeWidgetItem(self.tree_widget, [f'New Sampling {self.newsamplinfolderscount}'])
        icon_group = self.style().standardIcon(QStyle.SP_DirIcon)
        item_group.setIcon(0, icon_group)

        item = QTreeWidgetItem(item_group, ['New Sampling'])
        icon = self.style().standardIcon(QStyle.SP_FileIcon)
        item.setIcon(0, icon)
        item.setText(0, ' ' * 10 + title)

        self.tree_widget.itemClicked.connect(partial(self.drawsampling,item,savedwindow,new_x,new_y))

        return None
    

    def drawsampling(self,clicked_item,savedwindow,new_x,new_y,item,column):
        # Placeholder for drawing the two arrays
        # You can implement your drawing logic here
        if clicked_item == item:
            savedwindow.show()

def is_monotonic_increasing(array):
    return np.all(np.diff(array) >= 0)
    



