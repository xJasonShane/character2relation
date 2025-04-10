"""
主程序入口文件

功能：
1. 初始化应用程序
2. 创建主窗口
3. 加载各功能模块界面
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

# 导入各功能模块
from relation_graph import RelationGraphTab
from settings import SettingsTab
from setup import SetupTab
from about import AboutTab

class MainWindow(QMainWindow):
    """主窗口类"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("角色关系图工具")
        self.setGeometry(100, 100, 1024, 768)
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 添加各功能标签页
        self.relation_graph_tab = RelationGraphTab()
        self.settings_tab = SettingsTab()
        self.setup_tab = SetupTab()
        self.about_tab = AboutTab()
        
        self.tabs.addTab(self.relation_graph_tab, "关系图")
        self.tabs.addTab(self.settings_tab, "设定")
        self.tabs.addTab(self.setup_tab, "设置")
        self.tabs.addTab(self.about_tab, "关于")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())