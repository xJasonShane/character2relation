"""
关系图界面模块

功能：
1. 显示角色关系画布
2. 处理角色拖拽和关系线创建
3. 管理角色模块的显示和交互
"""
import json
import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QGraphicsView, QGraphicsScene, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor, QDrag
from PyQt5.QtCore import QMimeData

class RelationGraphTab(QWidget):
    """关系图标签页类"""
    def __init__(self):
        super().__init__()
        
        # 主布局
        self.main_layout = QHBoxLayout()
        
        # 左侧设定框
        self.setup_panel = QListWidget()
        self.setup_panel.setFixedWidth(200)
        self.setup_panel.setDragEnabled(True)
        self.setup_panel.setAcceptDrops(True)
        self.setup_panel.setDragDropMode(QListWidget.DragOnly)
        
        # 右侧关系图画布
        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.canvas.setAcceptDrops(True)
        
        # 添加到主布局
        self.main_layout.addWidget(self.setup_panel)
        self.main_layout.addWidget(self.canvas)
        
        self.setLayout(self.main_layout)
        
        # 初始化角色列表
        self.character_items = []
        
        # 拖拽相关属性
        self.drag_start_position = None
        self.dragged_item = None
    
    def update_character_list(self, characters):
        """更新角色列表"""
        self.setup_panel.clear()
        for character in characters:
            self.setup_panel.addItem(character)
        
        # 初始化关系线属性
        self.current_line = None
        self.start_item = None
        
        # 清空画布上的角色项
        for item in self.character_items:
            self.scene.removeItem(item)
        self.character_items = []
        
    def save_relations(self):
        """保存关系图状态到JSON文件"""
        relations = []
        for item in self.scene.items():
            if isinstance(item, QGraphicsLineItem):
                relations.append({
                    "start": {"x": item.line().x1(), "y": item.line().y1()},
                    "end": {"x": item.line().x2(), "y": item.line().y2()}
                })
        
        with open('data.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data["relations"] = relations
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    def load_relations(self):
        """从JSON文件加载关系图状态"""
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for relation in data.get('relations', []):
                    self.scene.addLine(
                        relation["start"]["x"], relation["start"]["y"],
                        relation["end"]["x"], relation["end"]["y"],
                        QPen(QColor("black"))
                    )
        
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
        
    def dragEnterEvent(self, event):
        """处理拖拽进入事件"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        
    def dropEvent(self, event):
        """处理拖放事件"""
        if event.mimeData().hasText():
            character_name = event.mimeData().text()
            pos = self.canvas.mapToScene(event.pos())
            
            # 创建角色矩形项
            rect_item = self.scene.addRect(0, 0, 100, 50, QPen(Qt.black), QColor("lightblue"))
            rect_item.setPos(pos.x() - 50, pos.y() - 25)
            rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            
            # 添加角色名称文本
            text_item = self.scene.addText(character_name)
            text_item.setPos(pos.x() - text_item.boundingRect().width()/2, 
                            pos.y() - text_item.boundingRect().height()/2)
            text_item.setParentItem(rect_item)
            
            # 保存角色项
            self.character_items.append(rect_item)
            self.character_items.append(text_item)
            
            # 强制视图更新
            self.scene.update()
            self.canvas.viewport().update()
            
            event.acceptProposedAction()
        
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton and self.setup_panel.currentItem():
            # 开始拖拽
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.setup_panel.currentItem().text())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction)
            
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