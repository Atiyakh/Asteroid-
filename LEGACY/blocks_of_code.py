from traceback import print_exc
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, math

SUPER_GLOBAL_SCALE_VAR = dict()

arg_font = QFont('Arial',9)

arg_font_italic = QFont('Arial',9)
arg_font_italic.setItalic(True)

def customCircleArguments(ending_point, layout_length, starting_angle, span_angle, p=0):
    radius = layout_length / 2
    h_co = math.sin(starting_angle * (math.pi / 180)) * radius
    w_co = math.cos(starting_angle * (math.pi / 180)) * radius
    y_starting_point = ending_point.y() - (radius - h_co)
    x_starting_point = ending_point.x() - (radius + w_co)
    return int(x_starting_point + p), int(y_starting_point), layout_length, layout_length, starting_angle, span_angle

def drawCircularShape(painter:QPainter, x, pen_resize=False, color=None, p=0, shape_width=4, handle_length=3, x_=0):
    point = QPoint(9 + p, x)
    path = QPainterPath(point)
    path.lineTo(point + QPoint(handle_length, handle_length))
    path.arcTo(*customCircleArguments(path.currentPosition(), 5, -135, 45, p=0))
    path.lineTo(path.currentPosition() + QPoint(shape_width, 0))
    path.arcTo(*customCircleArguments(path.currentPosition(), 5, 270, 45, p=5))
    path.lineTo((path.currentPosition().x() + (handle_length - 1 + x_)), x)
    if pen_resize:
        painter.setPen(QPen(color, pen_resize, Qt.SolidLine))
        painter.drawPath(path)
        painter.setPen(QPen(color, 4, Qt.SolidLine))
    else:
        painter.drawPath(path)

class QArgumentEdit(QLineEdit):
    def childResizeEvent(self):
        self.setFixedWidth(self.child.width() - 2)
        self.parentWidget().parentWidget().adjust_size()

    def take_child(self, child:QWidget):
        self.child = child
        self.setText('')
        self.pre_height = child.height()
        child.setFixedHeight(33)
        child.parent_arg = self
        child.is_arg = True
        self.pre_color = child.color
        child.color = QColor(*((i - 20 if i > 0 else 0) for i in self.parent_block.color.getRgb()[:-1]))
        child.body_block.setStyleSheet(f"background-color: rgb{child.color.getRgb()[:-1]}; color: #fff; border-radius: 3px; padding: 0px;")
        self.setFixedWidth(child.width() - 2)
        self.parentWidget().parentWidget().adjust_size()
        self.setDisabled(True)
    
    def remove_child(self):
        if self.child:
            self.child.is_arg = False
            self.child.setFixedHeight(self.pre_height)
            self.child.parent_arg = None
            self.child.color = self.pre_color
            self.child.body_block.setStyleSheet(f"background-color: rgb{self.child.color.getRgb()[:-1]}; color: #fff; border-radius: 3px; padding: 0px;")
            self.child = None
            self.setDisabled(False)
            self.custom_event(None)

    def enterPressedEvent(self):
        try:
            args = list(self.all_args.values())
            args[args.index(self)+1].setFocus()
        except: pass

    def __init__(self):
        super().__init__()
        self.child = None
        self.pre_color = None
        self.parent_block = None
        self.all_args = []
        self.testing_label = QLabel()
        self.setFixedHeight(17)
        self.setStyleSheet("border-radius: 8px; color: #444; background-color: #fff; font-size: 14px; font-family: Helvetica; padding-left: 3px; padding-right: 3px;")
        self.testing_label.setStyleSheet(self.styleSheet())
        self.minimum_width = 28
        self.maximum_width = 220
        self.setFixedWidth(self.minimum_width)
        self.textChanged.connect(self.custom_event)
        self.returnPressed.connect(self.enterPressedEvent)

    def custom_event(self, _):
        self.testing_label.setText(self.text())
        self.testing_label.adjustSize()
        w = self.testing_label.width()
        if w > self.minimum_width:
            if w < self.maximum_width:
                self.setFixedWidth(w)
            else: self.setFixedWidth(self.maximum_width) 
        else: self.setFixedWidth(self.minimum_width)
        self.parentWidget().parentWidget().adjust_size()

    def childResizedEvent(self):
        self.setFixedWidth(self.child.width())

def processArgumentTag(arg_tag, arg_label:QLabel, arg_input:QArgumentEdit, body_layout:QHBoxLayout):
    font = QFont('Arial', 9)
    # font config
    if 'italic' in arg_tag: font.setItalic(True)
    if 'bold' in arg_tag: font.setBold(True)
    if 'underline' in arg_tag: font.setUnderline(True)
    # render argument widgets
    arg_label.setFont(font)
    if 'inverse' in arg_tag:
        body_layout.addWidget(arg_input)
        body_layout.addWidget(arg_label)
    else:
        body_layout.addWidget(arg_label)
        body_layout.addWidget(arg_input)

class QContainerHoldingStick(QLabel):
    def __init__(self, blockspace, parent_container:QWidget):
        self.parent_container = parent_container
        self.blockspace = blockspace
        super().__init__(blockspace)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"background-color: rgb{parent_container.color.getRgb()[:-1]}; border-radius: 2px;")
        self.setFixedWidth(9)
        self.setFixedHeight(50)
        self.mousePressEvent = parent_container.mousePressEvent
        self.mouseReleaseEvent = parent_container.mouseReleaseEvent

    def mouseMoveEvent(self, event):
        self.parent_container.mouseMoveEvent(event, evoker=self)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Qt.black, 0.2, Qt.SolidLine))
        painter.drawLine(QPoint(1, 2), QPoint(1, self.height()))
        painter.drawLine(QPoint(self.width() - 1, 2), QPoint(self.width() - 1, self.height()))

