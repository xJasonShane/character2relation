"""
导出PDF模块

功能：
1. 将关系图画布导出为PDF格式
"""
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPdfWriter, QPainter

class ExportPDF:
    """PDF导出类"""
    def __init__(self, scene):
        self.scene = scene
    
    def export(self):
        """导出关系图为PDF"""
        # 获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            None, "导出PDF", "", "PDF (*.pdf)")
        
        if file_path:
            # 创建QPdfWriter对象
            pdf_writer = QPdfWriter(file_path)
            pdf_writer.setPageSizeMM(self.scene.sceneRect().size() / 3.78)  # 转换为毫米
            
            # 创建QPainter对象
            painter = QPainter(pdf_writer)
            self.scene.render(painter)
            painter.end()