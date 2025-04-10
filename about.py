"""
关于界面模块

功能：
1. 显示软件作者信息
2. 提供Github链接
3. 检查更新功能
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class AboutTab(QWidget):
    """关于标签页类"""
    def __init__(self):
        super().__init__()
        
        # 主布局
        self.main_layout = QVBoxLayout()
        
        # 作者信息
        self.author_label = QLabel("作者: Your Name")
        self.github_label = QLabel("Github: https://github.com/yourusername/character2relation")
        
        # 检查更新按钮
        self.check_update = QPushButton("检查更新")
        self.check_update.clicked.connect(self.check_for_updates)
        
        # 设置对齐方式
        self.author_label.setAlignment(Qt.AlignLeft)
        self.github_label.setAlignment(Qt.AlignLeft)
        
        # 添加到主布局
        self.main_layout.addWidget(self.author_label)
        self.main_layout.addWidget(self.github_label)
        self.main_layout.addWidget(self.check_update)
        
        self.setLayout(self.main_layout)
    
    def check_for_updates(self):
        """检查软件更新"""
        # 打开Github链接
        QDesktopServices.openUrl(QUrl("https://github.com/yourusername/character2relation"))