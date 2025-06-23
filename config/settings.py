# config/settings.py

# Configuración de MediaPipe Hands
CAMERA_INDEX = 0  # Índice de la cámara a utilizar (0 para la predeterminada)
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1  # Número máximo de manos a detectar (1 para simplicidad en este ejemplo)

# Configuración de la ventana de la cámara
WINDOW_NAME = "Gesture Control Camera"

# Configuración de los parámetros del controlador de gestos
CURSOR_SPEED_MULTIPLIER = 2.1  # Multiplicador de velocidad del cursor (valor inicial)
CLICK_WAIT_TIME = 0.3          # Tiempo de espera entre clicks (para evitar dobles clicks no deseados)
SCROLL_VERTICAL_SENSITIVITY = 120 # Sensibilidad del scroll vertical
SCROLL_HORIZONTAL_SENSITIVITY = 120 # Sensibilidad del scroll horizontal
PINCH_THRESHOLD = 0.05 # Umbral para el gesto de pinza

# Otros
ENABLE_WEBCAM_DISPLAY = True # Controla si la ventana de la cámara se muestra