import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QComboBox, QMessageBox, QHeaderView, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt
from backend import Backend
from i18n import translations

class ArchToolWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.current_lang = "EN-US"
        self.t = translations[self.current_lang]

        self.setWindowTitle(self.t["app_title"])
        self.resize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self._create_header()

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.store_tab = QWidget()
        self.repos_tab = QWidget()
        self.aur_tab = QWidget()

        self.tabs.addTab(self.store_tab, self.t["store_tab"])
        self.tabs.addTab(self.repos_tab, self.t["repos_tab"])
        self.tabs.addTab(self.aur_tab, self.t["aur_tab"])

        self._setup_store_tab()
        self._setup_repos_tab()
        self._setup_aur_tab()

        self.status_label = QLabel(self.t["status_ready"])
        self.main_layout.addWidget(self.status_label)

    def _create_header(self):
        header_layout = QHBoxLayout()

        lang_label = QLabel(self.t["language"] + ":")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["EN-US", "PT-BR", "DE"])
        self.lang_combo.currentTextChanged.connect(self.change_language)

        header_layout.addStretch()
        header_layout.addWidget(lang_label)
        header_layout.addWidget(self.lang_combo)

        self.main_layout.addLayout(header_layout)

    def _setup_store_tab(self):
        layout = QVBoxLayout(self.store_tab)

        # Search controls
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.t["search_placeholder"])
        self.search_btn = QPushButton(self.t["search_btn"])
        self.search_btn.clicked.connect(self.search_packages)

        self.source_group = QButtonGroup(self)
        self.rb_pacman = QRadioButton(self.t["pacman"])
        self.rb_aur = QRadioButton(self.t["aur"])
        self.rb_pacman.setChecked(True)
        self.source_group.addButton(self.rb_pacman)
        self.source_group.addButton(self.rb_aur)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.rb_pacman)
        search_layout.addWidget(self.rb_aur)
        search_layout.addWidget(self.search_btn)

        # Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Version", "Description", "Source"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Action buttons
        actions_layout = QHBoxLayout()
        self.install_btn = QPushButton(self.t["install_btn"])
        self.remove_btn = QPushButton(self.t["remove_btn"])
        self.install_btn.clicked.connect(self.install_selected)
        self.remove_btn.clicked.connect(self.remove_selected)

        actions_layout.addWidget(self.install_btn)
        actions_layout.addWidget(self.remove_btn)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(actions_layout)

    def _setup_repos_tab(self):
        layout = QVBoxLayout(self.repos_tab)

        self.repo_name_input = QLineEdit()
        self.repo_name_input.setPlaceholderText(self.t["repo_name"])
        self.repo_url_input = QLineEdit()
        self.repo_url_input.setPlaceholderText(self.t["repo_url"])

        self.add_repo_btn = QPushButton(self.t["add_repo_btn"])
        self.add_repo_btn.clicked.connect(self.add_repository)

        layout.addWidget(self.repo_name_input)
        layout.addWidget(self.repo_url_input)
        layout.addWidget(self.add_repo_btn)
        layout.addStretch()

    def _setup_aur_tab(self):
        layout = QVBoxLayout(self.aur_tab)

        # Yay
        yay_layout = QHBoxLayout()
        yay_label = QLabel("Yay:")
        self.install_yay_btn = QPushButton(self.t["install_yay"])
        self.uninstall_yay_btn = QPushButton(self.t["uninstall_yay"])
        self.install_yay_btn.clicked.connect(lambda: self.backend.install_aur_helper("yay"))
        self.uninstall_yay_btn.clicked.connect(lambda: self.backend.uninstall_aur_helper("yay"))
        yay_layout.addWidget(yay_label)
        yay_layout.addWidget(self.install_yay_btn)
        yay_layout.addWidget(self.uninstall_yay_btn)

        # Paru
        paru_layout = QHBoxLayout()
        paru_label = QLabel("Paru:")
        self.install_paru_btn = QPushButton(self.t["install_paru"])
        self.uninstall_paru_btn = QPushButton(self.t["uninstall_paru"])
        self.install_paru_btn.clicked.connect(lambda: self.backend.install_aur_helper("paru"))
        self.uninstall_paru_btn.clicked.connect(lambda: self.backend.uninstall_aur_helper("paru"))
        paru_layout.addWidget(paru_label)
        paru_layout.addWidget(self.install_paru_btn)
        paru_layout.addWidget(self.uninstall_paru_btn)

        layout.addLayout(yay_layout)
        layout.addLayout(paru_layout)
        layout.addStretch()

    def search_packages(self):
        query = self.search_input.text().strip()
        if not query:
            return

        self.status_label.setText("Searching...")
        self.table.setRowCount(0)

        if self.rb_pacman.isChecked():
            results = self.backend.search_pacman(query)
        else:
            # For AUR we check if yay or paru is installed
            helper = "yay" if self.backend.check_installed("yay") else "paru"
            if not self.backend.check_installed(helper):
                QMessageBox.warning(self, "Warning", "No AUR helper (yay/paru) found. Install one first in the 'AUR Helpers' tab.")
                self.status_label.setText(self.t["status_ready"])
                return
            results = self.backend.search_aur(query, helper=helper)

        for i, pkg in enumerate(results):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(pkg["name"]))
            self.table.setItem(i, 1, QTableWidgetItem(pkg["version"]))
            self.table.setItem(i, 2, QTableWidgetItem(pkg["desc"]))
            self.table.setItem(i, 3, QTableWidgetItem(pkg["source"]))

        self.status_label.setText(f"Found {len(results)} packages.")

    def install_selected(self):
        selected = self.table.selectedItems()
        if not selected: return
        row = selected[0].row()
        pkg_name = self.table.item(row, 0).text()
        source = self.table.item(row, 3).text()

        helper = None
        if source == "aur":
            helper = "yay" if self.backend.check_installed("yay") else "paru"

        self.backend.install_package(pkg_name, helper)

    def remove_selected(self):
        selected = self.table.selectedItems()
        if not selected: return
        row = selected[0].row()
        pkg_name = self.table.item(row, 0).text()
        source = self.table.item(row, 3).text()

        helper = None
        if source == "aur":
            helper = "yay" if self.backend.check_installed("yay") else "paru"

        self.backend.remove_package(pkg_name, helper)

    def add_repository(self):
        name = self.repo_name_input.text().strip()
        url = self.repo_url_input.text().strip()
        if not name or not url:
            return

        success, _ = self.backend.add_repo(name, url)
        if success:
            QMessageBox.information(self, "Success", self.t["repo_added_success"])
            self.repo_name_input.clear()
            self.repo_url_input.clear()
        else:
            QMessageBox.critical(self, "Error", self.t["repo_added_fail"])

    def change_language(self, lang):
        self.current_lang = lang
        self.t = translations[lang]
        self.update_ui_texts()

    def update_ui_texts(self):
        self.setWindowTitle(self.t["app_title"])
        self.tabs.setTabText(0, self.t["store_tab"])
        self.tabs.setTabText(1, self.t["repos_tab"])
        self.tabs.setTabText(2, self.t["aur_tab"])

        self.search_input.setPlaceholderText(self.t["search_placeholder"])
        self.search_btn.setText(self.t["search_btn"])
        self.rb_pacman.setText(self.t["pacman"])
        self.rb_aur.setText(self.t["aur"])
        self.install_btn.setText(self.t["install_btn"])
        self.remove_btn.setText(self.t["remove_btn"])

        self.repo_name_input.setPlaceholderText(self.t["repo_name"])
        self.repo_url_input.setPlaceholderText(self.t["repo_url"])
        self.add_repo_btn.setText(self.t["add_repo_btn"])

        self.install_yay_btn.setText(self.t["install_yay"])
        self.uninstall_yay_btn.setText(self.t["uninstall_yay"])
        self.install_paru_btn.setText(self.t["install_paru"])
        self.uninstall_paru_btn.setText(self.t["uninstall_paru"])

        self.status_label.setText(self.t["status_ready"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Apply a simple stylesheet for modern look
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
        }
        QWidget {
            color: #ffffff;
            font-family: Arial;
            font-size: 14px;
        }
        QTabWidget::pane {
            border: 1px solid #444;
            background: #2b2b2b;
        }
        QTabBar::tab {
            background: #3b3b3b;
            padding: 8px 16px;
            margin: 2px;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #5c5c5c;
        }
        QLineEdit {
            background-color: #3b3b3b;
            border: 1px solid #555;
            padding: 6px;
            border-radius: 4px;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QTableWidget {
            background-color: #333333;
            gridline-color: #555;
            border: none;
        }
        QHeaderView::section {
            background-color: #444;
            padding: 4px;
            border: 1px solid #555;
        }
        QComboBox {
            background-color: #3b3b3b;
            border: 1px solid #555;
            padding: 4px;
            border-radius: 4px;
        }
    """)
    window = ArchToolWindow()
    window.show()
    sys.exit(app.exec())