class QContainerClosingStick(QWidget):
    def __init__(self, blockspace, parent_container:QWidget):
        self.parent_container = parent_container
        self.color = parent_container.color
        self.blockspace = blockspace
        super().__init__(blockspace)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedWidth(parent_container.width())
        self.setFixedHeight(24)
        self.mousePressEvent = parent_container.mousePressEvent
        self.mouseReleaseEvent = parent_container.mouseReleaseEvent

    def mouseMoveEvent(self, event):
        self.parent_container.mouseMoveEvent(event, evoker=self)

    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.SolidLine))
        # rect 1
        rect_1 = QRect(QPoint(2, 2), QPoint(16, 15))
        painter.drawRoundedRect(rect_1, 2, 2)
        painter.fillRect(rect_1, self.color)
        # rect 2
        rect_2 = QRect(QPoint(37, 2), QPoint(self.width() - 5, 15))
        painter.drawRoundedRect(rect_2, 2, 2)
        painter.fillRect(rect_2, self.color)
        # rect 3
        rect_3 = QRect(QPoint(15, 8), QPoint(38, 17))
        painter.fillRect(rect_3, self.color)
        # circular shapes
        drawCircularShape(painter, 5, p=9)
        drawCircularShape(painter, 12, shape_width=0, handle_length=6, p=-1)
        drawCircularShape(painter, 16, shape_width=0, handle_length=6, p=-1)
        drawCircularShape(painter, 13, shape_width=0, handle_length=6, p=-1)
        # border:
        path = QPainterPath(QPoint(9, 1))
        path.lineTo(QPoint(16, 1))
        path.moveTo(38, 1)
        path.lineTo(QPoint(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPoint(self.width() - 3, 16))
        path.moveTo(30, 17)
        path.lineTo(QPoint(self.width() - 4, 17))
        path.moveTo(1, 2)
        path.lineTo(QPoint(1, 16))
        path.moveTo(2, 17)
        path.lineTo(QPoint(7, 17))
        # circular shapes:
        painter.setPen(QPen(Qt.black, 0.2, Qt.SolidLine))
        drawCircularShape(painter, 2, shape_width=1, x_=0, handle_length=5, p=9)
        drawCircularShape(painter, 18, shape_width=1, x_=0, handle_length=5)
        # draw path
        painter.drawPath(path)

class QDContainerBlock(QWidget):
    def __init__(self, function_name:str, args_dict:dict, color:QColor, parent:QWidget):
        self.body_padding_left = 5
        self.is_inside_container = False
        self.body_block_height = 33
        self.block_container = None
        self.child_inside = None
        self.parent_container = None
        self.is_double = False
        self.d_container = None
        self.parent_block = None
        self.parent_arg = None
        self.child = None
        super().__init__(parent)
        self.blockarea = parent
        self.color = color
        self.args_dict = args_dict
        self.args = dict()
        self.function_name = function_name
        self.body_block = QWidget(self)
        self.body_layout = QHBoxLayout(self.body_block)
        self.body_layout.setContentsMargins(0,0,0,0)
        self.body_block.move(self.body_padding_left, 7)
        self.body_block.setFixedHeight(24)
        self.body_block.setStyleSheet(f"background-color: rgb{self.color.getRgb()[:-1]}; color: #fff; border-radius: 3px; padding: 0px;")
        self.holding_stick = QContainerHoldingStick(parent, self)
        self.closing_stick = QContainerClosingStick(parent, self)
        self.closing_stick.blockarea = self.blockarea
        self.holding_stick.blockarea = self.blockarea
        self.setCursor(Qt.PointingHandCursor)
        self.raise_()
        self.insert_elements()
        self.adjust_size()
    
    def check_child_total_height(self):
        if self.child_inside:
            self.holding_stick.setFixedHeight(
                self.child_inside.get_total_height() + 33
            )
        else:
            self.holding_stick.setFixedHeight(50)
        self.closing_stick.move(self.x(), self.y() + self.holding_stick.height())

    def adjust_size(self, partial_adjustments_=False):
        self.check_child_total_height()
        self.body_block.adjustSize()
        width = self.body_block.width()
        self.setFixedSize(width + 14, 39)
        if not partial_adjustments_:
            if self.parent_container:
                self.parent_container.adjust_size(partial_adjustments_=True)
                if self.parent_container.width() > self.width():
                    self.setFixedWidth(self.parent_container.width())
                else:
                    self.parent_container.setFixedWidth(self.width())
        if self.block_container:
            self.block_container.adjust_size()

    def insert_elements(self):
        if self.function_name:
            self.function_name_label = QLabel(self.function_name)
            self.function_name_label.setFont(arg_font)
            self.body_layout.addWidget(self.function_name_label)
        for arg_name, arg_tag in self.args_dict.items():
            if arg_name: arg_label = QLabel(arg_name)
            arg_input = QArgumentEdit()
            arg_input.parent_block = self
            arg_input.all_args = self.args
            self.args[arg_name] = arg_input
            if arg_name:
                processArgumentTag(arg_tag, arg_label, arg_input, self.body_layout)
            else:
                self.body_layout.addWidget(arg_input)
    
    def get_total_height(self):
        return self.holding_stick.height() + 18
    
    def take_child(self, child):
        self.child = child
        child.block_container = self.block_container
        child.parent_block = self
        if self.block_container:
            self.block_container.adjust_size()

    def take_child_inside(self, child_inside):
        self.child_inside = child_inside
        child_inside.block_container = self
        child_inside.is_inside_container = True
        self.adjust_size()
        if self.block_container:
            self.block_container.adjust_size()
    
    def remove_child(self):
        if self.child:
            self.child.parent_block = None
            self.child = None
    
    def move_args(self):
        for arg in self.args.values():
            if arg.child:
                arg.child.raise_()
                arg.child.move(self.x() + arg.x() + 5, self.y())

    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.SolidLine))
        # rect 1
        rect_1 = QRect(QPoint(2, 2), QPoint(16, 30))
        painter.drawRoundedRect(rect_1, 2, 2)
        painter.fillRect(rect_1, self.color)
        # rect 2
        rect_2 = QRect(QPoint(37, 2), QPoint(self.width() - 5, 30))
        painter.drawRoundedRect(rect_2, 2, 2)
        painter.fillRect(rect_2, self.color)
        # rect 3
        rect_3 = QRect(QPoint(2, 30), QPoint(40, 30))
        painter.drawRoundedRect(rect_3, 2, 2)
        painter.fillRect(rect_3, self.color)
        # circular shapes
        drawCircularShape(painter, 5, p=9)
        drawCircularShape(painter, 27, shape_width=0, handle_length=6, p=8)
        drawCircularShape(painter, 31, shape_width=0, handle_length=6, p=8)
        drawCircularShape(painter, 28, shape_width=0, handle_length=6, p=8)
        # border:
        path = QPainterPath(QPoint(9, 1))
        path.lineTo(QPoint(17, 1))
        path.moveTo(38, 1)
        path.lineTo(QPoint(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPoint(self.width() - 3, 31))
        path.moveTo(38, 32)
        path.lineTo(QPoint(self.width() - 4, 32))
        path.moveTo(1, 2)
        path.lineTo(QPoint(1, 32))
        path.moveTo(9, 32)
        path.lineTo(QPoint(16, 32))
        # circular shapes:
        painter.setPen(QPen(Qt.black, 0.2, Qt.SolidLine))
        drawCircularShape(painter, 2, shape_width=1, x_=0, handle_length=5, p=9)
        drawCircularShape(painter, 33, shape_width=1, x_=0, handle_length=5, p=9)
        # draw path
        painter.drawPath(path)
    
    def mouseReleaseEvent(self, _):
        self.blockarea.adjust_size()

    def moveEvent(self, _):
        self.holding_stick.raise_()
        self.closing_stick.raise_()
        self.raise_()
        self.holding_stick.move(self.x(), self.y() + 5)
        self.closing_stick.move(self.x(), self.y() + self.holding_stick.height())
        if self.child:
            self.child.parentMoveEvent(self.x(), self.closing_stick.y() - 15)
        if self.child_inside:
            self.child_inside.move(self.x() + 9, self.y() + 33)
        self.move_args()
    
    def parentMoveEvent(self, x, y):
        self.raise_()
        self.move(x, y + self.body_block_height)
    
    def resizeEvent(self, _):
        self.closing_stick.setFixedWidth(self.width())
        if self.parent_arg:
            self.parent_arg.childResizeEvent()

class QContainerBlock(QWidget):
    def __init__(self, function_name:str, args_dict:dict, color:QColor, parent:QWidget):
        self.body_padding_left = 5
        self.is_inside_container = False
        self.body_block_height = 33
        self.copied = False
        self.block_container = None
        self.child_inside = None
        self.is_double = False
        self.d_container = None
        self.parent_block = None
        self.parent_arg = None
        self.child = None
        super().__init__(parent)
        self.blockarea = parent
        self.color = color
        self.args_dict = args_dict
        self.args = dict()
        self.function_name = function_name
        self.body_block = QWidget(self)
        self.body_layout = QHBoxLayout(self.body_block)
        self.body_layout.setContentsMargins(0,0,0,0)
        self.body_block.move(self.body_padding_left, 7)
        self.body_block.setFixedHeight(24)
        self.body_block.setStyleSheet(f"background-color: rgb{self.color.getRgb()[:-1]}; color: #fff; border-radius: 3px; padding: 0px;")
        self.holding_stick = QContainerHoldingStick(parent, self)
        self.closing_stick = QContainerClosingStick(parent, self)
        self.closing_stick.blockarea = self.blockarea
        self.holding_stick.blockarea = self.blockarea
        self.setCursor(Qt.PointingHandCursor)
        self.raise_()
        self.insert_elements()
        self.adjust_size()
    
    def check_child_total_height(self):
        if self.child_inside:
            self.holding_stick.setFixedHeight(
                self.child_inside.get_total_height() + 33
            )
        else:
            self.holding_stick.setFixedHeight(50)
        self.closing_stick.move(self.x(), self.y() + self.holding_stick.height())

    def set_double_container(self, d_container):
        self.is_double = True
        self.d_container = d_container
        self.closing_stick.hide()
        d_container.parent_container = self
        for widget in d_container, d_container.holding_stick, d_container.closing_stick:
            widget.mousePressEvent = self.mousePressEvent
            widget.mouseMoveEvent = self.mouseMoveEvent
        self.adjust_size()

    def get_total_height(self):
        return self.holding_stick.height() + (18 if not self.is_double else 0) + (self.d_container.get_total_height() if self.is_double else 0) + (self.child.get_total_height() if self.child else 0)

    def adjust_size(self, partial_adjustments_=False):
        self.check_child_total_height()
        self.body_block.adjustSize()
        width = self.body_block.width()
        self.setFixedSize(width + 14, 39)
        if not partial_adjustments_:
            if self.d_container:
                self.d_container.adjust_size(partial_adjustments_=True)
                if self.d_container.width() > self.width():
                    self.setFixedWidth(self.d_container.width())
                else:
                    self.d_container.setFixedWidth(self.width())
        if self.block_container:
            self.block_container.adjust_size()

    def insert_elements(self):
        if self.function_name:
            self.function_name_label = QLabel(self.function_name)
            self.function_name_label.setFont(arg_font)
            self.body_layout.addWidget(self.function_name_label)
        for arg_name, arg_tag in self.args_dict.items():
            if arg_name: arg_label = QLabel(arg_name)
            arg_input = QArgumentEdit()
            arg_input.parent_block = self
            arg_input.all_args = self.args
            self.args[arg_name] = arg_input
            if arg_name:
                processArgumentTag(arg_tag, arg_label, arg_input, self.body_layout)
            else:
                self.body_layout.addWidget(arg_input)

    def take_child(self, child):
        self.child = child
        child.block_container = self.block_container
        child.parent_block = self
        if self.block_container:
            self.block_container.adjust_size()
    
    def take_child_inside(self, child_inside):
        self.child_inside = child_inside
        child_inside.block_container = self
        child_inside.is_inside_container = True
        self.adjust_size()
        if self.block_container:
            self.block_container.adjust_size()
    
    def remove_child(self):
        if self.child:
            self.child.parent_block = None
            self.child = None
    
    def move_args(self):
        for arg in self.args.values():
            if arg.child:
                arg.child.raise_()
                arg.child.move(self.x() + arg.x() + 5, self.y())

    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.SolidLine))
        # rect 1
        rect_1 = QRect(QPoint(2, 2), QPoint(7, 30))
        painter.drawRoundedRect(rect_1, 2, 2)
        painter.fillRect(rect_1, self.color)
        # rect 2
        rect_2 = QRect(QPoint(28, 2), QPoint(self.width() - 5, 30))
        painter.drawRoundedRect(rect_2, 2, 2)
        painter.fillRect(rect_2, self.color)
        # rect 3
        rect_3 = QRect(QPoint(2, 30), QPoint(40, 30))
        painter.drawRoundedRect(rect_3, 2, 2)
        painter.fillRect(rect_3, self.color)
        # circular shapes
        drawCircularShape(painter, 5)
        drawCircularShape(painter, 27, shape_width=0, handle_length=6, p=8)
        drawCircularShape(painter, 31, shape_width=0, handle_length=6, p=8)
        drawCircularShape(painter, 28, shape_width=0, handle_length=6, p=8)
        # border:
        path = QPainterPath(QPoint(2, 1))
        path.lineTo(QPoint(7, 1))
        path.moveTo(29, 1)
        path.lineTo(QPoint(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPoint(self.width() - 3, 31))
        path.moveTo(38, 32)
        path.lineTo(QPoint(self.width() - 4, 32))
        path.moveTo(1, 2)
        path.lineTo(QPoint(1, 32))
        path.moveTo(9, 32)
        path.lineTo(QPoint(16, 32))
        # circular shapes:
        painter.setPen(QPen(Qt.black, 0.2, Qt.SolidLine))
        drawCircularShape(painter, 2, shape_width=1, x_=0, handle_length=5)
        drawCircularShape(painter, 33, shape_width=1, x_=0, handle_length=5, p=9)
        # draw path
        painter.drawPath(path)
    
    def mouseReleaseEvent(self, _):
        try: self.blockarea.adjust_size()
        except: print_exc()

    def mousePressEvent(self, event):
        try:
            self.holding_stick.raise_()
            self.closing_stick.raise_()
            if self.is_double: self.d_container.raise_()
            self.raise_()
            self.oldPosition = event.globalPos()
            for arg in self.args.values():
                if arg.child:
                    arg.child.parentArgumentPressEvent()
        except: print_exc()

    def make_copy(self):
        container = QContainerBlock(self.function_name, self.args_dict, self.color, self.blockarea)
        container.move(0, 0)
        container.closing_stick.move(0, 0)
        container.holding_stick.move(0, 0)
        container.holding_stick.show()
        container.closing_stick.show()
        container.show()

    def mouseMoveEvent(self, event, evoker=None):
        print(evoker)
        if not self.copied:
            self.copied = True
            self.make_copy()
            new_parent = SUPER_GLOBAL_SCALE_VAR['super-main-window']
            if evoker == self.closing_stick:
                point = new_parent.pos() + QPoint(event.x(), event.y() + 38 + self.holding_stick.height())
            else: point = new_parent.pos() + QPoint(event.x(), event.y() + 38)
            self.setParent(new_parent)
            self.closing_stick.setParent(new_parent)
            self.holding_stick.setParent(new_parent)
            self.move(event.globalPos() - point)
        try:
            self.show()
            self.closing_stick.show()
            self.holding_stick.show()
            delta = QPoint(event.globalPos() - self.oldPosition)
            if not evoker or self.copied: self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except: print_exc()

    def moveEvent(self, _):
        self.holding_stick.raise_()
        self.closing_stick.raise_()
        self.raise_()
        self.holding_stick.move(self.x(), self.y() + 5)
        if self.is_double:
            self.d_container.move(self.x(), self.y() + self.holding_stick.height())
            self.d_container.raise_()
        else:
            self.closing_stick.move(self.x(), self.y() + self.holding_stick.height())
        if self.child:
            self.child.parentMoveEvent(self.x(), self.closing_stick.y() - 15)
        if self.child_inside:
            self.child_inside.move(self.x() + 9, self.y() + 33)
        self.move_args()
    
    def parentMoveEvent(self, x, y):
        self.raise_()
        self.move(x, y + self.body_block_height)
    
    def resizeEvent(self, _):
        self.closing_stick.setFixedWidth(self.width())
        if self.parent_arg:
            self.parent_arg.childResizeEvent()

class QCallFunctionBlock(QWidget):
    def __init__(self, function_name:str, args_dict:dict, color:QColor, parent:QWidget, always_arg=False):
        self.body_padding_left = 5
        self.body_block_height = 33
        self.block_container = None
        self.parent_block = None
        self.is_arg = False
        self.is_always_arg = False
        self.copied = False
        self.parent_arg = None
        self.is_inside_container = False
        self.child = None
        super().__init__(parent)
        self.color = color
        self.blockarea = parent
        self.args_dict = args_dict
        self.args = dict()
        self.function_name = function_name
        self.body_block = QWidget(self)
        self.body_layout = QHBoxLayout(self.body_block)
        self.body_layout.setContentsMargins(0,0,0,0)
        self.body_block.move(self.body_padding_left, 7)
        self.body_block.setFixedHeight(24)
        self.body_block.setStyleSheet(f"background-color: rgb{self.color.getRgb()[:-1]}; color: #fff; border-radius: 3px; padding: 0px;")
        if always_arg: self.set_always_arg()
        self.setCursor(Qt.PointingHandCursor)
        self.insert_elements()
        self.adjust_size()

    def set_always_arg(self):
        self.is_arg = True
        self.is_always_arg = True

    def adjust_size(self):
        self.body_block.adjustSize()
        width = self.body_block.width()
        self.setFixedSize(width + 14, 39)
        if self.block_container:
            self.block_container.adjust_size()
    
    def get_total_height(self):
        return self.body_block_height + (self.child.get_total_height() if self.child else 0)

    def insert_elements(self):
        if self.function_name:
            self.function_name_label = QLabel(self.function_name)
            self.function_name_label.setFont(arg_font)
            self.body_layout.addWidget(self.function_name_label)
        for arg_name, arg_tag in self.args_dict.items():
            if arg_name: arg_label = QLabel(arg_name)
            arg_input = QArgumentEdit()
            arg_input.parent_block = self
            arg_input.all_args = self.args
            self.args[arg_name] = arg_input
            if arg_name:
                processArgumentTag(arg_tag, arg_label, arg_input, self.body_layout)
            else:
                self.body_layout.addWidget(arg_input)
    
    def take_child(self, child):
        self.child = child
        child.block_container = self.block_container
        child.parent_block = self
        if self.block_container:
            self.block_container.adjust_size()
    
    def remove_child(self):
        if self.child:
            self.child.parent_block = None
            self.child = None
    
    def move_args(self):
        for arg in self.args.values():
            if arg.child:
                arg.child.raise_()
                arg.child.move(self.x() + arg.x() + 5, self.y())
    
    def mouseReleaseEvent(self, _):
        try: self.blockarea.adjust_size()
        except: print("ERR")

    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.SolidLine))
        # rect 1
        if not self.is_arg:
            rect_1 = QRect(QPoint(2, 2), QPoint(7, 30))
        else:
            rect_1 = QRect(QPoint(2, 2), QPoint(30, 30))
        painter.drawRoundedRect(rect_1, 2, 2)
        painter.fillRect(rect_1, self.color)
        # rect 2
        rect_2 = QRect(QPoint(28, 2), QPoint(self.width() - 5, 30))
        painter.drawRoundedRect(rect_2, 2, 2)
        painter.fillRect(rect_2, self.color)
        # circular shapes
        if not self.is_arg:
            drawCircularShape(painter, 5)
            drawCircularShape(painter, 27, shape_width=0, handle_length=6, p=-1)
            drawCircularShape(painter, 31, shape_width=0, handle_length=6, p=-1)
            drawCircularShape(painter, 28, shape_width=0, handle_length=6, p=-1)
        # border:
        path = QPainterPath(QPoint(2, 1))
        if not self.is_arg:
            path.lineTo(QPoint(7, 1))
        else:
            path.lineTo(QPoint(28, 1))
        path.moveTo(29, 1)
        path.lineTo(QPoint(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPoint(self.width() - 3, 31))
        path.moveTo(30, 32)
        path.lineTo(QPoint(self.width() - 4, 32))
        path.moveTo(1, 2)
        path.lineTo(QPoint(1, 31))
        path.moveTo(2, 32)
        if not self.is_arg:
            path.lineTo(QPoint(7, 32))
        else:
            path.lineTo(QPoint(28, 32))
        # circular shapes:
        painter.setPen(QPen(Qt.black, 0.2, Qt.SolidLine))
        if not self.is_arg:
            drawCircularShape(painter, 2, shape_width=1, x_=0, handle_length=5)
            drawCircularShape(painter, 33, shape_width=1, x_=0, handle_length=5)
        # draw path
        painter.drawPath(path)

    def mousePressEvent(self, event):
        try:
            self.raise_()
            self.oldPosition = event.globalPos()
            for arg in self.args.values():
                if arg.child:
                    arg.child.parentArgumentPressEvent()
        except: pass

    def parentArgumentPressEvent(self):
        self.raise_()
        for arg in self.args.values():
            if arg.child:
                arg.child.parentArgumentPressEvent()
    
    def make_copy(self):
        copy = QCallFunctionBlock(self.function_name, self.args_dict, self.color, self.blockarea, self.is_always_arg)
        copy.move(0, 0)
        copy.show()

    def mouseMoveEvent(self, event):
        if not self.copied:
            self.copied = True
            self.make_copy()
            point = SUPER_GLOBAL_SCALE_VAR['super-main-window'].pos() + QPoint(event.x(), event.y() + 38)
            self.setParent(SUPER_GLOBAL_SCALE_VAR['super-main-window'])
            self.move(event.globalPos() - point)
        try:
            self.show()
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except: pass

    def moveEvent(self, _):
        self.raise_()
        if self.child:
            self.child.parentMoveEvent(self.x(), self.y())
        self.move_args()

    def parentMoveEvent(self, x, y):
        self.raise_()
        self.move(x, y + self.body_block_height)

    def resizeEvent(self, _):
        if self.parent_arg:
            self.parent_arg.childResizeEvent()

class QStartingBlock(QWidget):
    def __init__(self, function_name:str, args_dict:dict, color:QColor, parent:QWidget):
        self.body_padding_left = 5
        self.is_inside_container = False
        self.body_block_height = 31
        self.parent_block = None
        self.block_container = None
        self.is_arg = False
        self.parent_arg = None
        self.copied = False
        self.child = None
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.blockarea = parent
        self.color = color
        self.args_dict = args_dict
        self.args = dict()
        self.function_name = function_name
        self.body_block = QWidget(self)
        self.body_layout = QHBoxLayout(self.body_block)
        self.body_layout.setContentsMargins(0,0,0,0)
        self.body_block.move(self.body_padding_left, 7)
        self.body_block.setFixedHeight(24)
        self.body_block.setStyleSheet(f"background-color: rgb{self.color.getRgb()[:-1]}; color: #fff; border-radius: 3px; padding: 0px;")
        self.insert_elements()
        self.adjust_size()

    def adjust_size(self):
        self.body_block.adjustSize()
        width = self.body_block.width()
        self.setFixedSize(width + 14, 39)
        if self.block_container:
            self.block_container.adjust_size()

    def get_total_height(self):
        return self.body_block_height + (self.child.get_total_height() if self.child else 0)

    def insert_elements(self):
        if self.function_name:
            self.function_name_label = QLabel(self.function_name)
            self.function_name_label.setFont(arg_font)
            self.body_layout.addWidget(self.function_name_label)
        for arg_name, arg_tag in self.args_dict.items():
            if arg_name: arg_label = QLabel(arg_name)
            arg_input = QArgumentEdit()
            arg_input.parent_block = self
            arg_input.all_args = self.args
            self.args[arg_name] = arg_input
            if arg_name:
                processArgumentTag(arg_tag, arg_label, arg_input, self.body_layout)
            else:
                self.body_layout.addWidget(arg_input)

    def take_child(self, child):
        self.child = child
        child.block_container = self.block_container
        child.parent_block = self
        if self.block_container:
            self.block_container.adjust_size()

    def remove_child(self):
        if self.child:
            self.child.parent_block = None
            self.child = None

    def move_args(self):
        for arg in self.args.values():
            if arg.child:
                arg.child.raise_()
                arg.child.move(self.x() + arg.x() + 5, self.y())

    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.SolidLine))
        # rect 1
        rect_1 = QRect(QPoint(2, 2), QPoint(30, 30))
        painter.drawRoundedRect(rect_1, 2, 2)
        painter.fillRect(rect_1, self.color)
        # rect 2
        rect_2 = QRect(QPoint(28, 2), QPoint(self.width() - 5, 30))
        painter.drawRoundedRect(rect_2, 2, 2)
        painter.fillRect(rect_2, self.color)
        # circular shapes
        if not self.is_arg:
            drawCircularShape(painter, 28, shape_width=-3, handle_length=6, p=1)
            drawCircularShape(painter, 32, shape_width=-3, handle_length=6, p=1)
            drawCircularShape(painter, 29, shape_width=-3, handle_length=6, p=1)
        # border:
        path = QPainterPath(QPoint(2, 1))
        path.lineTo(QPoint(28, 1))
        path.moveTo(29, 1)
        path.lineTo(QPoint(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPoint(self.width() - 3, 31))
        path.moveTo(30, 32)
        path.lineTo(QPoint(self.width() - 4, 32))
        path.moveTo(1, 2)
        path.lineTo(QPoint(1, 31))
        path.moveTo(2, 32)
        path.lineTo(QPoint(7, 32))
        # circular shapes:
        painter.setPen(QPen(Qt.black, 0.2, Qt.SolidLine))
        drawCircularShape(painter, 34, shape_width=1, x_=0, handle_length=5)
        # draw path
        painter.drawPath(path)
    
    def mouseReleaseEvent(self, _):
        try: self.blockarea.adjust_size()
        except: pass

    def mousePressEvent(self, event):
        try:
            self.raise_()
            self.oldPosition = event.globalPos()
            for arg in self.args.values():
                if arg.child:
                    arg.child.parentArgumentPressEvent()
        except: pass

    def parentArgumentPressEvent(self):
        self.raise_()
        for arg in self.args.values():
            if arg.child:
                arg.child.parentArgumentPressEvent()
    
    def make_copy(self):
        copy = QStartingBlock(self.function_name, self.args_dict, self.color, self.blockarea)
        copy.move(0, 0)
        copy.show()

    def mouseMoveEvent(self, event):
        if not self.copied:
            self.copied = True
            self.make_copy()
            point = SUPER_GLOBAL_SCALE_VAR['super-main-window'].pos() + QPoint(event.x(), event.y() + 38)
            self.setParent(SUPER_GLOBAL_SCALE_VAR['super-main-window'])
            self.move(event.globalPos() - point)
        try:
            self.show()
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except: pass

    def moveEvent(self, _):
        self.raise_()
        if self.child:
            self.child.parentMoveEvent(self.x(), self.y())
        self.move_args()

    def parentMoveEvent(self, x, y):
        self.raise_()
        self.move(x, y + self.body_block_height)

    def resizeEvent(self, _):
        if self.parent_arg:
            self.parent_arg.childResizeEvent()

class QBlockArea(QWidget):
    def adjust_size(self):
        farthest_x, farthest_y = 0, 0
        for x, y in ((child.x() + child.width(), child.y() + child.height()) for child in self.children()):
            if x > farthest_x: farthest_x = x
            if y > farthest_y: farthest_y = y
        farthest_x += 150
        farthest_y += 150
        if self.parent().width() > farthest_x: farthest_x = self.parent().width()
        if self.parent().height() > farthest_y: farthest_y = self.parent().height()
        self.setFixedSize(farthest_x, farthest_y)

    def __init__(self):
        super().__init__()

class block_container_widget(QWidget):
    def showEvent(self, _):
        f_y = 0
        for child in self.children():
            if child.y() + child.height() > f_y: f_y = child.y() + child.height()
        self.setFixedHeight(f_y + 7)

def load_flow_control_blocks(layout:QLayout):
    flow_control_blocks = list()
    color = QColor(227, 139, 2)
    flow_control_blocks.append(QStartingBlock(" when the program starts", {}, color, block_container_widget()))
    flow_control_blocks.append(QCallFunctionBlock(" wait for", {'seconds':'inverse'}, color, block_container_widget()))
    flow_control_blocks.append(QCallFunctionBlock(" do nothing", {}, color, block_container_widget()))
    flow_control_blocks.append(QContainerBlock(" repeat", {'times':'inverse'}, color, block_container_widget()))
    flow_control_blocks.append(QContainerBlock(" loop through", {'':'', 'as': ''}, color, block_container_widget()))
    flow_control_blocks.append(QContainerBlock(" if", {'then':'inverse'}, color, block_container_widget()))
    flow_control_blocks.append(QContainerBlock(" repeat forever", {}, color, block_container_widget()))
    flow_control_blocks.append(QContainerBlock(" repeat until", {'':''}, color, block_container_widget()))
    flow_control_blocks.append(QCallFunctionBlock(" stop repeating", {}, color, block_container_widget()))
    flow_control_blocks.append(QCallFunctionBlock(" skip to next iteration", {}, color, block_container_widget()))
    flow_control_blocks.append(QCallFunctionBlock(" exit program", {}, color, block_container_widget()))
    flow_control_blocks.append(QCallFunctionBlock(" end block", {}, color, block_container_widget()))
    # if - else
    x = block_container_widget()
    if_block = QContainerBlock(" if", {'then':'inverse'}, color, x)
    else_block = QDContainerBlock(" else", {}, color, x)
    if_block.set_double_container(else_block)
    flow_control_blocks.append(if_block)
    # try - except
    x = block_container_widget()
    try_block = QContainerBlock(" try ", {}, color, x)
    except_block = QDContainerBlock(" and if you faild", {}, color, x)
    try_block.set_double_container(except_block)
    flow_control_blocks.append(try_block)
    for flow_control_block in flow_control_blocks:
        layout.addWidget(flow_control_block.parent())

def load_core_operations_blocks(layout:QLayout):
    core_operations_blocks = list()
    color = QColor(117, 8, 224)
    core_operations_blocks.append(QCallFunctionBlock(" display", {'':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" receive text", {'input_hint':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" concatonate", {'':'', 'with':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" slice", {'':'', 'from':'', 'to':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" get", {'':'', 'of':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" in", {'':'', 'replace':'', 'with':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" length of", {'':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" reverse text", {'':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" where", {'in':'inverse', '?':'inverse'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" split", {'':'', 'in':''}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" remove spaces", {'text':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" remove spaces on the right", {'text':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" remove spaces on the left", {'text':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" capitalize", {'text':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" lower", {'text':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" start file interaction", {'file_path':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" read file", {'file_interaction':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" write file", {'data':'italic', 'file_interaction':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" append", {'data':'italic', 'file_interaction':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" close file", {'file_interaction':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" delete file", {'file_path':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" delete folder", {'folder_path':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" create file", {'file_path':'italic'}, color, block_container_widget()))
    core_operations_blocks.append(QCallFunctionBlock(" create folder", {'folder_path':'italic'}, color, block_container_widget()))
    for core_operations_block in core_operations_blocks:
        layout.addWidget(core_operations_block.parent())

def load_vars_blocks(layout:QLayout):
    vars_blocks = list()
    color = QColor(32, 199, 125)
    vars_blocks.append(QCallFunctionBlock(" set", {'':'', 'to equal':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" type of", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" to text", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" to integer", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" to floating point number", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" to boolean", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" change the variable", {'':'', 'by':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" multiply the variable", {'':'', 'with':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" devide the variable", {'':'', 'by':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" raise the variable", {'':'', 'to the power of':''}, color, block_container_widget()))
    for vars_block in vars_blocks:
        layout.addWidget(vars_block.parent())

def load_math_blocks(layout:QLayout):
    vars_blocks = list()
    color = QColor(0, 117, 255)
    vars_blocks.append(QCallFunctionBlock("", {'':'', '+':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '-':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '*':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '/':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '^':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', 'mod':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '<':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '>':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '=':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '≠':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '≤':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', '≥':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', 'and':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {'':'', 'or':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock("", {' not':''}, color, block_container_widget(), True))
    vars_blocks.append(QCallFunctionBlock(" pick random integer between", {'':'', 'and':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock(" pick random float between", {'':'', 'and':''}, color, block_container_widget()))
    for vars_block in vars_blocks:
        layout.addWidget(vars_block.parent())

def load_arrays_blocks(layout:QLayout):
    vars_blocks = list()
    color = QColor(24,182,199)
    vars_blocks.append(QCallFunctionBlock("make list", {}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("insert", {'':'', 'in list':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("delete", {'':'', 'from list':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("does list", {'has':'inverse', '?':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("how many", {'does list':'inverse', 'has?':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("find", {'':'', 'in list':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("find", {'':'', 'in list':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("remove item number", {'':'', 'from list':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("remove the last item", {'in list':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("where", {'in list':'inverse', '?':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("get item number", {'':'', 'in list':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("slice list", {'':'', 'from':'', 'to':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("pop item number", {'in list':'inverse', 'out':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("pop item number", {'in list':'inverse', 'out':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("clear list", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("max", {'list':'italic'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("min", {'list':'italic'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("sum", {'list':'italic'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("make a copy of list", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("reverse list", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("make dictionary", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("insert in dectionary", {'':'', 'key':'italic', 'value':'italic'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("remove row from dictionary", {'where':'inverse', 'key':'italic'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("does dictionary", {'have the key':'inverse', '?':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("does dictionary", {'have the value':'inverse', '?':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("how many", {'does dictionary':'inverse', 'have?':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("list keys of dictionary", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("list values of dictionary", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("clear dictionary", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("pop last row in dictionary", {'out':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("pop row number", {'in dectionary':'inverse', 'out':'inverse'}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("get row number", {'':'', 'of dictionary': ''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("make a copy of dictionary", {'':''}, color, block_container_widget()))
    vars_blocks.append(QCallFunctionBlock("transform dictionary", {'into two dimentional list':'inverse'}, color, block_container_widget()))
    for vars_block in vars_blocks:
        layout.addWidget(vars_block.parent())

class QBlockSpace(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.blockspace_layout = QHBoxLayout(self)
        self.blockspace_layout.setContentsMargins(0,0,0,0)
        self.blockspace_layout.setSpacing(0)
        # blockarea
        self.blockarea_sa  = QScrollArea()
        self.setStyleSheet("""
            QWidget {border-width:0px; border-style:solid; border-color:#222; background-color: #2f2f2f; border-radius: 5px;}
            QScrollArea {border-width:0px; border-style:solid; border-color:red; background-color: #2f2f2f; border-radius: 5px;}
            QScrollBar:vertical {
                border: 0px solid #1e1e1e;
                background-color: #fff;
                width: 8px;
                margin: 0px;
            }
            QScrollBar:horizontal {
                border: 0px solid #1e1e1e;
                background-color: #fff;
                height: 8px;
                margin: 0px;
            }
            QScrollBar::handle {
                background-color: #444;
                min-height: 20px;
            }
            QScrollBar::handle:hover {
                background-color: #4f4f4f;
            }
            QScrollBar::add-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)
        self.blockarea = QBlockArea()
        self.blockarea_sa.resizeEvent = lambda _: self.blockarea.adjust_size()
        self.blockarea_sa.setWidget(self.blockarea)
        self.blockarea_sa.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.blockarea_sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.blockarea_sa.setWidgetResizable(True)
        self.blockspace_layout.addWidget(self.blockarea_sa)
        # blockpicker
        self.blockpicker = QWidget()
        self.blockpicker.setStyleSheet("""
            QWidget { border-width:0px; border-style:solid; border-color:#222; background-color: #333; border-radius: 0px; }
            QScrollArea { border-width:0px; border-style:solid; border-color:#222; background-color: #2f2f2f; }
            QScrollBar:vertical {
                border: 0px solid #1e1e1e;
                background-color: #fff;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar:horizontal {
                border: 0px solid #1e1e1e;
                background-color: #fff;
                height: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle {
                background-color: #444;
                min-height: 20px;
            }
            QScrollBar::handle:hover {
                background-color: #4f4f4f;
            }
            QScrollBar::add-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)
        self.blockpicker.setFixedWidth(500)
        self.categories_widget = QWidget()
        self.categories_widget.setFixedWidth(55)
        self.categories_layout = QVBoxLayout(self.categories_widget)
        self.categories_layout.setContentsMargins(4,4,4,4)
        self.categories_widget.setStyleSheet("border-width:0px; border-style:solid; border-color:#555; background-color: #444; border-radius: 6px; color: #fff;")
        self.blockpicker_layout = QHBoxLayout(self.blockpicker)
        self.blockspace_layout.addWidget(self.blockpicker)
        self.blockpicker_layout.addWidget(self.categories_widget)
        # Flow Control
        self.flow_ctrl_button = QPushButton()
        self.flow_ctrl_button.setCursor(Qt.PointingHandCursor)
        self.flow_ctrl_button.setToolTip("Flow Control")
        self.flow_ctrl_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\flow control.png"))
        self.flow_ctrl_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.flow_ctrl_button)
        self.flow_ctrl_button.setFixedHeight(45)
        # Core Operations
        self.core_operations_button = QPushButton()
        self.core_operations_button.setCursor(Qt.PointingHandCursor)
        self.core_operations_button.setToolTip("Core Operations")
        self.core_operations_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\core operations.png"))
        self.core_operations_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.core_operations_button)
        self.core_operations_button.setFixedHeight(45)
        # Variables/Datatypes
        self.vars_button = QPushButton()
        self.vars_button.setCursor(Qt.PointingHandCursor)
        self.vars_button.setToolTip("Variables & Datatypes")
        self.vars_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\variables.png"))
        self.vars_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.vars_button)
        self.vars_button.setFixedHeight(45)
        # Mathematics
        self.math_button = QPushButton()
        self.math_button.setCursor(Qt.PointingHandCursor)
        self.math_button.setToolTip("Mathematics")
        self.math_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\mathematics.png"))
        self.math_button.setIconSize(QSize(35, 35))
        self.categories_layout.addWidget(self.math_button)
        self.math_button.setFixedHeight(45)
        # Lists & Dictionaries
        self.lad_button = QPushButton()
        self.lad_button.setCursor(Qt.PointingHandCursor)
        self.lad_button.setToolTip("Lists & Dictionaries")
        self.lad_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\arrays.png"))
        self.lad_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.lad_button)
        self.lad_button.setFixedHeight(45)
        # User Defined Classes
        self.lad_button = QPushButton()
        self.lad_button.setCursor(Qt.PointingHandCursor)
        self.lad_button.setToolTip("User Defined Classes")
        self.lad_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\user defined.png"))
        self.lad_button.setIconSize(QSize(35, 35))
        self.categories_layout.addWidget(self.lad_button)
        self.lad_button.setFixedHeight(45)
        # Foregin Libraries and Extensions
        self.categories_layout.addStretch()
        self.lad_button = QPushButton()
        self.lad_button.setCursor(Qt.PointingHandCursor)
        self.lad_button.setToolTip("Libraries & Extensions")
        self.lad_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\extensions.png"))
        self.lad_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.lad_button)
        self.lad_button.setFixedHeight(45)
        # choose block
        self.choose_block_sa = QScrollArea()
        self.choose_block_widget = QWidget()
        self.choose_block_sa.setWidget(self.choose_block_widget)
        self.choose_block_sa.setWidgetResizable(True)
        self.choose_block_sa.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.choose_block_layout = QVBoxLayout(self.choose_block_widget)
        self.blockpicker_layout.insertWidget(0, self.choose_block_sa)
        # choose categories:
        self.flow_control_label = QLabel("Flow Control"); self.flow_control_label.setStyleSheet("color: #fff; font-size: 25px; margin-bottom: 6px;")
        self.choose_block_layout.addWidget(self.flow_control_label)
        load_flow_control_blocks(self.choose_block_layout)
        self.Core_operations_label = QLabel("Core Operations"); self.Core_operations_label.setStyleSheet("color: #fff; font-size: 25px; margin-bottom: 6px;")
        self.choose_block_layout.addWidget(self.Core_operations_label)
        load_core_operations_blocks(self.choose_block_layout)
        self.vars_label = QLabel("Variables & Datatypes"); self.vars_label.setStyleSheet("color: #fff; font-size: 25px; margin-bottom: 6px;")
        self.choose_block_layout.addWidget(self.vars_label)
        load_vars_blocks(self.choose_block_layout)
        self.math_label = QLabel("Mathematics"); self.math_label.setStyleSheet("color: #fff; font-size: 25px; margin-bottom: 6px;")
        self.choose_block_layout.addWidget(self.math_label)
        load_math_blocks(self.choose_block_layout)
        self.LAD_label = QLabel("Lists & Dictionaries"); self.LAD_label.setStyleSheet("color: #fff; font-size: 25px; margin-bottom: 6px;")
        self.choose_block_layout.addWidget(self.LAD_label)
        load_arrays_blocks(self.choose_block_layout)
        self.user_classes_label = QLabel("User Defined Classes"); self.user_classes_label.setStyleSheet("color: #fff; font-size: 25px; margin-bottom: 6px;")
        self.libs_label = QLabel("Libraries & Extensions"); self.libs_label.setStyleSheet("color: #fff; font-size: 25px; margin-bottom: px;")
        for label in self.user_classes_label, self.libs_label:
            self.choose_block_layout.addWidget(label)
        self.choose_block_layout.addStretch()

class QConsoleWindow(QWidget):
    def paintEvent(self, _):
        # config
        self.color = QColor(30, 30, 30)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.SolidLine))
        # rect 1
        rect_1 = QRect(QPoint(2, 0), QPoint(self.width() - 2, self.height() - 7))
        painter.drawRect(rect_1)
        painter.fillRect(rect_1, self.color)
        # rect 2
        rect_2 = QRect(QPoint(2, 5), QPoint(self.width() - 2, self.height() - 3))
        painter.drawRoundedRect(rect_2, 5, 5)
        painter.fillRect(rect_2, self.color)

class QBlockConsole(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setObjectName('console_block')
        self.console_layout = QVBoxLayout(self)
        self.console_layout.setSpacing(0)
        self.console_layout.setContentsMargins(0,0,0,0)
        # headers
        self.console_headers = QWidget()
        self.console_headers.setStyleSheet("background-color: #0097D4;")
        self.console_headers.setFixedHeight(32)
        self.console_headers_layout = QHBoxLayout(self.console_headers)
        self.console_layout.addWidget(self.console_headers)
        # console window
        self.console_window = QConsoleWindow()
        self.console_layout.addWidget(self.console_window)

class CodeBlocks(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color:#111;")
        self.codeblocks_layout = QVBoxLayout(self)
        self.codeblocks_layout.setContentsMargins(0,0,0,0)
        self.codeblocks_layout.setSpacing(0)
        self.blockspace = QBlockSpace()
        self.codeblocks_layout.addWidget(self.blockspace)
        self.blocksconsole = QBlockConsole()
        self.codeblocks_layout.addWidget(self.blocksconsole)

def init():
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        codeblocks = CodeBlocks()
        SUPER_GLOBAL_SCALE_VAR['super-main-window'] = codeblocks
        codeblocks.setMinimumSize(1000, 600)
        codeblocks.show()
        app.exec_()

init()
