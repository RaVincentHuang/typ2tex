import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QComboBox, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem, QScrollArea
from PyQt5.QtCore import QUrl, Qt
import PyQt5

from chat import ask_language_model
from convert import tex2typ, typ2tex
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QTextEdit, QApplication, QGraphicsBlurEffect, QGraphicsDropShadowEffect

class TranslatorWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the main window of the LaTeX Typst Tool application.
        Sets the window title, geometry, and creates the tab widget with different tabs.
        Sets up the layout and adds various widgets to each tab.
        """
        super().__init__()
        self.setWindowTitle("LaTeX Typst Tool")
        self.setGeometry(300, 400, 800, 500)
        
        self.tab_widget = QTabWidget()

        self.translator = QWidget()
        self.latex = QWidget()
        self.typst = QWidget()
        self.chat = QWidget()
        self.editor = QWidget()
        self.config = QWidget()
        
        
        self.tab_widget.addTab(self.translator, "Translator")
        self.tab_widget.addTab(self.latex, "LaTeX Symbol")
        self.tab_widget.addTab(self.typst, "Typst Symbol")
        self.tab_widget.addTab(self.chat, "Chat")
        self.tab_widget.addTab(self.editor, "Editor")
        self.tab_widget.addTab(self.config, "Config")
        self.tab_widget.setStyleSheet("QTabBar::tab { height: 40px; width: 120px; }")

        self.latex_image = QPixmap("photo/LaTeX_project_logo_bird.svg.png")
        self.typst_image = QPixmap("photo/typst.png")


        # 添加标签页的Layout
        self.translator_layout = QVBoxLayout(self.translator)
        self.latex_layout = QVBoxLayout(self.latex)
        self.typst_layout = QVBoxLayout(self.typst)
        self.chat_layout = QVBoxLayout(self.chat)

        
        self.source_language_label = QLabel("Source Language:", self.translator)
        self.source_language_label.move(50, 20)
        
        self.source_language_combobox = QComboBox(self.translator)
        self.source_language_combobox.setGeometry(220, 15, 150, 30)
        self.source_language_combobox.addItem("LaTeX")
        self.source_language_combobox.addItem("Typst")

        self.target_language_label = QLabel("Target Language:", self.translator)
        self.target_language_label.move(50, 60)
        
        self.target_language_combobox = QComboBox(self.translator)
        self.target_language_combobox.setGeometry(220, 55, 150, 30)
        self.target_language_combobox.addItem("Typst")
        self.target_language_combobox.addItem("LaTeX")

        self.input_label = QLabel("Input:", self.translator)
        self.input_label.move(50, 100)

        self.input_textbox = QTextEdit(self.translator)
        self.input_textbox.setGeometry(140, 100, 500, 150)
        
        self.translate_button = QPushButton("Translate", self.translator)
        self.translate_button.setGeometry(260, 260, 100, 30)
        self.translate_button.clicked.connect(self.translate_text)
        
        self.clean_button = QPushButton("Clean", self.translator)
        self.clean_button.setGeometry(400, 260, 100, 30)
        self.clean_button.clicked.connect(self.clean_text)
        
        self.translate_button.setStyleSheet("background-color: blue;")
        self.clean_button.setStyleSheet("background-color: red;")
        
        
        self.output_label = QLabel("Output:", self.translator)
        self.output_label.move(50, 300)

        self.output_textbox = QTextEdit(self.translator)
        self.output_textbox.setGeometry(140, 300, 500, 150)
        self.output_textbox.setReadOnly(True)
        
        font = self.font()
        font.setPointSize(12)
        font.setWeight(75)
        self.source_language_label.setFont(font)
        self.target_language_label.setFont(font)
        self.input_label.setFont(font)
        self.output_label.setFont(font)
        self.source_language_label.adjustSize()
        self.target_language_label.adjustSize()
        self.input_label.adjustSize()
        self.output_label.adjustSize()
        
        self.latex_search_label = QLabel("Search:", self.latex)
        self.latex_search_label.move(50, 20)

        self.latex_search_textbox = QLineEdit(self.latex)
        self.latex_search_textbox.setGeometry(140, 15, 500, 30)

        self.latex_table = QTableWidget(self.latex)
        self.latex_table.setGeometry(50, 60, 600, 350)
        self.latex_table.setColumnCount(2)
        self.latex_table.setHorizontalHeaderLabels(["Symbol", "Description"])
        self.latex_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.latex_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.latex_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.latex_table.setShowGrid(True)
        self.latex_table.verticalHeader().setVisible(False)
        self.latex_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Add symbols and descriptions to the latex_table
        self.latex_search_label = QLabel("Search:", self.latex)
        self.latex_search_label.move(50, 20)
        
        self.search_button = QPushButton("Search", self.latex)
        self.search_button.setGeometry(660, 15, 100, 30)
        self.search_button.clicked.connect(self.search_symbols)

        

        self.latex_search_textbox = QLineEdit(self.latex)
        self.latex_search_textbox.setGeometry(140, 15, 500, 30)

        self.latex_table = QTableWidget(self.latex)
        self.latex_table.setGeometry(50, 60, 600, 350)
        self.latex_table.setColumnCount(2)
        self.latex_table.setHorizontalHeaderLabels(["Symbol", "Description"])
        self.latex_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.latex_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.latex_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.latex_table.setShowGrid(True)
        self.latex_table.verticalHeader().setVisible(False)
        self.latex_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Add symbols and descriptions to the latex_table
        symbols = [
            
            ("\\alpha", "Alpha"),
            ("\\beta", "Beta"),
            ("\\gamma", "Gamma"),
            ("\\delta", "Delta"),
            ("\\epsilon", "Epsilon"),
            ("\\zeta", "Zeta"),
            ("\\eta", "Eta"),
            ("\\theta", "Theta"),
            ("\\iota", "Iota"),
            ("\\kappa", "Kappa"),
            ("\\lambda", "Lambda"),
            ("\\mu", "Mu"),
            ("\\nu", "Nu"),
            ("\\xi", "Xi"),
            ("\\pi", "Pi"),
            ("\\rho", "Rho"),
            ("\\sigma", "Sigma"),
            ("\\tau", "Tau"),
            ("\\upsilon", "Upsilon"),
            ("\\phi", "Phi"),
            ("\\chi", "Chi"),
            ("\\psi", "Psi"),
            ("\\omega", "Omega"),
            ("\\varepsilon", "Epsilon (variant)"),
            ("\\vartheta", "Theta (variant)"),
            ("\\varpi", "Pi (variant)"),
            ("\\varrho", "Rho (variant)"),
            ("\\varsigma", "Sigma (variant)"),
            ("\\varphi", "Phi (variant)"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("\\cap", "Intersection"),
            ("\\cup", "Union"),
            ("\\vee", "Logical OR"),
            ("\\wedge", "Logical AND"),
            ("\\oplus", "Direct sum"),
            ("\\otimes", "Tensor product"),
            ("\\odot", "Circle dot"),
            ("\\sqcup", "Disjoint union"),
            ("\\uplus", "Multiset union"),
            ("\\triangledown", "Decrease"),
            ("\\triangleup", "Increase"),
            ("\\circ", "Circle"),
            ("\\star", "Star"),
            ("\\diamond", "Diamond"),
            ("\\box", "Square"),
            ("\\triangleleft", "Left triangle"),
            ("\\triangleright", "Right triangle"),
            ("\\interleave", "Parallel"),
            ("\\parallel", "Parallel"),
            ("\\uplus", "Multiset union"),
            ("+", "Addition"),
            ("-", "Subtraction"),
            ("*", "Multiplication"),
            ("/", "Division"),
            ("\\times", "Times"),
            ("\\div", "Divide"),
            ("\\cdot", "Dot"),
            ("\\pm", "Plus/Minus"),
            ("\\mp", "Minus/Plus"),
            ("\\oplus", "Direct Sum"),
            ("\\ominus", "Minus Sign"),
            ("\\otimes", "Tensor Product"),
            ("\\oslash", "Circle with Slash"),
            ("\\odot", "Circle Dot"),
            ("\\bigoplus", "Big Direct Sum"),
            ("\\bigotimes", "Big Tensor Product"),
            ("\\bigodot", "Big Circle Dot")
            # Add more symbols and descriptions here
        ]
        
        for row, (symbol, description) in enumerate(symbols):
            self.latex_table.insertRow(row)
            self.latex_table.setItem(row, 0, QTableWidgetItem(symbol))
            self.latex_table.setItem(row, 1, QTableWidgetItem(description))
            
        
        self.typst_search_label = QLabel("Search:", self.typst)
        self.typst_search_label.move(50, 20)
        self.typst_search_textbox = QLineEdit(self.typst)
        self.typst_search_textbox.setGeometry(140, 15, 500, 30)
        
        self.search_button_typst = QPushButton("Search", self.typst)
        self.search_button_typst.setGeometry(660, 15, 100, 30)
        self.search_button_typst.clicked.connect(self.search_symbols_typst)

        self.typst_search_textbox = QLineEdit(self.typst)
        self.typst_search_textbox.setGeometry(140, 15, 500, 30)
        
        self.typst_table = QTableWidget(self.typst)
        self.typst_table.setGeometry(50, 60, 600, 350)
        self.typst_table.setColumnCount(2)
        self.typst_table.setHorizontalHeaderLabels(["Symbol", "Description"])
        self.typst_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.typst_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.typst_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.typst_table.setShowGrid(True)
        self.typst_table.verticalHeader().setVisible(False)
        self.typst_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Add symbols and descriptions to the typst_table
        symbols = [
            ("α", "Alpha"),
            ("β", "Beta"),
            ("γ", "Gamma"),
            ("δ", "Delta"),
            ("ε", "Epsilon"),
            ("ζ", "Zeta"),
            ("η", "Eta"),
            ("θ", "Theta"),
            ("ι", "Iota"),
            ("κ", "Kappa"),
            ("λ", "Lambda"),
            ("μ", "Mu"),
            ("ν", "Nu"),
            ("ξ", "Xi"),
            ("π", "Pi"),
            ("ρ", "Rho"),
            ("σ", "Sigma"),
            ("τ", "Tau"),
            ("υ", "Upsilon"),
            ("φ", "Phi"),
            ("χ", "Chi"),
            ("ψ", "Psi"),
            ("ω", "Omega"),
            ("ε", "Epsilon (variant)"),
            ("θ", "Theta (variant)"),
            ("π", "Pi (variant)"),
            ("ρ", "Rho (variant)"),
            ("ς", "Sigma (variant)"),
            ("φ", "Phi (variant)"),
            ("\U0001F600", "Grinning Face"),
            ("\U0001F603", "Smiling Face with Open Mouth"),
            ("\U0001F604", "Smiling Face with Open Mouth and Smiling Eyes"),
            ("\U0001F601", "Grinning Face with Smiling Eyes"),
            ("\U0001F606", "Smiling Face with Open Mouth and Closed Eyes"),
            ("\U0001F605", "Smiling Face with Open Mouth and Cold Sweat"),
            ("\U0001F602", "Face with Tears of Joy"),
            ("\U0001F923", "Rolling on the Floor Laughing"),
            ("\U0001F60A", "Smiling Face with Smiling Eyes"),
            ("\U0001F607", "Smiling Face with Halo"),
            ("\U0001F642", "Slightly Smiling Face"),
            ("\U0001F643", "Upside-Down Face"),
            ("\U0001F609", "Winking Face"),
            ("\U0001F60C", "Relieved Face"),
            ("\U0001F60D", "Smiling Face with Heart-Eyes"),
            ("\U0001F618", "Face Blowing a Kiss"),
            ("\U0001F617", "Kissing Face"),
            ("\U0001F619", "Kissing Face with Smiling Eyes"),
            ("\U0001F61A", "Kissing Face with Closed Eyes"),
            ("\U0001F60B", "Face Savoring Food"),
            ("\U0001F61B", "Face with Tongue"),
            ("\U0001F61C", "Winking Face with Tongue"),
            ("\U0001F61D", "Squinting Face with Tongue"),
            ("\U0001F911", "Money-Mouth Face"),
            ("\U0001F917", "Hugging Face"),
            ("\U0001F914", "Thinking Face"),
            ("\U0001F910", "Zipper-Mouth Face"),
            ("\U0001F610", "Neutral Face"),
            ("\U0001F611", "Expressionless Face"),
            ("\U0001F636", "Face Without Mouth"),
            ("\U0001F60F", "Smirking Face"),
            ("\U0001F612", "Unamused Face"),
            ("\U0001F644", "Face with Rolling Eyes"),
            ("\U0001F62C", "Grimacing Face"),
            ("\U0001F925", "Lying Face"),
            ("\U0001F60C", "Relieved Face"),
            ("\U0001F614", "Pensive Face"),
            ("\U0001F62A", "Sleepy Face"),
            ("\U0001F924", "Drooling Face"),
            ("\U0001F634", "Sleeping Face"),
            ("\U0001F637", "Face with Medical Mask"),
            ("\U0001F912", "Face with Thermometer"),
            ("\U0001F915", "Face with Head-Bandage"),
            ("\U0001F922", "Nauseated Face"),
            ("\U0001F92E", "Face Vomiting"),
            ("\U0001F927", "Sneezing Face"),
            ("\U0001F975", "Hot Face"),
            ("\U0001F976", "Cold Face"),
            ("\U0001F974", "Woozy Face"),
            ("\U0001F635", "Dizzy Face"),
            ("\U0001F92F", "Exploding Head"),
            ("\U0001F920", "Cowboy Hat Face"),
            ("\U0001F973", "Partying Face"),
            ("\U0001F97A", "Pleading Face"),
            ("\U0001F913", "Nerd Face"),
            ("\U0001F60E", "Smiling Face with Sunglasses"),
            ("\U0001F929", "Star-Struck"),
            ("\U0001F970", "Smiling Face with Hearts"),
            ("\U0001F618", "Face Blowing a Kiss"),
            ("\U0001F617", "Kissing Face"),
            ("\U0001F619", "Kissing Face with Smiling Eyes"),
            ("\U0001F61A", "Kissing Face with Closed Eyes"),
            ("\U0001F60B", "Face Savoring Food"),
            ("\U0001F61B", "Face with Tongue"),
            ("\U0001F61C", "Winking Face with Tongue"),
            ("\U0001F61D", "Squinting Face with Tongue"),
            ("\U0001F911", "Money-Mouth Face"),
            ("\U0001F917", "Hugging Face"),
            ("\U0001F914", "Thinking Face"),
            ("\U0001F910", "Zipper-Mouth Face"),
            ("\U0001F610", "Neutral Face"),
            ("\U0001F611", "Expressionless Face"),
            ("↖", "Up-Left Arrow"),
            ("↑", "Up Arrow"),
            ("↗", "Up-Right Arrow"),
            ("←", "Left Arrow"),
            ("↔", "Left-Right Arrow"),
            ("→", "Right Arrow"),
            ("↙", "Down-Left Arrow"),
            ("↓", "Down Arrow"),
            ("↘", "Down-Right Arrow"),
            ("⇐", "Double Left Arrow"),
            ("⇔", "Double Left-Right Arrow"),
            ("⇒", "Double Right Arrow"),
            ("⇑", "Double Up Arrow"),
            ("⇓", "Double Down Arrow"),
            ("⇖", "North West Arrow"),
            ("⇗", "North East Arrow"),
            ("⇘", "South East Arrow"),
            ("⇙", "South West Arrow"),
            ("∑", "Summation"),
            ("∫", "Integral"),
            ("∂", "Partial Differential"),
            ("√", "Square Root"),
            ("∞", "Infinity"),
            ("≠", "Not Equal"),
            ("≈", "Approximately Equal"),
            ("≡", "Congruent"),
            ("≤", "Less Than or Equal"),
            ("≥", "Greater Than or Equal"),
            ("±", "Plus-Minus"),
            ("÷", "Division"),
            ("×", "Multiplication"),
            ("°", "Degree"),
            ("‰", "Per Mille"),
            ("∠", "Angle"),
            ("∴", "Therefore"),
            ("∵", "Because"),
            ("∈", "Element of"),
            ("∉", "Not an Element of"),
            ("⊂", "Subset"),
            ("⊃", "Superset"),
            ("⊆", "Subset or Equal"),
            ("⊇", "Superset or Equal"),
            ("∪", "Union"),
            ("∩", "Intersection"),
            ("∅", "Empty Set"),
            ("∀", "For All"),
            ("∃", "Exists"),
            ("∄", "Does Not Exist"),
            ("∑", "N-ary Summation"),
            ("∏", "N-ary Product"),
            ("∐", "N-ary Coproduct"),
            ("√", "Square Root"),
            ("∛", "Cube Root"),
            ("∜", "Fourth Root"),
            ("∝", "Proportional To"),
            ("∞", "Infinity"),
            ("∟", "Right Angle"),
            ("∠", "Angle"),
            ("∡", "Measured Angle"),
            ("∢", "Spherical Angle"),
            ("∣", "Divides"),
            ("∤", "Does Not Divide"),
            ("∥", "Parallel To"),
            ("∦", "Not Parallel To"),
            ("∧", "Logical And"),
            ("∨", "Logical Or"),
            ("∩", "Intersection"),
            ("∪", "Union"),
            ("∫", "Integral"),
            ("∬", "Double Integral"),
            ("∭", "Triple Integral"),
            ("∮", "Contour Integral"),
            ("∯", "Surface Integral"),
            ("∰", "Volume Integral"),
            ("∱", "Clockwise Integral"),
            ("∲", "Clockwise Contour Integral"),
            ("∳", "Anticlockwise Contour Integral"),
            ("∴", "Therefore"),
            ("∵", "Because"),
            ("∶", "Ratio"),
            ("∷", "Proportion"),
            ("∸", "Dot Minus"),
            ("∺", "Geometric Proportion"),
            ("∻", "Homothetic"),
            ("∼", "Similar To"),
            ("∽", "Reversed Tilde"),
            ("∾", "Inverted Lazy S"),
            ("∿", "Sine Wave"),
            ("≀", "Wreath Product"),
            ("≁", "Not Tilde"),
            ("≂", "Minus Tilde"),
            ("≃", "Asymptotically Equal To"),
            ("≄", "Not Asymptotically Equal To"),
            ("≅", "Approximately Equal To"),
            ("≆", "Approximately But Not Actually Equal To"),
            ("≇", "Neither Approximately Nor Actually Equal To"),
            ("≈", "Almost Equal To"),
            ("≉", "Not Almost Equal To"),
            ("≊", "Almost Equal Or Equal To"),
            ("≋", "Triple Tilde"),
            ("≌", "All Equal To"),
            ("≍", "Equivalent To"),
            ("≎", "Geometrically Equivalent To"),
            ("≏", "Difference Between"),
            ("≐", "Approaches The Limit"),
            ("≑", "Geometrically Equal To"),
            ("≒", "Approximately Equal To Or The Image Of"),
            ("≓", "Image Of Or Approximately Equal To"),
            ("≔", "Colon Equals"),
            ("≕", "Equals Colon"),
            ("≖", "Ring In Equal To"),
            ("≗", "Ring Equal To"),
            ("≘", "Corresponds To"),
            ("≙", "Estimates"),
            ("≚", "Equiangular To"),
            ("≛", "Star Equals"),
            ("≜", "Delta Equal To"),
            ("≝", "Equal To By Definition"),
            ("≞", "Measured By"),
            ("≟", "Questioned Equal To"),
            ("≠", "Not Equal To"),
            ("≡", "Identical To"),
            ("≢", "Not Identical To"),
            ("≣", "Strictly Equivalent To"),
            ("≤", "Less-Than Or Equal To"),
            ("≥", "Greater-Than Or Equal To"),
            ("≦", "Less-Than Over Equal To"),
            ("≧", "Greater-Than Over Equal To"),
            ("≨", "Less-Than But Not Equal To"),
            ("≩", "Greater-Than But Not Equal To"),
            ("≪", "Much Less-Than"),
            ("≫", "Much Greater-Than"),
            ("≬", "Between"),
            ("≭", "Not Equivalent To"),
            ("≮", "Not Less-Than"),
            ("≯", "Not Greater-Than"),
            ("≰", "Neither Less-Than Nor Equal To"),
            ("≱", "Neither Greater-Than Nor Equal To"),
            ("≲", "Less-Than Or Equivalent To"),
            ("≳", "Greater-Than Or Equivalent To"),
            ("≴", "Neither Less-Than Nor Equivalent To"),
            ("≵", "Neither Greater-Than Nor Equivalent To"),
            ("≶", "Less-Than Or Greater-Than"),
            ("≷", "Greater-Than Or Less-Than"),
            ("≸", "Neither Less-Than Nor Greater-Than"),
            ("≹", "Neither Greater-Than Nor Less-Than"),
            ("≺", "Precedes"),
            ("≻", "Succeeds"),
            ("≼", "Precedes Or Equal To"),
            ("≽", "Succeeds Or Equal To"),
            ("≾", "Precedes Or Equivalent To"),
            ("≿", "Succeeds Or Equivalent To"),
            ("⊀", "Does Not Precede"),
            ("⊁", "Does Not Succeed"),
            ("⊂", "Subset Of"),
            ("⊃", "Superset Of"),
            ("⊄", "Not A Subset Of"),
            ("⊅", "Not A Superset Of"),
            ("⊆", "Subset Of Or Equal To"),
            ("⊇", "Superset Of Or Equal To"),
            ("⊈", "Neither A Subset Of Nor Equal To"),
            ("⊉", "Neither A Superset Of Nor Equal To"),
            ("⊊", "Subset Of But Not Equal To"),
            ("⊋", "Superset Of But Not Equal To"),
            ("⊌", "Neither A Subset Of Nor Equal To"),
            ("⊍", "Neither A Superset Of Nor Equal To"),
            ("⊎", "Multiset"),
            ("⊏", "Square Image Of"),
            ("⊐", "Square Original Of"),
            ("⊑", "Square Image Of Or Equal To"),
            ("⊒", "Square Original Of Or Equal To"),
            ("⊓", "Square Cap"),
            ("⊔", "Square Cup"),
            ("⊕", "Circled Plus"),
            ("⊖", "Circled Minus"),
            ("⊗", "Circled Times"),
            ("⊘", "Circled Division Slash"),
            ("⊙", "Circled Dot Operator"),
            ("⊚", "Circled Ring Operator"),
            ("⊛", "Circled Asterisk Operator"),
            ("⊜", "Circled Equals"),
            ("⊝", "Circled Dash"),
            ("⊞", "Squared Plus"),
            ("⊟", "Squared Minus"),
            ("⊠", "Squared Times"),
            ("⊡", "Squared Dot Operator"),
            ("⊢", "Right Tack"),
            ("⊣", "Left Tack"),
            ("⊤", "Down Tack"),
            ("⊥", "Up Tack"),
            ("⊧", "Models"),
            ("⊨", "True"),
            ("⊩", "Forces"),
            ("⊪", "Triple Vertical Bar Right Turnstile"),
            ("⊫", "Double Vertical Bar Double Right Turnstile"),
            ("⊬", "Does Not Prove"),
            ("⊭", "Not True"),
            ("⊮", "Does Not Force"),
            ("⊯", "Negated Double Vertical Bar Double Right Turnstile"),
            ("⊰", "Precedes Under Relation"),
            ("⊱", "Succeeds Under Relation"),
            ("⊲", "Normal Subgroup Of"),
            ("⊳", "Contains As Normal Subgroup"),
            ("⊴", "Normal Subgroup Of Or Equal To"),
            ("⊵", "Contains As Normal Subgroup Or Equal To"),
            ("⊶", "Original Of"),
            ("⊷", "Image Of"),
            ("⊸", "Multimap"),
            ("⊹", "Hermitian Conjugate Matrix"),
            ("⊺", "Intercalate"),
            ("⊻", "Xor"),
            ("⊼", "Nand"),
            ("⊽", "Nor"),
            ("⊾", "Right Angle With Arc"),
            ("⊿", "Right Triangle"),
            # Add more symbols and descriptions here
        ]

        for row, (symbol, description) in enumerate(symbols):
            self.typst_table.insertRow(row)
            self.typst_table.setItem(row, 0, QTableWidgetItem(symbol))
            self.typst_table.setItem(row, 1, QTableWidgetItem(description))
        
        
        self.api_key_label = QLabel("API Key:", self.config)
        self.api_key_label.move(50, 20)
        self.api_key_textbox = QLineEdit(self.config)
        self.api_key_textbox.setGeometry(140, 20, 200, 30)
        self.model_type_label = QLabel("Model Type:", self.config)
        self.model_type_label.move(50, 60)
        self.model_type_combobox = QComboBox(self.config)
        self.model_type_combobox.setGeometry(140, 60, 150, 30)
        self.model_type_combobox.addItem("gpt-3.5-turbo-instruct")
        self.model_type_combobox.addItem("davinci-002")
        self.model_type_combobox.addItem("babbage-002")
        
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setGeometry(140, 200, 150, 30)
        self.chat_textbox = QTextEdit()
        self.chat_textbox.setReadOnly(True)
        self.chat_scroll_area.setWidget(self.chat_textbox)
        self.chat_layout.addWidget(self.chat_scroll_area)
        self.send_textbox = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.chat_layout.addWidget(self.send_textbox)
        self.chat_layout.addWidget(self.send_button)

        button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
    """

    # Apply stylesheet to labels and buttons
        self.send_button.setStyleSheet(button_style)
        
        self.setStyleSheet("background-color: #F0F0F0;")
        
                
        # Create a new tab for the markdown editor
        self.editor_layout = QVBoxLayout(self.editor)

        # Create a QTextEdit widget for the markdown editor
        self.markdown_editor = QTextEdit(parent=self.editor)
        self.markdown_editor.setGeometry(40, 20, 350, 400)
        self.markdown_editor.textChanged.connect(self.display_markdown)
        
        self.markdown_shower = QTextEdit(parent=self.editor)
        self.markdown_shower.setReadOnly(True)
        self.markdown_shower.setGeometry(390, 20, 350, 400)
        
        # Set the central widget to the tab widget
        self.tab_widget.addTab(self.editor, "Editor")
        
        # Set font and font size for the entire application
        font = QFont("Arial", 12)
        QApplication.setFont(font)
        
        # Set the stylesheet for the QTextEdit widgets
        text_edit_style = """
        QTextEdit {
            background-color: white;
            color: black;
            font-size: 12px;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 4px;
        }
        """

        # Apply the stylesheet to the QTextEdit widgets
        self.markdown_editor.setStyleSheet(text_edit_style)
        self.markdown_shower.setStyleSheet(text_edit_style)
        
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # shadow = QGraphicsDropShadowEffect(self)
        # shadow.setBlurRadius(15)
        # shadow.setXOffset(0)
        # shadow.setYOffset(0)
        # self.setGraphicsEffect(shadow)
        
        # Apply the blur effect to the central widget
        self.setCentralWidget(self.tab_widget)
                
    def send_message(self):
        """
        Sends a message using the specified engine and API key.

        Retrieves the input text from the send_textbox, the engine from the model_type_combobox,
        and the API key from the api_key_textbox. Calls the ask_language_model function with
        the input text, engine, and API key to get the answer. Inserts the question and answer
        into the chat_textbox.

        Raises:
            Exception: If an error occurs during the process.

        """
        try:
            input_text = self.send_textbox.text()
            engine = self.model_type_combobox.currentText()
            api_key = self.api_key_textbox.text()

            answer = ask_language_model(input_text, engine, api_key)

            self.chat_textbox.insertHtml(f"<b>Question:</b> {input_text}<br><b>Answer:</b> {answer}<br><br>")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
    def display_markdown(self):
        """
        Updates the markdown_shower widget with the content from the markdown_editor widget.

        This method retrieves the plain text content from the markdown_editor widget and sets it as the markdown content
        for the markdown_shower widget. If an error occurs during the process, an exception is caught and an error message
        is printed.

        Args:
            None

        Returns:
            None
        """
        try:
            content = self.markdown_editor.toPlainText()
            self.markdown_shower.setMarkdown(content)
        except Exception as e:
            print(f"An error occurred: {e}")
        

    def translate_text(self):
        """
        Translates the input text from the source language to the target language.

        Returns:
            str: The translated text.

        Raises:
            Exception: If an error occurs during translation.
        """
        input_text = self.input_textbox.toPlainText()
        source_language = self.source_language_combobox.currentText()
        target_language = self.target_language_combobox.currentText()

        try:
            if source_language == target_language:
                output_text = input_text
            elif source_language == "LaTeX":
                output_text = tex2typ(input_text)
            elif source_language == "Typst":
                output_text = typ2tex(input_text)
            else:
                output_text = "Error!"
        except Exception as e:
            output_text = f"Error: {str(e)}"
            
        self.output_textbox.setPlainText(output_text)
    
    def clean_text(self): 
        """
        Clears the content of the output_textbox and input_textbox.
        """
        self.output_textbox.clear()
        self.input_textbox.clear()
    
    def search_symbols(self):
        """
        Searches for symbols in the LaTeX table based on the search text entered by the user.

        If the search text is not empty, the function iterates through each row in the LaTeX table
        and checks if the search text is present in either the symbol or description column. If a match
        is found, the corresponding row is set to be visible. If no match is found, the row is hidden.

        If the search text is empty, all rows in the LaTeX table are set to be visible.

        Raises:
            Exception: If an error occurs during the search process.

        Returns:
            None
        """
        try:
            search_text = self.latex_search_textbox.text()
            if search_text:
                for row in range(self.latex_table.rowCount()):
                    symbol_item = self.latex_table.item(row, 0)
                    description_item = self.latex_table.item(row, 1)
                    if search_text.lower() in symbol_item.text().lower() or search_text.lower() in description_item.text().lower():
                        self.latex_table.setRowHidden(row, False)
                    else:
                        self.latex_table.setRowHidden(row, True)
            else:
                for row in range(self.latex_table.rowCount()):
                    self.latex_table.setRowHidden(row, False)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def search_symbols_typst(self):
        """
        Search for symbols in the typst_table based on the search_text.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        try:
            search_text = self.typst_search_textbox.text()
            if search_text:
                for row in range(self.typst_table.rowCount()):
                    symbol_item = self.typst_table.item(row, 0)
                    description_item = self.typst_table.item(row, 1)
                    if search_text.lower() in symbol_item.text().lower() or search_text.lower() in description_item.text().lower():
                        self.typst_table.setRowHidden(row, False)
                    else:
                        self.typst_table.setRowHidden(row, True)
            else:
                for row in range(self.typst_table.rowCount()):
                    self.typst_table.setRowHidden(row, False)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    
            
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = TranslatorWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    window.show()
    sys.exit(app.exec_())
    # Set stylesheet for labels and buttons