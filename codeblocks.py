from PyQt6.QtGui import QMoveEvent
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys, math
import traceback

GLOBAL_SCALE_VAR = dict()

def customCircleArguments(ending_point, layout_length, starting_angle, span_angle, p=0):
    radius = layout_length / 2
    h_co = math.sin(starting_angle * (math.pi / 180)) * radius
    w_co = math.cos(starting_angle * (math.pi / 180)) * radius
    y_starting_point = ending_point.y() - (radius - h_co)
    x_starting_point = ending_point.x() - (radius + w_co)
    return int(x_starting_point + p), int(y_starting_point), layout_length, layout_length, starting_angle, span_angle

def drawCircularShape(painter:QPainter, x, pen_resize=False, color=None, p=0, shape_width=4, handle_length=3, x_=0):
    point = QPointF(9 + p, x)
    path = QPainterPath(point)
    path.lineTo(point + QPointF(handle_length, handle_length))
    path.arcTo(*customCircleArguments(path.currentPosition(), 5, -135, 45, p=0))
    path.lineTo(path.currentPosition() + QPointF(shape_width, 0))
    path.arcTo(*customCircleArguments(path.currentPosition(), 5, 270, 45, p=5))
    path.lineTo((path.currentPosition().x() + (handle_length - 1 + x_)), x)
    if pen_resize:
        painter.setPen(QPen(color, pen_resize, Qt.PenStyle.SolidLine))
        painter.drawPath(path)
        painter.setPen(QPen(color, 4, Qt.PenStyle.SolidLine))
    else:
        painter.drawPath(path)

def get_visible_area(scroll_area):
    x_offset = scroll_area.horizontalScrollBar().value()
    y_offset = scroll_area.verticalScrollBar().value()
    return QPoint(x_offset, y_offset)

class VariablesEntry(QLineEdit):
    def __init__(self, layout:QVBoxLayout):
        super().__init__()
        self.layout_ = layout
        self.color = QColor(20, 199-40, 125-40)
        self.returnPressed.connect(self.on_enter_pressed)
    
    def create_variable(self, text):
        container = block_container_widget()
        CallFunctionBlock(text, {}, self.color, container, is_arg=True)
        self.layout_.insertWidget(41, container)

    def on_enter_pressed(self):
        self.create_variable(self.text())
        self.setText('')

class ArgumentEdit(QLineEdit):
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
        except: print("TODO enter pressed event")

    def __init__(self):
        super().__init__()
        self.child = None
        self.pre_color = None
        self.parent_block = None
        self.argument = None
        self.all_args = []
        self.testing_label = QLabel()
        self.setFixedHeight(17)
        self.setStyleSheet("border-radius: 8px; color: #444; background-color: #fff; font-size: 14px; font-family: Roboto; padding-left: 3px; padding-right: 3px;")
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
        self.parentWidget().adjustSize()

    def childResizedEvent(self):
        self.setFixedWidth(self.child.width())
    
    def moveEvent(self, event):
        if self.argument:
            self.argument.move(self.mapTo(self.parentWidget().parentWidget(), QPoint(0, 0)).x(), 0)
        return super().moveEvent(event)

class ContainerClosingStick(QWidget):
    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.PenStyle.SolidLine))
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
        path = QPainterPath(QPointF(9, 1))
        path.lineTo(QPointF(16, 1))
        path.moveTo(38, 1)
        path.lineTo(QPointF(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPointF(self.width() - 3, 16))
        path.moveTo(30, 17)
        path.lineTo(QPointF(self.width() - 4, 17))
        path.moveTo(1, 2)
        path.lineTo(QPointF(1, 16))
        path.moveTo(2, 17)
        path.lineTo(QPointF(7, 17))
        # circular shapes:
        painter.setPen(QPen(Qt.GlobalColor.black, 0.2, Qt.PenStyle.SolidLine))
        drawCircularShape(painter, 2, shape_width=1, x_=0, handle_length=5, p=9)
        # drawCircularShape(painter, 18, shape_width=1, x_=0, handle_length=5)
        # draw path
        painter.drawPath(path)
    
    def showEvent(self, event):
        self.move(self.parent_container.stick.pos() + QPoint(0, self.parent_container.stick.height() - 6))
        self.raise_()
        self.parent_container.closing.raise_()
        return super().showEvent(event)

    def __init__(self, parent_container, parent):
        self.parent_container = parent_container
        self.color = parent_container.color
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"background-color: rgb{parent_container.color.getRgb()[:-1]}; border-radius: 4px;")
        self.setFixedWidth(9)
        self.setFixedHeight(26)
        self.mousePressEvent = parent_container.mousePressEvent
        self.mouseReleaseEvent = parent_container.mouseReleaseEvent
        self.mouseMoveEvent = lambda foreign_event: self.parent_container.mouseMoveEvent(foreign_event)

class ContainerHoldingStick(QLabel):
    def __init__(self, parent_container, parent):
        self.parent_container = parent_container
        self.initial_height = 60
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"background-color: rgb{parent_container.color.getRgb()[:-1]}; border-radius: 4px;")
        self.setFixedWidth(9)
        self.setFixedHeight(self.initial_height)
        self.mousePressEvent = parent_container.mousePressEvent
        self.mouseReleaseEvent = parent_container.mouseReleaseEvent
        self.mouseMoveEvent = lambda foreign_event: self.parent_container.mouseMoveEvent(foreign_event)

    def resizeEvent(self, event):
        self.parent_container.closing.move(self.parent_container.pos() + QPoint(0, self.height() - 6))
        if self.parent_container.is_parent_block:
            self.parent_container.child_block.move(self.parent_container.x(), self.parent_container.y() + self.height() + 12)
        self.parent_container.stack_total_height_changed_alert()
        return super().resizeEvent(event)

    def showEvent(self, event):
        self.move(self.parent_container.pos())
        self.parent_container.raise_()
        return super().showEvent(event)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Qt.GlobalColor.black, 0.2, Qt.PenStyle.SolidLine))
        painter.drawLine(QPoint(1, 2), QPoint(1, self.height()))
        painter.drawLine(QPoint(self.width() - 1, 2), QPoint(self.width() - 1, self.height()))

