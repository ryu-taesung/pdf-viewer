import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QGraphicsView,
                               QGraphicsScene, QLabel, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy, QCheckBox)
from PySide6.QtGui import QImage, QPixmap, QBrush, QColor, QPalette
from PySide6.QtCore import Qt
import fitz  # PyMuPDF


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.resize(800, 600)

        self.graphics_view = QGraphicsView()
        self.graphics_view.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # Set the background color to black
        self.graphics_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.graphics_scene = QGraphicsScene()

        self.page_label = QLabel("Page:")
        self.page_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.page_edit = QLineEdit("1")
        self.page_edit.setFixedWidth(50)
        self.page_edit.editingFinished.connect(self.page_edit_changed)
        self.total_pages_label = QLabel()

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)

        pages_layout = QHBoxLayout()
        pages_layout.addWidget(self.page_label)
        pages_layout.addWidget(self.page_edit)
        pages_layout.addWidget(self.total_pages_label)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(pages_layout)
        main_layout.addWidget(self.graphics_view)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.next_button)
        
        self.invert_colors_checkbox = QCheckBox("Invert Colors")
        self.invert_colors_checkbox.stateChanged.connect(self.invert_colors_toggled)
        controls_layout.addWidget(self.invert_colors_checkbox)

        main_layout.addLayout(controls_layout)

        self.setCentralWidget(central_widget)

        self.open_pdf_action = self.menuBar().addAction("Open PDF")
        self.open_pdf_action.triggered.connect(self.open_pdf)

        self.doc = None
        self.current_page = 0

    def open_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)", options=options)

        if file_name:
            self.load_pdf(file_name)

    def load_pdf(self, file_name):
        self.doc = fitz.open(file_name)
        self.total_pages_label.setText(f"of {self.doc.page_count}")
        self.show_page(self.current_page)

    def show_page(self, page_number):
        if self.doc is None or page_number < 0 or page_number >= self.doc.page_count:
            return

        self.graphics_scene.clear()
        pdf_page = self.doc.load_page(page_number)
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        image = QImage.fromData(pdf_page.get_pixmap(matrix=mat).tobytes(), "PNG")

        # Invert colors if the checkbox is checked
        if self.invert_colors_checkbox.isChecked():
            for x in range(image.width()):
                for y in range(image.height()):
                    color = QColor(image.pixel(x, y))
                    inverted_color = QColor.fromRgb(~color.rgb() & 0xFFFFFF)
                    image.setPixelColor(x, y, inverted_color)

        pixmap = QPixmap.fromImage(image)
        self.graphics_scene.addPixmap(pixmap)
        self.graphics_view.setScene(self.graphics_scene)
        self.page_edit.setText(str(page_number + 1))
        self.current_page = page_number


    def prev_page(self):
        self.show_page(self.current_page - 1)

    def next_page(self):
        self.show_page(self.current_page + 1)

    def page_edit_changed(self):
        try:
            page_number = int(self.page_edit.text()) - 1
            self.show_page(page_number)
        except ValueError:
            # Reset the page_edit to the current page number in case of invalid input
            self.page_edit.setText(str(self.current_page + 1))

    def invert_colors_toggled(self, state):
      self.show_page(self.current_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #dark them from: https://stackoverflow.com/a/56851493
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())
