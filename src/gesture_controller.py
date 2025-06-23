import time
import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
from .hand_recognition import HandRecog
from .gesture_handlers import Controller
from .enums.gesture_enums import HLabel, Gest
from config.settings import (
    CAMERA_INDEX,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    MAX_NUM_HANDS,
    WINDOW_NAME 
)

#Cargar el modelo de gestos desde un archivo .safetensors
from safetensors.torch import load_file

model_path = "models/model.safetensors"

try:
    # Intenta cargar el modelo
    model_state_dict = load_file(model_path)
    print("El modelo se ha cargado correctamente.")
except Exception as e:
    # Si hay un error, imprime el mensaje de error y detén la ejecución
    print(f"Error al cargar el modelo: {e}")
    raise SystemExit  

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# --- constantes para la ventana de la cámara ---
CAMERA_WINDOW_WIDTH = 200 # Ancho deseado
CAMERA_WINDOW_HEIGHT = 150 # Alto deseado
CAMERA_WINDOW_X = 10 # Posición X desde la izquierda superior
CAMERA_WINDOW_Y = 10 # Posición Y desde la izquierda superior

class GestureController:
    """
    Maneja la cámara, obtiene los puntos de referencia (landmarks) de MediaPipe,
    y sirve como punto de entrada para todo el programa.
    """
    gc_mode = 0
    cap = None
    CAM_HEIGHT = 0
    CAM_WIDTH = 0
    hr_major = None
    hr_minor = None
    stop_detection_event = None
    gesture_queue = None

    def __init__(self, stop_event=None, gesture_queue=None):
        self.stop_detection_event = stop_event
        self.gesture_queue = gesture_queue
        self.gc_mode = 0

    def start_detection(self):
        self.gc_mode = 1
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        if not self.cap.isOpened():
            print(f"Error: No se pudo abrir la cámara en el índice {CAMERA_INDEX}.")
            self.gc_mode = 0
            if self.gesture_queue:
                self.gesture_queue.put("ERROR: No se pudo abrir la cámara.")
            return

        self.CAM_HEIGHT = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.CAM_WIDTH = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        handmajor = HandRecog(HLabel.MAJOR)
        handminor = HandRecog(HLabel.MINOR)

        prev_major_gesture = Gest.UNKNOWN

        # --- Configuración de la ventana de la cámara de OpenCV ---
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL) # Crear ventana con tamaño normalizable
        # Reajustar el tamaño para que sea más pequeño
        cv2.resizeWindow(WINDOW_NAME, CAMERA_WINDOW_WIDTH, CAMERA_WINDOW_HEIGHT)
        # Mover la ventana a la posición deseada (esquina superior izquierda)
        cv2.moveWindow(WINDOW_NAME, CAMERA_WINDOW_X, CAMERA_WINDOW_Y)

        # Intentar que la ventana esté siempre encima (solo funciona en algunos OS/WM)
        # Esto es un truco, y no es 100% fiable en todos los sistemas operativos.
        # En Windows, puede funcionar mejor con el flag cv2.WINDOW_GUI_NORMAL o cv2.WINDOW_GUI_EXPANDED
        # y luego usar un módulo específico de OS como win32gui.
        # Para multiplataforma, cv2.WINDOW_AUTOSIZE con cv2.WND_PROP_TOPMOST es lo que se intenta.
        # Es posible que necesites win32gui (pip install pywin32) para un control más fino en Windows.
        # Para este ejemplo, solo usaremos las funciones básicas de OpenCV.
        # cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_TOPMOST, cv2.WINDOW_AUTOSIZE) # No siempre funciona

        with mp_hands.Hands(
                min_detection_confidence=MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
                max_num_hands=MAX_NUM_HANDS) as hands:

            while self.gc_mode == 1 and (self.stop_detection_event is None or not self.stop_detection_event.is_set()):
                ret, image = self.cap.read()
                if not ret:
                    print("Error: No se pudo leer el frame de la cámara.")
                    time.sleep(0.1)
                    continue

                image = cv2.flip(image, 1)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                gest_name_major = Gest.UNKNOWN
                gest_name_minor = Gest.UNKNOWN

                if results.multi_hand_landmarks:
                    for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        handedness_dict = MessageToDict(results.multi_handedness[i])
                        label = handedness_dict['classification'][0]['label']

                        if label == "Right":
                            handmajor.update_hand_result(hand_landmarks)
                            GestureController.hr_major = hand_landmarks
                            handmajor.set_finger_state()
                            gest_name_major = handmajor.get_gesture()
                        elif label == "Left":
                            handminor.update_hand_result(hand_landmarks)
                            GestureController.hr_minor = hand_landmarks
                            handminor.set_finger_state()
                            gest_name_minor = handminor.get_gesture()

                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        if hand_landmarks.landmark and len(hand_landmarks.landmark) > 9:
                            x_text = int(hand_landmarks.landmark[9].x * image.shape[1])
                            y_text = int(hand_landmarks.landmark[9].y * image.shape[0])

                            display_gesture_name = "Unknown"
                            if label == "Right":
                                display_gesture_name = gest_name_major.name
                                cv2.putText(image, f"R: {display_gesture_name}", (x_text, y_text - 20),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            elif label == "Left":
                                display_gesture_name = gest_name_minor.name
                                cv2.putText(image, f"L: {display_gesture_name}", (x_text, y_text - 20),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                    if gest_name_major != Gest.UNKNOWN and gest_name_major != Gest.PALM:
                        Controller.handle_controls(gest_name_major, handmajor.hand_result)
                        if self.gesture_queue and gest_name_major != prev_major_gesture:
                            self.gesture_queue.put(f"Gesto activo: {gest_name_major.name}")
                            prev_major_gesture = gest_name_major
                    else:
                        Controller.prev_hand = None
                        if self.gesture_queue and prev_major_gesture != Gest.UNKNOWN:
                            self.gesture_queue.put("Gesto activo: Ninguno / Desconocido")
                            prev_major_gesture = Gest.UNKNOWN

                else:
                    Controller.prev_hand = None
                    Controller.flag = False
                    Controller.grabflag = False
                    Controller.scrollflag = False
                    Controller.pinchmajorflag = False
                    if self.gesture_queue and prev_major_gesture != Gest.UNKNOWN:
                        self.gesture_queue.put("Manos no detectadas")
                        prev_major_gesture = Gest.UNKNOWN

                # Redimensionar la imagen para la ventana pequeña
                display_image = cv2.resize(image, (CAMERA_WINDOW_WIDTH, CAMERA_WINDOW_HEIGHT))
                cv2.imshow(WINDOW_NAME, display_image)

                # Si la ventana de OpenCV se cierra manualmente, `cv2.getWindowProperty` devolverá -1.
                # También, `waitKey` devuelve -1 si no hay ninguna tecla presionada.
                if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                    print("Deteniendo por 'q' o cierre de ventana de cámara.")
                    # Establecer el evento de detención para notificar a la GUI
                    self.stop_detection_event.set()
                    break
                # Si se usa un evento de detención de GUI, salimos del bucle
                if self.stop_detection_event and self.stop_detection_event.is_set():
                    print("Evento de detención de GUI activado. Saliendo del bucle de detección.")
                    break

            self.cap.release()
            cv2.destroyAllWindows()
            self.gc_mode = 0
            print("Detección de gestos finalizada.")
            if self.gesture_queue:
                self.gesture_queue.put("Detección detenida.")

    def stop_detection(self):
        self.gc_mode = 0
        if self.stop_detection_event:
            self.stop_detection_event.set()
        print("Solicitud de detención de detección enviada.")