class ContainerBlock(QWidget):
    def setParent(self, parent):
        if self.is_parent_block:
            self.child_block.setParent(parent)
        if self.is_inner_parent_block:
            self.inner_child_block.setParent(parent)
        self.stick.setParent(parent)
        self.closing.setParent(parent)
        return super().setParent(parent)

    def showEvent(self, event):
        if self.is_parent_block:
            self.child_block.show()
        if self.is_inner_parent_block:
            self.inner_child_block.show()
        self.closing.show()
        self.stick.show()
        return super().showEvent(event)

    def set_parent_block(self, parent_block):
        self.parent_block = parent_block
        self.is_child_block = True

    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.PenStyle.SolidLine))
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
        path = QPainterPath(QPointF(2, 1))
        path.lineTo(QPointF(7, 1))
        path.moveTo(29, 1)
        path.lineTo(QPointF(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPointF(self.width() - 3, 31))
        path.moveTo(38, 32)
        path.lineTo(QPointF(self.width() - 4, 32))
        path.moveTo(1, 2)
        path.lineTo(QPointF(1, 32))
        path.moveTo(9, 32)
        path.lineTo(QPointF(16, 32))
        # circular shapes:
        painter.setPen(QPen(Qt.GlobalColor.black, 0.2, Qt.PenStyle.SolidLine))
        drawCircularShape(painter, 2, shape_width=1, x_=0, handle_length=5)
        #drawCircularShape(painter, 33, shape_width=1, x_=0, handle_length=5, p=9)
        # draw path
        painter.drawPath(path)

    def set_child_block(self, child_block):
        child_block.set_parent_block(self)
        self.child_block = child_block
        self.raise_()
        self.is_parent_block = True
        child_block.move(self.x(), self.y() + self.stick.height() + 12)
        self.stack_total_height_changed_alert()
    
    def disconnect_child_block(self):
        if self.is_parent_block:
            self.is_parent_block = False
            self.child_block = None
        return self
    
    def disconnect_inner_child_block(self):
        if self.is_inner_parent_block:
            self.is_inner_parent_block = False
            self.inner_child_block = None
            self.stick.setFixedHeight(self.stick.initial_height)

    def disconnect_parent_block(self):
        self.is_child_block = False
        prev_parent = self.parent_block.disconnect_child_block()
        self.parent_block = None
        prev_parent.stack_total_height_changed_alert()
    
    def disconnect_inner_parent_block(self):
        self.is_inner_child_block = False
        self.inner_parent_block.disconnect_inner_child_block()
        self.inner_parent_block = None

    def hideEvent(self, event):
        self.stick.hide()
        self.closing.hide()
        return super().hideEvent(event)

    def discard_block(self):
        self.hide()
        self.deleteLater()
        self.stick.deleteLater()
        self.closing.deleteLater()
        if self.is_parent_block:
            self.child_block.discard_block()
        if self.is_inner_parent_block:
            self.inner_child_block.discard_block()

    def mouseReleaseEvent(self, _):
        starting_point = GLOBAL_SCALE_VAR['blockarea-sa'].mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
        relative_point = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
        end_point = starting_point + QPoint(GLOBAL_SCALE_VAR['blockarea-sa'].width(), GLOBAL_SCALE_VAR['blockarea-sa'].height())
        if starting_point.x() < relative_point.x() < end_point.x() and starting_point.y() < relative_point.y() < end_point.y():
            block_relative_point_to_main = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            blockarea_sa_relative_point_to_main = GLOBAL_SCALE_VAR['blockarea-sa'].mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            block_relative_point_to_blockarea = block_relative_point_to_main - blockarea_sa_relative_point_to_main + get_visible_area(GLOBAL_SCALE_VAR['blockarea-sa'])
            self.setParent(GLOBAL_SCALE_VAR['blockarea'])
            self.stick.setParent(GLOBAL_SCALE_VAR['blockarea'])
            self.closing.setParent(GLOBAL_SCALE_VAR['blockarea'])
            self.closing.show()
            self.stick.show()
            self.show()
            self.move(block_relative_point_to_blockarea)
            GLOBAL_SCALE_VAR['connectors-lookup'][self]
        else:
            self.discard_block()
        GLOBAL_SCALE_VAR['blockarea'].adjust_size()

    def moveEvent(self, event):
        if self.stick != self.parent():
            self.stick.setParent(self.parent())
            self.closing.setParent(self.parent())
            self.closing.show()
            self.stick.show()
        self.stick.move(self.pos())
        self.closing.move(self.pos() + QPoint(0, self.stick.height() - 6))
        self.closing.raise_()
        if self.is_parent_block:
            self.child_block.move(self.x(), self.y() + self.stick.height() + 12)
        if self.is_inner_parent_block:
            self.inner_child_block.move(self.pos() + QPoint(self.stick.width(), self.height()-6))
        return super().moveEvent(event)

    def raise_(self):
        if self.is_parent_block:
            self.child_block.raise_()
        if self.is_inner_parent_block:
            self.inner_child_block.raise_()
        return super().raise_()

    def mouseMoveEvent(self, event):
        try:
            block_relative_point_to_main = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            self.setParent(GLOBAL_SCALE_VAR['main-window'])
            self.stick.setParent(GLOBAL_SCALE_VAR['main-window'])
            self.closing.setParent(GLOBAL_SCALE_VAR['main-window'])
            self.show()
            self.closing.show()
            self.stick.show()
            self.move(block_relative_point_to_main)
            delta = QPoint(event.globalPosition().toPoint()  - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            if self.is_child_block:
                self.disconnect_parent_block()
            if self.inner_parent_block:
                self.disconnect_inner_parent_block()
            self.oldPosition = event.globalPosition().toPoint()
        except: traceback.print_exc()

    def make_copy(self):
        copy_ = self.__class__(
            function_name=self.function_name,
            args_dict=self.args_dict,
            color=self.color,
            parent=self.parent(),
            is_copy=False
        )
        copy_.show()
        copy_.move(self.pos())
        relative_point = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
        self.setParent(GLOBAL_SCALE_VAR['main-window'])
        self.move(relative_point)
        self.show()

    def mousePressEvent(self, event):
        try:
            if not self.is_copy:
                self.make_copy()
                self.is_copy = True
            self.stick.raise_()
            self.closing.raise_()
            self.raise_()
            self.oldPosition = event.globalPosition().toPoint() 
        except: traceback.print_exc()

    def analyze_args(self):
        self.arg_entries = dict()
        for arg_name, arg_type in self.args_dict.items():
            # extract style
            is_reversed = False; is_italic = False; is_bold = False
            if "italic" in arg_type: is_italic = True
            if "bold" in arg_type: is_bold = True
            if "reverse" in arg_type: is_reversed = True
            # define arg entries
            if arg_name:
                entry_tag = QLabel(arg_name)
                entry_tag.setStyleSheet(f"border-radius: 8px; color: #fff; background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()}); padding-left: 3px; padding-right: 3px;")
                font = QFont("Roboto", 10)
                font.setBold(is_bold)
                font.setItalic(is_italic)
                entry_tag.setFont(font)
            arg_entry = ArgumentEdit()
            # adding entry and tag to the layout
            if arg_name:
                for widget in ((arg_entry, entry_tag) if is_reversed else (entry_tag, arg_entry)):
                    self.body_widget_layout.addWidget(widget)
            else: self.body_widget_layout.addWidget(arg_entry)

    def resizeEvent(self, event):
        self.closing.setFixedWidth(self.width())
        return super().resizeEvent(event)

    def set_inner_parent_block(self, inner_parent_block):
        self.is_inner_child_block = True
        self.inner_parent_block = inner_parent_block
    
    def get_total_height(self):
        return self.closing.y() - self.y() + (self.child_block.get_total_height() if self.is_parent_block else 0) + 18

    def set_inner_child_block(self, inner_child_block):
        self.is_inner_parent_block = True
        self.inner_child_block = inner_child_block
        self.raise_()
        inner_child_block.set_inner_parent_block(self)
        inner_child_block.move(self.pos() + QPoint(self.stick.width(), self.height()-6))
        inner_child_block.setParent(self.parent())
        inner_child_block.show()
        # get total child height to adjust stick
        self.stick.setFixedHeight(inner_child_block.get_total_height() + self.height())
    
    def inner_stack_height_changed(self):
        self.stick.setFixedHeight(self.inner_child_block.get_total_height() + self.height())
    
    def stack_total_height_changed_alert(self):
        if self.is_child_block:
            self.parent_block.stack_total_height_changed_alert()
        elif self.is_inner_child_block:
            self.inner_parent_block.inner_stack_height_changed()

    def __init__(self, function_name:str, args_dict:dict, color:QColor, parent:QWidget, is_copy=False):
        # call function block constants
        self.total_height = 39
        self.inner_parent_block = None
        self.is_arg = False
        self.is_in_stack = False
        self.is_child_block = False
        self.is_parent_block = False
        self.is_starter = False
        self.body_widget_total_height = 25
        self.parent_block = None
        self.child_block = None
        self.inner_child_block = None
        self.is_inner_child = False
        self.is_inner_parent_block = False
        self.is_inner_child_block = False
        # init args
        self.is_copy = is_copy
        self.color = color
        self.function_name = function_name
        self.args_dict = args_dict
        # widget initiation
        super().__init__(parent)
        self.setFixedHeight(self.total_height)
        self.move(10, 10)
        # add a stick on the left
        self.stick = ContainerHoldingStick(self, parent)
        self.closing = ContainerClosingStick(self, parent)
        self.closing.show()
        self.stick.show()
        # make the body
        self.body_widget = QWidget(self)
        self.body_widget.resizeEvent = lambda _: self.setFixedWidth(self.body_widget.width()+5)
        self.body_widget.move(2, 7)
        self.body_widget_layout = QHBoxLayout()
        self.body_widget_layout.setContentsMargins(3, 0, 3, 1)
        self.body_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.body_widget.setLayout(self.body_widget_layout)
        self.body_widget.setFixedHeight(self.body_widget_total_height)
        self.body_widget.setStyleSheet(f"background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()});")
        # set function name
        self.function_name_tag = QLabel(self.function_name)
        self.function_name_tag.setStyleSheet(f"border-radius: 8px; color: #fff; background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()}); padding-left: 3px;")
        self.function_name_tag.setFont(QFont("Helvetica", 10))
        self.body_widget_layout.addWidget(self.function_name_tag)
        # get args
        self.analyze_args()

class CallFunctionBlock(QWidget):
    def get_total_height(self):
        return 33 + (self.child_block.get_total_height() if self.is_parent_block else 0)

    def setParent(self, parent):
        if self.child_block:
            self.child_block.setParent(parent)
        return super().setParent(parent)

    def stack_total_height_changed_alert(self):
        if self.is_child_block:
            self.parent_block.stack_total_height_changed_alert()
        elif self.is_inner_child_block:
            self.inner_parent_block.inner_stack_height_changed()
        
    def resizeEvent(self, event):
        if self.argument_edit:
            self.argument_edit.setFixedWidth(self.width()-3)
            self.argument_edit.parentWidget().adjustSize()

    def set_parent_block(self, parent_block):
        self.parent_block = parent_block
        self.is_child_block = True

    def set_inner_parent_block(self, inner_parent_block):
        self.inner_parent_block = inner_parent_block
        self.is_inner_child_block = True

    def moveEvent(self, event):
        if self.is_parent_block:
            self.child_block.move(self.x(), self.y()+33)
        return super().moveEvent(event)

    def raise_(self):
        if self.is_parent_block:
            self.child_block.raise_()
        return super().raise_()

    def set_child_block(self, block):
        block.set_parent_block(self)
        self.child_block = block
        self.raise_()
        self.is_parent_block = True
        block.move(self.x(), self.y() + 33)
        self.stack_total_height_changed_alert()

    def paintEvent(self, _):
        # config
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.color, 4, Qt.PenStyle.SolidLine))
        # rect 1
        if not self.is_arg and not self.is_starter:
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
        if self.is_starter:
            drawCircularShape(painter, 27, shape_width=0, handle_length=6, p=-1)
            drawCircularShape(painter, 31, shape_width=0, handle_length=6, p=-1)
            drawCircularShape(painter, 28, shape_width=0, handle_length=6, p=-1)
        elif not self.is_arg:
            drawCircularShape(painter, 5, handle_length=3)
            drawCircularShape(painter, 27, shape_width=0, handle_length=6, p=-1)
            drawCircularShape(painter, 31, shape_width=0, handle_length=6, p=-1)
            drawCircularShape(painter, 28, shape_width=0, handle_length=6, p=-1)
        # border:
        path = QPainterPath(QPointF(2, 1))
        if not self.is_arg and not self.is_starter:
            path.lineTo(QPointF(7, 1))
        else:
            path.lineTo(QPointF(28, 1))
        path.moveTo(29, 1)
        path.lineTo(QPointF(self.width() - 4, 1))
        path.moveTo(self.width() - 3, 1)
        path.lineTo(QPointF(self.width() - 3, 31))
        path.moveTo(30, 32)
        path.lineTo(QPointF(self.width() - 4, 32))
        path.moveTo(1, 2)
        path.lineTo(QPointF(1, 31))
        path.moveTo(2, 32)
        if not self.is_arg:
            path.lineTo(QPointF(7, 32))
        else:
            path.lineTo(QPointF(28, 32))
        # circular shapes:
        painter.setPen(QPen(Qt.GlobalColor.black, 0.2, Qt.PenStyle.SolidLine))
        if not self.is_arg and not self.is_starter:
            drawCircularShape(painter, 2, shape_width=1, x_=0, handle_length=5)
            #drawCircularShape(painter, 33, shape_width=1, x_=0, handle_length=5)
        # draw path
        painter.drawPath(path)

    def disconnect_child_block(self):
        if self.is_parent_block:
            self.is_parent_block = False
            self.child_block = None
        return self

    def disconnect_parent_block(self):
        self.is_child_block = False
        prev_parent = self.parent_block.disconnect_child_block()
        self.parent_block = None
        prev_parent.stack_total_height_changed_alert()
    
    def make_copy(self):
        copy_ = self.__class__(
            function_name=self.function_name,
            args_dict=self.args_dict,
            color=self.color,
            parent=self.parent(),
            is_arg=self.is_arg,
            is_copy=False,
            is_starter=self.is_starter
        )
        copy_.show()
        copy_.move(self.pos())
        relative_point = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
        self.setParent(GLOBAL_SCALE_VAR['main-window'])
        self.move(relative_point)
        self.show()

    def discard_block(self):
        self.hide()
        self.deleteLater()
        if self.is_parent_block:
            self.child_block.discard_block()

    def mouseReleaseEvent(self, _):
        starting_point = GLOBAL_SCALE_VAR['blockarea-sa'].mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
        relative_point = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
        end_point = starting_point + QPoint(GLOBAL_SCALE_VAR['blockarea-sa'].width(), GLOBAL_SCALE_VAR['blockarea-sa'].height())
        if starting_point.x() < relative_point.x() < end_point.x() and starting_point.y() < relative_point.y() < end_point.y():
            block_relative_point_to_main = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            blockarea_sa_relative_point_to_main = GLOBAL_SCALE_VAR['blockarea-sa'].mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            block_relative_point_to_blockarea = block_relative_point_to_main - blockarea_sa_relative_point_to_main + get_visible_area(GLOBAL_SCALE_VAR['blockarea-sa'])
            self.setParent(GLOBAL_SCALE_VAR['blockarea'])
            self.move(block_relative_point_to_blockarea)
            self.show()
            if not self.is_arg:
                GLOBAL_SCALE_VAR['connectors-lookup'][self]
            else: GLOBAL_SCALE_VAR['connectors-lookup'].pass_arg(self)
        else:
            self.discard_block()
        
        GLOBAL_SCALE_VAR['blockarea'].adjust_size()
    
    def show(self):
        if self.child_block:
            self.child_block.show()
        super().show()

    def disconnect_inner_parent_block(self):
        self.is_inner_child_block = False
        self.inner_parent_block.disconnect_inner_child_block()
        self.inner_parent_block = None

    def mouseMoveEvent(self, event):
        try:
            block_relative_point_to_main = self.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            self.setParent(GLOBAL_SCALE_VAR['main-window'])
            self.show()
            delta = QPoint(event.globalPosition().toPoint()  - self.oldPosition)
            self.move(block_relative_point_to_main + delta)
            if self.is_child_block:
                self.disconnect_parent_block()
            if self.is_inner_child_block:
                self.disconnect_inner_parent_block()
            if self.is_arg:
                if self.in_action:
                    self.argument_edit.argument = None
                    self.argument_edit.custom_event(None)
                    self.argument_edit = None
                    self.in_action = False
            self.oldPosition = event.globalPosition().toPoint()
        except: traceback.print_exc()

    def mousePressEvent(self, event):
        try:
            if not self.is_copy:
                self.make_copy()
                self.is_copy = True
            self.raise_()
            self.oldPosition = event.globalPosition().toPoint() 
        except: traceback.print_exc()
    
    def analyze_args(self):
        self.arg_entries = dict()
        for arg_name, arg_type in self.args_dict.items():
            # extract style
            is_reversed = False; is_italic = False; is_bold = False
            if "italic" in arg_type: is_italic = True
            if "bold" in arg_type: is_bold = True
            if "reverse" in arg_type: is_reversed = True
            # define arg entries
            if arg_name:
                entry_tag = QLabel(arg_name)
                entry_tag.setStyleSheet(f"border-radius: 8px; color: #fff; background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()}); padding-left: 3px; padding-right: 3px;")
                font = QFont("Roboto", 10)
                font.setBold(is_bold)
                font.setItalic(is_italic)
                entry_tag.setFont(font)
            arg_entry = ArgumentEdit()
            # adding entry and tag to the layout
            if arg_name:
                for widget in ((arg_entry, entry_tag) if is_reversed else (entry_tag, arg_entry)):
                    self.body_widget_layout.addWidget(widget)
            else: self.body_widget_layout.addWidget(arg_entry)

    def __init__(self, function_name:str, args_dict:dict, color:QColor, parent:QWidget, is_arg=False, is_copy=False, is_starter=False):
        # call function block constants
        self.total_height = 39
        self.is_arg = is_arg
        self.in_action = False
        self.is_in_stack = False
        self.is_inner_child_block = False
        self.inner_parent_block = None
        self.argument_edit = None
        self.is_child_block = False
        self.is_parent_block = False
        self.body_widget_total_height = 25
        self.parent_block = None
        self.child_block = None
        # init args
        self.is_copy = is_copy
        self.color = color
        self.is_starter = is_starter
        self.function_name = function_name
        self.args_dict = args_dict
        # widget initiation
        super().__init__(parent)
        self.setFixedHeight(self.total_height)
        self.move(10, 10)
        # make the body
        self.body_widget = QWidget(self)
        self.body_widget.resizeEvent = lambda _: self.setFixedWidth(self.body_widget.width()+5)
        self.body_widget.move(2, 7)
        self.body_widget_layout = QHBoxLayout()
        self.body_widget_layout.setContentsMargins(3, 0, 3, 1)
        self.body_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.body_widget.setLayout(self.body_widget_layout)
        self.body_widget.setFixedHeight(self.body_widget_total_height)
        self.body_widget.setStyleSheet(f"background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()});")
        # set function name
        if self.function_name:
            self.function_name_tag = QLabel(self.function_name)
            self.function_name_tag.setStyleSheet(f"border-radius: 8px; color: #fff; background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()}); padding-left: 3px;")
            self.function_name_tag.setFont(QFont("Helvetica", 10))
            self.body_widget_layout.addWidget(self.function_name_tag)
        # get args
        self.analyze_args()

