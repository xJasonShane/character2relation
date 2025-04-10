"""
导出图片模块

功能：
1. 将关系图画布导出为图片格式
2. 支持多种图片格式（PNG、JPG等）
"""
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPainter

class ExportImage:
    """图片导出类"""
    def __init__(self, scene):
        self.scene = scene
    
    def export(self):
        """导出关系图为图片"""
        # 获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            None, "导出图片", "", "PNG (*.png);;JPEG (*.jpg *.jpeg)")
        
        if file_path:
            # 创建QImage对象
            image = QImage(self.scene.sceneRect().size().toSize(), 
                          QImage.Format_ARGB32)
            image.fill(Qt.white)
            
            # 创建QPainter对象
            painter = QPainter(image)
            self.scene.render(painter)
            painter.end()
            
            # 保存图片
            image.save(file_path)