"""
导出SVG模块

功能：
1. 将关系图画布导出为SVG矢量格式
"""
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtGui import QPainter

class ExportSVG:
    """SVG导出类"""
    def __init__(self, scene):
        self.scene = scene
    
    def export(self):
        """导出关系图为SVG"""
        # 获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            None, "导出SVG", "", "SVG (*.svg)")
        
        if file_path:
            # 创建QSvgGenerator对象
            svg_gen = QSvgGenerator()
            svg_gen.setFileName(file_path)
            svg_gen.setSize(self.scene.sceneRect().size().toSize())
            
            # 创建QPainter对象
            painter = QPainter(svg_gen)
            self.scene.render(painter)
            painter.end()