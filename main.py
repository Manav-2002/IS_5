import sys
from PyQt5 import QtWidgets
import sys 
import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import pandas as pd
from sidebar_ui import Ui_MainWindow
from collections import OrderedDict 
import numpy as np
from cusum import detect_cusum

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_8)
        self.ui.pushButton.clicked.connect(self.g)

    def g(self):
        filename=QtWidgets.QFileDialog.getOpenFileName(None,'load Data',os. getcwd(),'*.csv')
        
        if((os.path.splitext(filename[0])[1]!='.csv')):
           msg = QtWidgets.QMessageBox()
           msg.setIcon(QtWidgets.QMessageBox.Critical)
           msg.setText("Wrong File Selected")
           msg.setWindowTitle("Error")
           msg.show()
           msg.exec_()
        
        else:
            self.ui.lineEdit.setText(filename[0])
            print(filename[0])
            self.df = pd.read_csv(filename[0])
            self.ui.tableWidget.setRowCount(len(self.df))
            self.ui.tableWidget.setColumnCount(len(self.df))
            for i in range(len(self.df)):
                for j in range(len(self.df.columns)):
                    item = QtWidgets.QTableWidgetItem(str(self.df.iloc[i, j]))
                    self.ui.tableWidget.setItem(i, j, item)
            
            headers = self.df.columns
            self.ui.tableWidget.setHorizontalHeaderLabels(headers)
            for i in self.df.columns:
                self.ui.comboBox.addItem(i)
                self.ui.comboBox_2.addItem(i)
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_9)
            self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_5)
    def on_pushButton_2_clicked(self):
        self.plot_data()
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_11)    
    def on_pushButton_3_clicked(self):
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_12)
    def on_pushButton_4_clicked(self):
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_13)
    def on_pushButton_5_clicked(self):
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_14)
    def on_pushButton_6_clicked(self):
        self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_4)
        self.ui.tableWidget_2.setRowCount(6)
        self.ui.tableWidget_2.setColumnCount(2)
        self.series = self.df[self.ui.comboBox.currentText()].values

        item00 = QtWidgets.QTableWidgetItem("missing values")
        item01 = QtWidgets.QTableWidgetItem("mean")
        item02 = QtWidgets.QTableWidgetItem("variance")
        item03 = QtWidgets.QTableWidgetItem("minimum value")
        item04= QtWidgets.QTableWidgetItem("maximum value")
        item05 = QtWidgets.QTableWidgetItem("median")
        
        self.ui.tableWidget_2.setItem(0, 0, item00)
        self.ui.tableWidget_2.setItem(1, 0, item01)
        self.ui.tableWidget_2.setItem(2, 0, item02)
        self.ui.tableWidget_2.setItem(3, 0, item03)
        self.ui.tableWidget_2.setItem(4, 0, item04)
        self.ui.tableWidget_2.setItem(5, 0, item05)
        for i in range(6):
            item= QtWidgets.QTableWidgetItem(str(self.df[self.ui.comboBox_2.currentText()].describe()[i]))
            self.ui.tableWidget_2.setItem(i,1,item)
        
        self.ui.tableWidget_2.horizontalHeader().setVisible(False)
        # item1 = QtWidgets.QTableWidgetItem(str(1))
        # self.ui.tableWidget_2.setItem(1, 1, item1)


    ## Function for searching
    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashborad_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_dashborad_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_orders_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_orders_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_products_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_products_btn_2_toggled(self, ):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_customers_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_customers_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)
    def plot_data(self):
        if (self.ui.comboBox.currentText() == ''):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Please enter a cloumn name to plot")
            msg.setWindowTitle("Error")
            msg.show()
            msg.exec_()
        
        else:
            # try:
            self.series = self.df[self.ui.comboBox.currentText()].values
            
            # print(type(self.series))
            # self.lineEdit_2.setText(str(np.isnan(self.series).sum()))
            # self.lineEdit_3.setText(str(len(self.series) - np.isnan(self.series).sum()))
            self.ui.graphicsView.figure.clf()
            ax=self.ui.graphicsView.figure.add_subplot(111)
            ax.plot(self.series,'m')
            ax.grid(True)
            ax.set_ylabel('Amplitude')
            ax.set_title(self.ui.comboBox.currentText())
            #ax.set_xlim(-1,1)
            self.ui.graphicsView_4.figure.clf()
            # self.ui.graphicsView.figure.clf()
            self.ui.graphicsView_2.figure.clf()
            self.ui.graphicsView_3.figure.clf()
            ax1=self.ui.graphicsView_2.figure.add_subplot(111)
            ax2=self.ui.graphicsView_3.figure.subplots(1,3)
            ax3=self.ui.graphicsView_4.figure.add_subplot(111)
            ta, tai, taf, amp, gp, gn=detect_cusum(self.df[self.ui.comboBox.currentText()][~self.df[self.ui.comboBox.currentText()].isnull()],threshold=2,drift=0,show=False)
            # print(len(ta))
            x=self.df[self.ui.comboBox.currentText()][~self.df[self.ui.comboBox.currentText()].isnull()]
            x = np.atleast_1d(x).astype('float64')
            # threshold=float(self.lineEdit_4.text())
            # # print(self.lineEdit_4.text())
            # drift=float(self.lineEdit_5.text())
            # print(self.lineEdit_5.text())
            threshold=1
            drift=0
            ending=False
            # gp, gn = np.zeros(x.size), np.zeros(x.size)
            t = range(x.size)
            ax1.plot(t, x, 'b-', lw=2)
            print("hhhhhhhhhhhh")
            print(len(ta))
            if len(ta):
                ax1.plot(tai, x[tai], '>', mfc='g', mec='g', ms=10,
                        label='Start')
                if ending:
                    ax1.plot(taf, x[taf], '<', mfc='g', mec='g', ms=10,
                            label='Ending')
                ax1.plot(ta, x[ta], 'o', mfc='r', mec='r', mew=1, ms=5,
                        label='Alarm')
                ax1.legend(loc='best', framealpha=.5, numpoints=1)
            ax1.set_xlim(-.01*x.size, x.size*1.01-1)
            ax1.set_xlabel('Data #', fontsize=14)
            ax1.set_ylabel('Amplitude', fontsize=14)
            ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
            yrange = ymax - ymin if ymax > ymin else 1
            ax1.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
            ax1.set_title('Time series and detected changes ' +
                        '(threshold= %.3g, drift= %.3g): N changes = %d'
                        % (threshold, drift, len(tai)))
            # ax2.plot(t, gp, 'y-', label='+')
            # ax2.plot(t, gn, 'm-', label='-')
            # ax2.set_xlim(-.01*x.size, x.size*1.01-1)
            # ax2.set_xlabel('Data #', fontsize=14)
            # ax2.set_ylim(-0.01*threshold, 1.1*threshold)
            # ax2.axhline(threshold, color='r')
            ax1.set_ylabel('Amplitude', fontsize=14)
            # ax2.set_title('Time series of the cumulative sums of ' +
                        # 'positive and negative changes')
            # ax2.legend(loc='best', framealpha=.5, numpoints=1)
            # ax2[0].plot(self.df[self.ui.comboBox.currentText()][0:74].to_numpy())
            # ax2[1].plot(self.df[self.ui.comboBox.currentText()][74:120].to_numpy())
            # ax2[2].plot(self.df[self.ui.comboBox.currentText()][160:170].to_numpy())
            # ax2[1].plot(self.df[self.ui.comboBox.currentText()][223:].to_numpy())
            tai2=tai
            list(OrderedDict.fromkeys(tai2))
            f=0
            for i in tai2[1:]:
                ax3.plot(self.df[self.ui.comboBox.currentText()][f:i].to_numpy())
                f=i
            ax3.plot(self.df[self.ui.comboBox.currentText()][f:].to_numpy())
            self.ui.graphicsView.figure.tight_layout()
            self.ui.graphicsView.canvas.draw()
            self.ui.graphicsView_2.figure.tight_layout()
            self.ui.graphicsView_2.canvas.draw()
            self.ui.graphicsView_3.figure.tight_layout()
            self.ui.graphicsView_3.canvas.draw()
            
            self.ui.graphicsView_4.figure.tight_layout()
            self.ui.graphicsView_4.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ## loading style file
    # with open("style.qss", "r") as style_file:
    #     style_str = style_file.read()
    # app.setStyleSheet(style_str)

    ## loading style file, Example 2
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())


    window = MainWindow()
    window.show()

    sys.exit(app.exec())



