"""
关系图界面模块

功能：
1. 显示角色关系画布
2. 处理角色拖拽和关系线创建
3. 管理角色模块的显示和交互
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor

class RelationGraphTab(QWidget):
    """关系图标签页类"""
    def __init__(self):
        super().__init__()
        
        # 主布局
        self.main_layout = QHBoxLayout()
        
        # 左侧设定框
        self.setup_panel = QListWidget()
        self.setup_panel.setFixedWidth(200)
        
        # 右侧关系图画布
        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        
        # 添加到主布局
        self.main_layout.addWidget(self.setup_panel)
        self.main_layout.addWidget(self.canvas)
        
        self.setLayout(self.main_layout)
        
        # 初始化关系线属性
        self.current_line = None
        self.start_item = None
        
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.modifiers() == Qt.AltModifier:
            # 当按下ALT键时，开始创建关系线
            item = self.scene.itemAt(self.canvas.mapToScene(event.pos()), self.canvas.transform())
            if item:
                self.start_item = item
                self.current_line = self.scene.addLine(
                    QPointF(item.scenePos().x() + item.boundingRect().width()/2, 
                            item.scenePos().y() + item.boundingRect().height()/2),
                    QPointF(event.pos().x(), event.pos().y()),
                    QPen(QColor("black"))
                )
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if self.current_line:
            # 更新关系线终点位置
            line = self.current_line.line()
            self.current_line.setLine(
                line.x1(), line.y1(),
                event.pos().x(), event.pos().y()
            )
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if self.current_line and event.modifiers() == Qt.AltModifier:
            # 当释放ALT键时，完成关系线创建
            end_item = self.scene.itemAt(self.canvas.mapToScene(event.pos()), self.canvas.transform())
            if end_item and end_item != self.start_item:
                # 创建从start_item到end_item的关系线
                self.scene.removeItem(self.current_line)
                self.scene.addLine(
                    QPointF(self.start_item.scenePos().x() + self.start_item.boundingRect().width()/2, 
                            self.start_item.scenePos().y() + self.start_item.boundingRect().height()/2),
                    QPointF(end_item.scenePos().x() + end_item.boundingRect().width()/2, 
                            end_item.scenePos().y() + end_item.boundingRect().height()/2),
                    QPen(QColor("black"))
                )
            else:
                self.scene.removeItem(self.current_line)
            self.current_line = None
            self.start_item = None
        super().mouseReleaseEvent(event)