class QBlockArea(QWidget):
    def adjust_size(self):
        farthest_x, farthest_y = 0, 0
        for x, y in ((child.x() + child.width(), child.y() + child.height()) for child in self.children()):
            if x > farthest_x: farthest_x = x
            if y > farthest_y: farthest_y = y
        farthest_x += 300 # (180px horizontal X 150px vertical) should give enough room for more codeblocks
        farthest_y += 250
        if self.parent().width() > farthest_x: farthest_x = GLOBAL_SCALE_VAR['blockarea-sa'].width() - 8 # 8px for the scrollbars
        if self.parent().height() > farthest_y: farthest_y = GLOBAL_SCALE_VAR['blockarea-sa'].height() - 8
        self.setFixedSize(farthest_x, farthest_y)

    def __init__(self):
        super().__init__()

class block_container_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.update()

    def showEvent(self, _):
        f_y = 0
        for child in self.children():
            if child.y() + child.height() > f_y: f_y = child.y() + child.height()
        self.setFixedHeight(f_y + 4)

def load_flow_control_blocks(layout:QLayout):
    flow_control_blocks = list()
    color = QColor(227, 139, 2)
    starter_container = block_container_widget()
    starter = CallFunctionBlock(" when the program starts", {}, color, starter_container, is_starter=True, is_copy=False)
    flow_control_blocks.append(starter)
    container1 = block_container_widget()
    call_function1 = CallFunctionBlock(" wait for", {'seconds':'reverse'}, color, container1)
    flow_control_blocks.append(call_function1)
    container2 = block_container_widget()
    call_function2 = CallFunctionBlock(" do nothing", {}, color, container2)
    flow_control_blocks.append(call_function2)
    container_1 = block_container_widget()
    container_block_1 = ContainerBlock(" repeat", {'times':'reverse'}, color, container_1)
    flow_control_blocks.append(container_block_1)
    container_2 = block_container_widget()
    container_block_2 = ContainerBlock(" loop through", {'':'', 'as': ''}, color, container_2)
    flow_control_blocks.append(container_block_2)
    container_3 = block_container_widget()
    container_block_3 = ContainerBlock(" if", {'then':'reverse'}, color, container_3)
    flow_control_blocks.append(container_block_3)
    container_3_else_if = block_container_widget()
    container_block_3_else_if = ContainerBlock(" else if", {'then':'reverse'}, color, container_3_else_if)
    flow_control_blocks.append(container_block_3_else_if)
    container_3_else = block_container_widget()
    container_block_3_else = ContainerBlock(" else", {'then':'reverse'}, color, container_3_else)
    flow_control_blocks.append(container_block_3_else)
    container_4 = block_container_widget()
    container_block_4 = ContainerBlock(" repeat forever", {}, color, container_4)
    flow_control_blocks.append(container_block_4)
    container_5 = block_container_widget()
    container_block_5 = ContainerBlock(" repeat until", {'':''}, color, container_5)
    flow_control_blocks.append(container_block_5)
    container3 = block_container_widget()
    call_function3 = CallFunctionBlock(" stop repeating", {}, color, container3)
    flow_control_blocks.append(call_function3)
    container4 = block_container_widget()
    call_function4 = CallFunctionBlock(" skip to next iteration", {}, color, container4)
    flow_control_blocks.append(call_function4)
    container5 = block_container_widget()
    call_function5 = CallFunctionBlock(" exit program", {}, color, container5)
    flow_control_blocks.append(call_function5)
    container6 = block_container_widget()
    call_function6 = CallFunctionBlock(" end block", {}, color, container6)
    flow_control_blocks.append(call_function6)
    # if - else
    x = block_container_widget()
    #if_block = QContainerBlock(" if", {'then':'reverse'}, color, x)
    #else_block = QDContainerBlock(" else", {}, color, x)
    #if_block.set_double_container(else_block)
    #flow_control_blocks.append(if_block)
    # try - except
    x = block_container_widget()
    #try_block = QContainerBlock(" try ", {}, color, x)
    #except_block = QDContainerBlock(" and if you faild", {}, color, x)
    #try_block.set_double_container(except_block)
    #flow_control_blocks.append(try_block)
    for flow_control_block in flow_control_blocks:
        layout.addWidget(flow_control_block.parent())

