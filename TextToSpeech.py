from pathlib import Path
from typing import Union

from PyQt5 import uic
from PyQt5.QtCore import QLocale
from PyQt5.QtTextToSpeech import QTextToSpeech
from PyQt5.QtWidgets import (QApplication, QComboBox, QLineEdit, QMainWindow,
                             QPushButton, QSlider, QVBoxLayout)


class TextToSpeech(QMainWindow):

    def __init__(self):
        # Initialize
        super(TextToSpeech, self).__init__()

        # Load Ui File
        uic.loadUi(Path.joinpath(
            Path(__file__).parent.resolve(), 'TextToSpeech2.ui'), self)

        # Widgets
        self.lineEdit: QLineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.comboBox: QComboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBoxLocales: QComboBox = self.findChild(
            QComboBox, 'comboBoxLocales')
        self.horizontalSliderSpeed: QSlider = self.findChild(
            QSlider, 'horizontalSliderSpeed')

        self.pushButton: QPushButton = self.findChild(
            QPushButton, 'pushButton')
        self.slider: QSlider = self.findChild(QSlider, 'horizontalSlider')

        layout: QVBoxLayout = self.findChild(
            QVBoxLayout, 'verticalLayout')
        # layout.setContentsMargins(10, 10, 10, 10)
        print(layout.getContentsMargins())

        # Set actions
        self.pushButton.clicked.connect(self.say)

        # Get all engines
        self.engine: Union[QTextToSpeech, None] = None
        engineNames = QTextToSpeech.availableEngines()

        if len(engineNames) > 0:
            # Select the first engine for the default one
            engineName = engineNames[0]
            # Select default engine
            self.engine = QTextToSpeech(engineName)
            self.engine.stateChanged.connect(self.stateChanged)

            # Get all available voices
            self.voices = []
            for voice in self.engine.availableVoices():
                self.voices.append(voice)
                self.comboBox.addItem(voice.name())

            # Get locales
            self.locales = []
            currentLocale = self.engine.locale()
            currentIndex = 0
            for (i, locale) in enumerate(self.engine.availableLocales()):
                self.locales.append(locale)
                self.comboBoxLocales.addItem(
                    locale.languageToString(locale.language()) + ' - ' + locale.countryToString(locale.country()))

                if currentLocale == locale:
                    currentIndex = i
            #  set the current combo as the default locale
            self.comboBoxLocales.setCurrentIndex(currentIndex)

            # Horizontal slider
            self.horizontalSliderSpeed.setValue(0)
        else:
            self.pushButton.setEnabled(False)

        # Show Window App
        self.show()

    def stateChanged(self, state):
        """When QCombo box state is changed"""
        if state == QTextToSpeech.State.Ready:
            self.pushButton.setDisabled(False)

    def say(self):
        """Talk"""
        if self.lineEdit.text().strip() == '':
            return
        self.pushButton.setEnabled(False)
        self.engine.setVoice(self.voices[self.comboBox.currentIndex()])
        self.engine.setVolume(float(self.slider.value() / 100))
        self.engine.setLocale(
            self.locales[self.comboBoxLocales.currentIndex()])
        print(self.horizontalSliderSpeed.value(),
              self.horizontalSliderSpeed.value())
        self.engine.setRate(float(self.horizontalSliderSpeed.value() / 100))
        self.engine.say(self.lineEdit.text())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = TextToSpeech()
    sys.exit(app.exec_())
