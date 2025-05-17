import sys
import serial
import time
from PyQt5 import QtWidgets, uic, QtCore

try:
    arduino = serial.Serial('COM10', 9600, timeout=1)
    time.sleep(2)  # Espera a que se inicialice el puerto serial
except serial.SerialException as e:
    print(f"Error al conectar con el puerto serial COM10: {e}")
    sys.exit()

class LEDApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(LEDApp, self).__init__()
        uic.loadUi("Dep.ui", self)

        self.leds = [
            self.findChild(QtWidgets.QLabel, f"led{i+1}") for i in range(3)
        ]
        self.lum_label = self.findChild(QtWidgets.QLabel, "label_lum")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(200)

    def update_values(self):
        try:
            line = arduino.readline().decode('utf-8').rstrip()
            if line.isdigit():
                value = int(line)
                self.lum_label.setText(f"Luminosidad: {value}")
                threshold = value * 3 // 1024  # Mapeo similar al Arduino
                for i in range(3):
                    if i < threshold:
                        self.leds[i].setStyleSheet("background-color: green;")
                    else:
                        self.leds[i].setStyleSheet("background-color: gray;")
            elif line:  # Imprimir cualquier otra cosa que llegue del serial para depuración
                print(f"Dato serial recibido: {line}")
        except serial.SerialException as e:
            print(f"Error al leer del puerto serial: {e}")
            self.timer.stop()
            arduino.close()
            sys.exit()
        except ValueError:
            print(f"Dato no numérico recibido del serial: {line}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def closeEvent(self, event):
        """Manejar el cierre de la ventana para cerrar el puerto serial."""
        if arduino.is_open:
            arduino.close()
            print("Puerto serial cerrado.")
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LEDApp()
    window.show()
    sys.exit(app.exec_())