def load_core_operations_blocks(layout:QLayout):
    core_operations_blocks = list()
    color = QColor(117, 8, 224)
    container1 = block_container_widget()
    call_function1 = CallFunctionBlock(" display", {'':''}, color, container1)
    core_operations_blocks.append(call_function1)
    
    container2 = block_container_widget()
    call_function2 = CallFunctionBlock("receive text", {'input_hint': 'italic'}, color, container2)
    core_operations_blocks.append(call_function2)

    container3 = block_container_widget()
    call_function3 = CallFunctionBlock("concatonate", {'': '', 'with': ''}, color, container3)
    core_operations_blocks.append(call_function3)

    container4 = block_container_widget()
    call_function4 = CallFunctionBlock("slice", {'': '', 'from': '', 'to': ''}, color, container4)
    core_operations_blocks.append(call_function4)

    container5 = block_container_widget()
    call_function5 = CallFunctionBlock("get", {'': '', 'of': ''}, color, container5)
    core_operations_blocks.append(call_function5)

    container6 = block_container_widget()
    call_function6 = CallFunctionBlock("in", {'': '', 'replace': '', 'with': ''}, color, container6)
    core_operations_blocks.append(call_function6)

    container7 = block_container_widget()
    call_function7 = CallFunctionBlock("length of", {'': ''}, color, container7)
    core_operations_blocks.append(call_function7)

    container8 = block_container_widget()
    call_function8 = CallFunctionBlock("reverse text", {'': ''}, color, container8)
    core_operations_blocks.append(call_function8)

    container9 = block_container_widget()
    call_function9 = CallFunctionBlock("where", {'in': 'reverse', '?': 'reverse'}, color, container9)
    core_operations_blocks.append(call_function9)

    container10 = block_container_widget()
    call_function10 = CallFunctionBlock("split", {'': '', 'in': ''}, color, container10)
    core_operations_blocks.append(call_function10)

    container11 = block_container_widget()
    call_function11 = CallFunctionBlock("remove spaces", {'text': 'italic'}, color, container11)
    core_operations_blocks.append(call_function11)

    container12 = block_container_widget()
    call_function12 = CallFunctionBlock("remove spaces on the right", {'text': 'italic'}, color, container12)
    core_operations_blocks.append(call_function12)

    container13 = block_container_widget()
    call_function13 = CallFunctionBlock("remove spaces on the left", {'text': 'italic'}, color, container13)
    core_operations_blocks.append(call_function13)

    container14 = block_container_widget()
    call_function14 = CallFunctionBlock("capitalize", {'text': 'italic'}, color, container14)
    core_operations_blocks.append(call_function14)

    container15 = block_container_widget()
    call_function15 = CallFunctionBlock("lower", {'text': 'italic'}, color, container15)
    core_operations_blocks.append(call_function15)

    container16 = block_container_widget()
    call_function16 = CallFunctionBlock("start file interaction", {'file_path': 'italic'}, color, container16)
    core_operations_blocks.append(call_function16)

    container17 = block_container_widget()
    call_function17 = CallFunctionBlock("read file", {'file_interaction': 'italic'}, color, container17)
    core_operations_blocks.append(call_function17)

    container18 = block_container_widget()
    call_function18 = CallFunctionBlock("write file", {'data': 'italic', 'file_interaction': 'italic'}, color, container18)
    core_operations_blocks.append(call_function18)

    container19 = block_container_widget()
    call_function19 = CallFunctionBlock("append", {'data': 'italic', 'file_interaction': 'italic'}, color, container19)
    core_operations_blocks.append(call_function19)

    container20 = block_container_widget()
    call_function20 = CallFunctionBlock("close file", {'file_interaction': 'italic'}, color, container20)
    core_operations_blocks.append(call_function20)

    container21 = block_container_widget()
    call_function21 = CallFunctionBlock("delete file", {'file_path': 'italic'}, color, container21)
    core_operations_blocks.append(call_function21)

    container22 = block_container_widget()
    call_function22 = CallFunctionBlock("delete folder", {'folder_path': 'italic'}, color, container22)
    core_operations_blocks.append(call_function22)

    container23 = block_container_widget()
    call_function23 = CallFunctionBlock("create file", {'file_path': 'italic'}, color, container23)
    core_operations_blocks.append(call_function23)

    container24 = block_container_widget()
    call_function24 = CallFunctionBlock("create folder", {'folder_path': 'italic'}, color, container24)
    core_operations_blocks.append(call_function24)

    for core_operations_block in core_operations_blocks:
        layout.addWidget(core_operations_block.parent())

