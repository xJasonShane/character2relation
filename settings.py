"""
设定界面模块

功能：
1. 添加新角色
2. 删除已有角色
3. 管理角色列表
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QHBoxLayout

class SettingsTab(QWidget):
    """设定标签页类"""
    def __init__(self):
        super().__init__()
        
        # 主布局
        self.main_layout = QVBoxLayout()
        
        # 角色列表
        self.character_list = QListWidget()
        
        # 添加角色控件
        self.add_panel = QWidget()
        self.add_layout = QHBoxLayout()
        
        self.character_input = QLineEdit()
        self.character_input.setPlaceholderText("输入角色名称")
        
        self.add_button = QPushButton("添加")
        self.add_button.clicked.connect(self.add_character)
        
        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(self.delete_character)
        
        self.add_layout.addWidget(self.character_input)
        self.add_layout.addWidget(self.add_button)
        self.add_layout.addWidget(self.delete_button)
        self.add_panel.setLayout(self.add_layout)
        
        # 添加到主布局
        self.main_layout.addWidget(self.character_list)
        self.main_layout.addWidget(self.add_panel)
        
        self.setLayout(self.main_layout)
    
    def add_character(self):
        """添加新角色到列表"""
        character_name = self.character_input.text().strip()
        if character_name:
            self.character_list.addItem(character_name)
            self.character_input.clear()
    
    def delete_character(self):
        """从列表中删除选中的角色"""
        current_item = self.character_list.currentItem()
        if current_item:
            self.character_list.takeItem(self.character_list.row(current_item))