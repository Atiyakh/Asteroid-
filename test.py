from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Viewport-Centered Watermark Example")
        self.resize(800, 600)

        # Create a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create content for the scroll area
        content = QWidget()
        layout = QVBoxLayout(content)
        for i in range(100):
            label = QLabel(f"Scrollable Content Line {i}")
            layout.addWidget(label)
        scroll_area.setWidget(content)

        # Overlay watermark
        watermark_label = QLabel(scroll_area.viewport())
        watermark_pixmap = QPixmap(r"D:\attya-plus\projects\AstroCode\static\colored_icon.png")  # Replace with your image path
        watermark_label.setPixmap(watermark_pixmap)
        watermark_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        watermark_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Allow interaction with scroll area

        # Position the watermark in the center of the viewport
        watermark_label.setGeometry(
            (scroll_area.viewport().width() - watermark_pixmap.width()) // 2,
            (scroll_area.viewport().height() - watermark_pixmap.height()) // 2,
            watermark_pixmap.width(),
            watermark_pixmap.height(),
        )

        # Handle resizing of the scroll area to reposition the watermark
        scroll_area.viewport().resizeEvent = lambda event: self.reposition_watermark(
            watermark_label, scroll_area, watermark_pixmap
        )

        self.setCentralWidget(scroll_area)

    def reposition_watermark(self, watermark_label, scroll_area, watermark_pixmap):
        # Reposition the watermark to remain centered
        watermark_label.setGeometry(
            (scroll_area.viewport().width() - watermark_pixmap.width()) // 2,
            (scroll_area.viewport().height() - watermark_pixmap.height()) // 2,
            watermark_pixmap.width(),
            watermark_pixmap.height(),
        )

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