def load_vars_blocks(layout:QLayout):
    vars_blocks = list()
    color = QColor(32, 199, 125)
    container2 = block_container_widget()
    call_function2 = CallFunctionBlock("set", {'': '', 'to equal': ''}, color, container2)
    vars_blocks.append(call_function2)

    container3 = block_container_widget()
    call_function3 = CallFunctionBlock("type of", {'': ''}, color, container3)
    vars_blocks.append(call_function3)

    container4 = block_container_widget()
    call_function4 = CallFunctionBlock("to text", {'': ''}, color, container4)
    vars_blocks.append(call_function4)

    container5 = block_container_widget()
    call_function5 = CallFunctionBlock("to integer", {'': ''}, color, container5)
    vars_blocks.append(call_function5)

    container6 = block_container_widget()
    call_function6 = CallFunctionBlock("to floating point number", {'': ''}, color, container6)
    vars_blocks.append(call_function6)

    container7 = block_container_widget()
    call_function7 = CallFunctionBlock("to boolean", {'': ''}, color, container7)
    vars_blocks.append(call_function7)

    container8 = block_container_widget()
    call_function8 = CallFunctionBlock("change the variable", {'': '', 'by': ''}, color, container8)
    vars_blocks.append(call_function8)

    container9 = block_container_widget()
    call_function9 = CallFunctionBlock("multiply the variable", {'': '', 'with': ''}, color, container9)
    vars_blocks.append(call_function9)

    container10 = block_container_widget()
    call_function10 = CallFunctionBlock("divide the variable", {'': '', 'by': ''}, color, container10)
    vars_blocks.append(call_function10)

    container11 = block_container_widget()
    call_function11 = CallFunctionBlock("raise the variable", {'': '', 'to the power of': ''}, color, container11)
    vars_blocks.append(call_function11)

    vars_entry = VariablesEntry(layout)
    vars_entry.setPlaceholderText("Declare variables")
    vars_entry.setFont(QFont("Helvetica", 12))
    vars_entry.setStyleSheet(f"color: #DDD; background-color: #333; border: 1px solid rgb({color.red()}, {color.green()}, {color.blue()}); padding: 8px; border-radius: 18; margin-right: 5px; margin-left: 5px")
    layout.addWidget(vars_entry)

    for vars_block in vars_blocks:
        layout.addWidget(vars_block.parent())

