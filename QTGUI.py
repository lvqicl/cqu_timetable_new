import datetime
import sys

from PySide2.QtCore import QFile, QStringListModel, QTimer, QModelIndex, QCoreApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
from main import load_from_xlsx, mkical


class timetable_to_ics():
    def __init__(self):
        super(timetable_to_ics, self).__init__()

        qfile = QFile('layout/mainWindow.ui')
        qfile.open(QFile.ReadOnly)
        qfile.close()
        """
        未按下按钮却执行函数可能是因为未使用 lambda
        参考：
        https://blog.csdn.net/guge907/article/details/23291763
        """
        self.ui = QUiLoader().load(qfile)
        QMessageBox.information(
            self.ui,
            "关于此程序",
            "该程序是在 AGPLv3 下发布的自由软件，源码可在 https://github.com/weearc/cqu_timetable_new 获取，欢迎在遵守该协议的情况下自由运行、拷贝、分发、学习、修改该软件。\n\tCopyright (C) 2021 weearc\nThis program is free software: you can redistribute it and/or modify\n"
            "it under the terms of the GNU Affero General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version."
            "This program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n"
            "You should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>."
        )
        self.ui.BFileSelect.clicked.connect(lambda: self.file_select())
        self.ui.Bhelp.clicked.connect(lambda: self.show_help())
        self.ui.runOnBox.rejected.connect(lambda: QCoreApplication.quit())
        self.ui.runOnBox.accepted.connect(lambda: self.gen_ical(self.ui.startDate.text(), self.ui.fileSelectText.text()))

    def gen_ical(self, start_date, file_path):
        if all([start_date, file_path]) is False:
            QMessageBox.warning(
                self.ui,
                "错误",
                "请勿输入空值"
            )
        else:
            data = load_from_xlsx(file_path)
            isDebug = False
            year = start_date[0:4]
            month = start_date[4:6]
            day = start_date[6:]
            dt = datetime.date(int(year), int(month), int(day))
            cal = mkical(data, dt, isDebug)
            f = open(file_path, 'wb')
            f.write(cal.to_ical())
            f.close()


    def file_select(self):
        file_fileter = "XLSX(*.xlsx)"
        fd = QFileDialog.getOpenFileName(self.ui, "请选择课表文件", filter=file_fileter)
        self.ui.fileSelectText.setText(fd[0])

    def show_help(self):
        QMessageBox.information(
            self.ui,
            "关于",
            "请从登陆选课网站 http://my.cqu.edu.cn/enroll/ ，点击“查看课表”，再点击“Excel”下载课程表数据。点击下方的“OK”后选择下载下来的文件。"
        )

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    mainWindow = timetable_to_ics()
    mainWindow.ui.show()
    sys.exit(app.exec_())