def load_math_blocks(layout:QLayout):
    vars_blocks = list()
    color = QColor(0, 117, 255)
    # Create variables for each CallFunctionBlock
    block1 = block_container_widget()
    call_function_add = CallFunctionBlock("", {'': '', '+': ''}, color, block1, True)
    vars_blocks.append(call_function_add)

    block2 = block_container_widget()
    call_function_subtract = CallFunctionBlock("", {'': '', '-': ''}, color, block2, True)
    vars_blocks.append(call_function_subtract)

    block3 = block_container_widget()
    call_function_multiply = CallFunctionBlock("", {'': '', '*': ''}, color, block3, True)
    vars_blocks.append(call_function_multiply)

    block4 = block_container_widget()
    call_function_divide = CallFunctionBlock("", {'': '', '/': ''}, color, block4, True)
    vars_blocks.append(call_function_divide)

    block5 = block_container_widget()
    call_function_exponent = CallFunctionBlock("", {'': '', '^': ''}, color, block5, True)
    vars_blocks.append(call_function_exponent)

    block6 = block_container_widget()
    call_function_mod = CallFunctionBlock("", {'': '', 'mod': ''}, color, block6, True)
    vars_blocks.append(call_function_mod)

    block7 = block_container_widget()
    call_function_less_than = CallFunctionBlock("", {'': '', '<': ''}, color, block7, True)
    vars_blocks.append(call_function_less_than)

    block8 = block_container_widget()
    call_function_greater_than = CallFunctionBlock("", {'': '', '>': ''}, color, block8, True)
    vars_blocks.append(call_function_greater_than)

    block9 = block_container_widget()
    call_function_equal = CallFunctionBlock("", {'': '', '=': ''}, color, block9, True)
    vars_blocks.append(call_function_equal)

    block10 = block_container_widget()
    call_function_not_equal = CallFunctionBlock("", {'': '', '≠': ''}, color, block10, True)
    vars_blocks.append(call_function_not_equal)

    block11 = block_container_widget()
    call_function_less_than_equal = CallFunctionBlock("", {'': '', '≤': ''}, color, block11, True)
    vars_blocks.append(call_function_less_than_equal)

    block12 = block_container_widget()
    call_function_greater_than_equal = CallFunctionBlock("", {'': '', '≥': ''}, color, block12, True)
    vars_blocks.append(call_function_greater_than_equal)

    block13 = block_container_widget()
    call_function_and = CallFunctionBlock("", {'': '', 'and': ''}, color, block13, True)
    vars_blocks.append(call_function_and)

    block14 = block_container_widget()
    call_function_or = CallFunctionBlock("", {'': '', 'or': ''}, color, block14, True)
    vars_blocks.append(call_function_or)

    block15 = block_container_widget()
    call_function_not = CallFunctionBlock("", {' not': ''}, color, block15, True)
    vars_blocks.append(call_function_not)

    block16 = block_container_widget()
    call_function_random_int = CallFunctionBlock("pick random integer between", {'': '', 'and': ''}, color, block16)
    vars_blocks.append(call_function_random_int)

    block17 = block_container_widget()
    call_function_random_float = CallFunctionBlock("pick random float between", {'': '', 'and': ''}, color, block17)
    vars_blocks.append(call_function_random_float)


    for vars_block in vars_blocks:
        layout.addWidget(vars_block.parent())

def load_arrays_blocks(layout:QLayout):
    vars_blocks = list()
    color = QColor(24,182,199)
    # Create variables for each CallFunctionBlock
    # Define each block container widget and assign it to a variable.
    container1 = block_container_widget()
    make_list_block = CallFunctionBlock("make list", {}, color, container1)
    vars_blocks.append(make_list_block)

    container2 = block_container_widget()
    insert_block = CallFunctionBlock("insert", {'': '', 'in list': ''}, color, container2)
    vars_blocks.append(insert_block)

    container3 = block_container_widget()
    delete_block = CallFunctionBlock("delete", {'': '', 'from list': ''}, color, container3)
    vars_blocks.append(delete_block)

    container4 = block_container_widget()
    does_list_block = CallFunctionBlock("does list", {'has': 'reverse', '?': 'reverse'}, color, container4)
    vars_blocks.append(does_list_block)

    container5 = block_container_widget()
    how_many_block = CallFunctionBlock("how many", {'does list': 'reverse', 'has?': 'reverse'}, color, container5)
    vars_blocks.append(how_many_block)

    container6 = block_container_widget()
    find_block1 = CallFunctionBlock("find", {'': '', 'in list': ''}, color, container6)
    vars_blocks.append(find_block1)

    container7 = block_container_widget()
    find_block2 = CallFunctionBlock("find", {'': '', 'in list': ''}, color, container7)
    vars_blocks.append(find_block2)

    container8 = block_container_widget()
    remove_item_number_block = CallFunctionBlock("remove item number", {'': '', 'from list': ''}, color, container8)
    vars_blocks.append(remove_item_number_block)

    container9 = block_container_widget()
    remove_last_item_block = CallFunctionBlock("remove the last item", {'in list': ''}, color, container9)
    vars_blocks.append(remove_last_item_block)

    container10 = block_container_widget()
    where_in_list_block = CallFunctionBlock("where", {'in list': 'reverse', '?': 'reverse'}, color, container10)
    vars_blocks.append(where_in_list_block)

    container11 = block_container_widget()
    get_item_number_block = CallFunctionBlock("get item number", {'': '', 'in list': ''}, color, container11)
    vars_blocks.append(get_item_number_block)

    container12 = block_container_widget()
    slice_list_block = CallFunctionBlock("slice list", {'': '', 'from': '', 'to': ''}, color, container12)
    vars_blocks.append(slice_list_block)

    container13 = block_container_widget()
    pop_item_number_block1 = CallFunctionBlock("pop item number", {'in list': 'reverse', 'out': 'reverse'}, color, container13)
    vars_blocks.append(pop_item_number_block1)

    container14 = block_container_widget()
    pop_item_number_block2 = CallFunctionBlock("pop item number", {'in list': 'reverse', 'out': 'reverse'}, color, container14)
    vars_blocks.append(pop_item_number_block2)

    container15 = block_container_widget()
    clear_list_block = CallFunctionBlock("clear list", {'': ''}, color, container15)
    vars_blocks.append(clear_list_block)

    container16 = block_container_widget()
    max_list_block = CallFunctionBlock("max", {'list': 'italic'}, color, container16)
    vars_blocks.append(max_list_block)

    container17 = block_container_widget()
    min_list_block = CallFunctionBlock("min", {'list': 'italic'}, color, container17)
    vars_blocks.append(min_list_block)

    container18 = block_container_widget()
    sum_list_block = CallFunctionBlock("sum", {'list': 'italic'}, color, container18)
    vars_blocks.append(sum_list_block)

    container19 = block_container_widget()
    copy_list_block = CallFunctionBlock("make a copy of list", {'': ''}, color, container19)
    vars_blocks.append(copy_list_block)

    container20 = block_container_widget()
    reverse_list_block = CallFunctionBlock("reverse list", {'': ''}, color, container20)
    vars_blocks.append(reverse_list_block)

    container21 = block_container_widget()
    make_dictionary_block = CallFunctionBlock("make dictionary", {'': ''}, color, container21)
    vars_blocks.append(make_dictionary_block)

    container22 = block_container_widget()
    insert_in_dict_block = CallFunctionBlock("insert in dictionary", {'': '', 'key': 'italic', 'value': 'italic'}, color, container22)
    vars_blocks.append(insert_in_dict_block)

    container23 = block_container_widget()
    remove_row_dict_block = CallFunctionBlock("remove row from dictionary", {'where': 'reverse', 'key': 'italic'}, color, container23)
    vars_blocks.append(remove_row_dict_block)

    container24 = block_container_widget()
    does_dict_have_key_block = CallFunctionBlock("does dictionary", {'have the key': 'reverse', '?': 'reverse'}, color, container24)
    vars_blocks.append(does_dict_have_key_block)

    container25 = block_container_widget()
    does_dict_have_value_block = CallFunctionBlock("does dictionary", {'have the value': 'reverse', '?': 'reverse'}, color, container25)
    vars_blocks.append(does_dict_have_value_block)

    container26 = block_container_widget()
    how_many_dict_block = CallFunctionBlock("how many", {'does dictionary': 'reverse', 'have?': 'reverse'}, color, container26)
    vars_blocks.append(how_many_dict_block)

    container27 = block_container_widget()
    list_keys_dict_block = CallFunctionBlock("list keys of dictionary", {'': ''}, color, container27)
    vars_blocks.append(list_keys_dict_block)

    container28 = block_container_widget()
    list_values_dict_block = CallFunctionBlock("list values of dictionary", {'': ''}, color, container28)
    vars_blocks.append(list_values_dict_block)

    container29 = block_container_widget()
    clear_dict_block = CallFunctionBlock("clear dictionary", {'': ''}, color, container29)
    vars_blocks.append(clear_dict_block)

    container30 = block_container_widget()
    pop_last_row_dict_block = CallFunctionBlock("pop last row in dictionary", {'out': 'reverse'}, color, container30)
    vars_blocks.append(pop_last_row_dict_block)

    container31 = block_container_widget()
    pop_row_dict_block = CallFunctionBlock("pop row number", {'in dictionary': 'reverse', 'out': 'reverse'}, color, container31)
    vars_blocks.append(pop_row_dict_block)

    container32 = block_container_widget()
    get_row_number_dict_block = CallFunctionBlock("get row number", {'': '', 'of dictionary': ''}, color, container32)
    vars_blocks.append(get_row_number_dict_block)

    container33 = block_container_widget()
    copy_dict_block = CallFunctionBlock("make a copy of dictionary", {'': ''}, color, container33)
    vars_blocks.append(copy_dict_block)

    container34 = block_container_widget()
    transform_dict_block = CallFunctionBlock("transform dictionary", {'into two dimensional list': 'reverse'}, color, container34)
    vars_blocks.append(transform_dict_block)


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
            QWidget {border-width:0px; border-style:solid; border-color:#222; background-color: #2f2f2f;}
            QScrollArea {border-width:0px; border-style:solid; border-color:red; background-color: #2f2f2f;}
            QScrollBar:vertical {
                border: none;
                background-color: #fff;
                width: 8px;
                margin: 0px 0px 0px 0px;
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
                background: none;
                height: 0px;
                width: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line {
                border: 0px solid #1e1e1e;
                background-color: none;
                height: 0px;
                width: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.blockarea = QBlockArea()
        GLOBAL_SCALE_VAR['blockarea'] = self.blockarea
        GLOBAL_SCALE_VAR['blockarea-sa'] = self.blockarea_sa
        self.blockarea_sa.resizeEvent = lambda _: self.blockarea.adjust_size()
        self.blockarea_sa.setWidget(self.blockarea)
        self.blockarea_sa.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.blockarea_sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.blockarea_sa.setWidgetResizable(True)
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
        self.blockpicker_layout.addWidget(self.categories_widget)
        self.blockspace_layout.addWidget(self.blockpicker)
        self.blockspace_layout.addWidget(self.blockarea_sa)
        # Flow Control
        self.flow_ctrl_button = QPushButton()
        self.flow_ctrl_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.flow_ctrl_button.setToolTip("Flow Control")
        self.flow_ctrl_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\blocksimages\flow control.png"))
        self.flow_ctrl_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.flow_ctrl_button)
        self.flow_ctrl_button.setFixedHeight(45)
        # Core Operations
        self.core_operations_button = QPushButton()
        self.core_operations_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.core_operations_button.setToolTip("Core Operations")
        self.core_operations_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\blocksimages\core operations.png"))
        self.core_operations_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.core_operations_button)
        self.core_operations_button.setFixedHeight(45)
        # Variables/Datatypes
        self.vars_button = QPushButton()
        self.vars_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.vars_button.setToolTip("Variables & Datatypes")
        self.vars_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\blocksimages\variables.png"))
        self.vars_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.vars_button)
        self.vars_button.setFixedHeight(45)
        # Mathematics
        self.math_button = QPushButton()
        self.math_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.math_button.setToolTip("Mathematics")
        self.math_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\blocksimages\mathematics.png"))
        self.math_button.setIconSize(QSize(35, 35))
        self.categories_layout.addWidget(self.math_button)
        self.math_button.setFixedHeight(45)
        # Lists & Dictionaries
        self.lad_button = QPushButton()
        self.lad_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lad_button.setToolTip("Lists & Dictionaries")
        self.lad_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\blocksimages\arrays.png"))
        self.lad_button.setIconSize(QSize(40, 40))
        self.categories_layout.addWidget(self.lad_button)
        self.lad_button.setFixedHeight(45)
        # User Defined Classes
        self.lad_button = QPushButton()
        self.lad_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lad_button.setToolTip("User Defined Classes")
        self.lad_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\blocksimages\user defined.png"))
        self.lad_button.setIconSize(QSize(35, 35))
        self.categories_layout.addWidget(self.lad_button)
        self.lad_button.setFixedHeight(45)
        # Foregin Libraries and Extensions
        self.categories_layout.addStretch()
        self.lad_button = QPushButton()
        self.lad_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lad_button.setToolTip("Libraries & Extensions")
        self.lad_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\blocksimages\extensions.png"))
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
        self.blockpicker_layout.insertWidget(1, self.choose_block_sa)
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
        painter.setPen(QPen(self.color, 4, Qt.PenStyle.SolidLine))
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
        self.console_headers_layout.setContentsMargins(6, 0, 0, 0)
        self.console_layout.addWidget(self.console_headers)
        # add buttons
        self.run_button = QPushButton()
        self.run_button.setStyleSheet("background: none; border: none; color: transparent;")
        self.run_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\AstroCode\static\continue-tb.png"))
        self.run_button.setIconSize(QSize(27, 27))
        self.stop_button = QPushButton()
        self.stop_button.setStyleSheet("background: none; border: none; color: transparent;")
        self.stop_button.setIcon(QIcon(r"C:\Users\skhodari\Desktop\AstroCode\static\stop-tb.png"))
        self.stop_button.setIconSize(QSize(23, 23))
        
        self.console_headers_layout.addWidget(self.run_button)
        self.console_headers_layout.addWidget(self.stop_button)
        self.console_headers_layout.addStretch()
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

class ConnectorsLookup:
    def __init__(self):
        self.connector_range = QPoint(12, 12)

    def replace_argumentedit_with_an_argument(self, argument_edit, argument):
        call_function_block = argument_edit.parentWidget().parentWidget()
        argument.setParent(call_function_block)
        argument.argument_edit = argument_edit
        argument.in_action = True
        argument_edit.argument = argument
        argument.move(argument_edit.mapTo(call_function_block, QPoint(0, 0)).x(), 0)
        argument_edit.setFixedWidth(argument.width()-3)
        argument_edit.parentWidget().adjustSize()
        argument.show()

    def pass_arg(self, argument):
        argument_edits = set(GLOBAL_SCALE_VAR['blockarea'].findChildren(ArgumentEdit)) - set(argument.findChildren(ArgumentEdit))
        for argument_edit in argument_edits:
            argument_edit_relative_point = argument_edit.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            argument_relative_strting_point = argument.mapTo(GLOBAL_SCALE_VAR['main-window'], QPoint(0, 0))
            argument_relative_end_point = argument_relative_strting_point + QPoint(argument.width(), argument.height())
            if argument_relative_strting_point.x() < argument_edit_relative_point.x() < argument_relative_end_point.x() and argument_relative_strting_point.y() < argument_edit_relative_point.y() < argument_relative_end_point.y():
                self.replace_argumentedit_with_an_argument(argument_edit, argument)

    def __getitem__(self, block):
        possible_connections = []
        bottom_connector_introduced = False
        # get the block in the very bottom for top connectors
        bottom_block = block
        single = True
        while True:
            if bottom_block.is_parent_block:
                bottom_block = bottom_block.child_block
                single = False
            else: break
        # remove stuff we don't need
        call_function_blocks = GLOBAL_SCALE_VAR['blockarea'].findChildren(CallFunctionBlock) + GLOBAL_SCALE_VAR['blockarea'].findChildren(ContainerBlock)
        if block in call_function_blocks:
            call_function_blocks.remove(block)
        if block.is_parent_block:
            if block.child_block in call_function_blocks:
                call_function_blocks.remove(block.child_block)
        if block.is_child_block:
            if block.parent_block in call_function_blocks:
                call_function_blocks.remove(block.parent_block)
        # loop throu the others
        for connector_block in call_function_blocks:
            if isinstance(connector_block, CallFunctionBlock):
                # get bottom_block range
                if isinstance(bottom_block, ContainerBlock):
                    starting_range = bottom_block.closing.pos() - self.connector_range
                    end_range = bottom_block.closing.pos() + self.connector_range
                    connector_pos_bottom = connector_block.pos() - QPoint(0, bottom_block.closing.height())
                else:
                    starting_range = bottom_block.pos() - self.connector_range
                    end_range = bottom_block.pos() + self.connector_range
                    connector_pos_bottom = connector_block.pos() - QPoint(0, bottom_block.height())
                if starting_range.x() < connector_pos_bottom.x() < end_range.x() and starting_range.y() < connector_pos_bottom.y() < end_range.y():
                    possible_connections.append((bottom_block, connector_block, 'top'))
                # get top_block range
                starting_range = block.pos() - self.connector_range
                end_range = block.pos() + self.connector_range
                connector_pos_top = connector_block.pos() + QPoint(0, connector_block.height())
                if starting_range.x() < connector_pos_top.x() < end_range.x() and starting_range.y() < connector_pos_top.y() < end_range.y():
                    bottom_connector_introduced = True # or inner connector
                    possible_connections.append((connector_block, block, 'bottom'))
            elif isinstance(connector_block, ContainerBlock):
                # get bottom_block range
                if isinstance(bottom_block, ContainerBlock):
                    starting_range = bottom_block.closing.pos() - self.connector_range
                    end_range = bottom_block.closing.pos() + self.connector_range
                    connector_pos_bottom = connector_block.pos() - QPoint(0, bottom_block.closing.height())
                else:
                    starting_range = bottom_block.pos() - self.connector_range
                    end_range = bottom_block.pos() + self.connector_range
                    connector_pos_bottom = connector_block.pos() - QPoint(0, bottom_block.height())
                if starting_range.x() < connector_pos_bottom.x() < end_range.x() and starting_range.y() < connector_pos_bottom.y() < end_range.y():
                    possible_connections.append((bottom_block, connector_block, 'top'))
                # get top_block range
                starting_range = block.pos() - self.connector_range
                end_range = block.pos() + self.connector_range
                connector_pos_top = connector_block.closing.pos() + QPoint(0, connector_block.closing.height())
                if starting_range.x() < connector_pos_top.x() < end_range.x() and starting_range.y() < connector_pos_top.y() < end_range.y():
                    bottom_connector_introduced = True
                    possible_connections.append((connector_block, block, 'bottom'))
                # inner connector
                starting_range = block.pos() - self.connector_range
                end_range = block.pos() + self.connector_range
                connector_pos_top = connector_block.pos() + QPoint(connector_block.stick.width(), connector_block.height())
                if starting_range.x() < connector_pos_top.x() < end_range.x() and starting_range.y() < connector_pos_top.y() < end_range.y():
                    bottom_connector_introduced = True
                    possible_connections.append((connector_block, block, 'inner'))

        for block_1, block_2, type_ in possible_connections:
            if type_ == 'bottom':
                if not block_2.is_starter:
                    if block_1.is_parent_block:
                        blcok_1_child = block_1.child_block
                        block_1.child_block.disconnect_parent_block()
                        block_1.set_child_block(block_2)
                        block_2_bottom = block_2
                        while True:
                            if block_2_bottom.is_parent_block:
                                block_2_bottom = block_2_bottom.child_block
                            else: break
                        block_2_bottom.set_child_block(blcok_1_child)
                    else:
                        block_1.set_child_block(block_2)
                break
            elif type_ == 'inner':
                if not block_2.is_starter:
                    if block_1.inner_child_block:
                        blcok_1_child = block_1.inner_child_block
                        block_1.inner_child_block.disconnect_inner_parent_block()
                        block_1.set_inner_child_block(block_2)
                        block_2.set_child_block(blcok_1_child)
                    else:
                        block_1.set_inner_child_block(block_2)
                break
            else:
                if bottom_connector_introduced:
                    continue
                if not block_2.is_starter:
                    if block_2.is_child_block:
                        if single:
                            block_2_parent = block_2.parent_block
                            block_2.disconnect_parent_block()
                            block_2_parent.set_child_block(block_1)
                        else:
                            block_2.disconnect_parent_block()
                            block_1.set_child_block(block_2)
                    block_1.set_child_block(block_2)
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    codeblocks = CodeBlocks()
    connectors_lookup = ConnectorsLookup()
    GLOBAL_SCALE_VAR['main-window'] = codeblocks
    GLOBAL_SCALE_VAR['connectors-lookup'] = connectors_lookup
    codeblocks.setMinimumSize(1000, 600)
    codeblocks.show()
    app.exec()
