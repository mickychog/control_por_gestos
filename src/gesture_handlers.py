import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import screen_brightness_control as sbcontrol
from .enums.gesture_enums import Gest, HLabel
import time # Añadir para posibles delays de depuración

# Función para mover el cursor de manera segura
def safe_move_to(x, y, duration=0.1):
    screen_width, screen_height = pyautogui.size()
    x = min(max(0, x), screen_width - 1)
    y = min(max(0, y), screen_height - 1)

    pyautogui.moveTo(x, y, duration=duration)

class Controller:
    tx_old = 0
    ty_old = 0
    trial = True
    flag = False # Generalmente para controlar si un click ya se ha disparado.
    grabflag = False # Para click/doble click y arrastre (mouseDown/Up).
    scrollflag = False # Para el modo de scroll.
    pinchmajorflag = False # Para el modo de volumen/brillo (OK).
    pinchstartxcoord = None
    pinchstartycoord = None
    pinchdirectionflag = None
    prevpinchlv = 0
    pinchlv = 0
    framecount = 0
    prev_hand = None
    pinch_threshold = 0.3 # Ajustar si el movimiento es demasiado sensible/insensible.

    def getpinchylv(hand_result):
        """Devuelve la distancia en el eje Y entre el inicio del gesto de pinza y la posición actual."""
        if not hand_result or not hand_result.landmark or len(hand_result.landmark) <= 8:
            return 0.0
        dist = round((Controller.pinchstartycoord - hand_result.landmark[8].y) * 10, 1)
        return dist

    def getpinchxlv(hand_result):
        """Devuelve la distancia en el eje X entre el inicio del gesto de pinza y la posición actual."""
        if not hand_result or not hand_result.landmark or len(hand_result.landmark) <= 8:
            return 0.0
        dist = round((hand_result.landmark[8].x - Controller.pinchstartxcoord) * 10, 1)
        return dist

    def changesystembrightness():
        """Ajusta el brillo del sistema según el valor de `Controller.pinchlv`."""
        try:
            currentBrightnessLv = sbcontrol.get_brightness(display=0)
            print(f"DEBUG Brillo: Brillo actual: {currentBrightnessLv}%")
            # Convertir a escala 0-100 para la operación, luego a 0-1 para el cálculo
            currentBrightnessLv_scaled = currentBrightnessLv[0] / 100.0 if isinstance(currentBrightnessLv, list) else currentBrightnessLv / 100.0

            # Ajusta este factor para mayor o menor sensibilidad
            # Multiplicamos pinchlv por un factor, por ejemplo, 2 para mayor impacto
            change_amount = Controller.pinchlv / 50.0

            newBrightnessLv = currentBrightnessLv_scaled + change_amount

            if newBrightnessLv > 1.0:
                newBrightnessLv = 1.0
            elif newBrightnessLv < 0.0:
                newBrightnessLv = 0.0

            # Convertir de nuevo a escala 0-100 para sbcontrol
            target_brightness = int(100 * newBrightnessLv)

            # Para evitar llamadas excesivas o rápidas que puedan causar problemas
            # Si el cambio es muy pequeño, quizás no aplicarlo.
            if abs(target_brightness - currentBrightnessLv[0]) > 2: # Solo cambiar si es un cambio significativo
                sbcontrol.set_brightness(target_brightness, display=0)
                print(f"DEBUG Brillo: Cambiando brillo a {target_brightness}%")
            # else:
            #     print(f"DEBUG Brillo: Cambio de brillo insignificante ({target_brightness}%)")

        except sbcontrol.ScreenBrightnessError as e:
            print(f"ERROR Brillo: No se pudo cambiar el brillo de la pantalla. {e}")
            print("Posiblemente necesites ejecutar como administrador o verificar permisos.")
        except Exception as e:
            print(f"ERROR Brillo: Ocurrió un error inesperado al cambiar el brillo: {e}")


    def changesystemvolume():
        """Ajusta el volumen del sistema según el valor de `Controller.pinchlv`."""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            currentVolumeLv = volume.GetMasterVolumeLevelScalar()
            # print(f"DEBUG Volumen: Volumen actual: {round(currentVolumeLv * 100, 2)}%")

            change_amount = Controller.pinchlv / 50.0 # Ajusta este factor para mayor o menor sensibilidad
            newVolumeLv = currentVolumeLv + change_amount

            if newVolumeLv > 1.0:
                newVolumeLv = 1.0
            elif newVolumeLv < 0.0:
                newVolumeLv = 0.0

            # Solo cambiar si el cambio es significativo o si hay una gran diferencia
            if abs(newVolumeLv - currentVolumeLv) > 0.01: # Cambiar si el delta es más del 1%
                volume.SetMasterVolumeLevelScalar(newVolumeLv, None)
                print(f"DEBUG Volumen: Cambiando volumen a {round(newVolumeLv * 100, 2)}%")
            # else:
            #     print(f"DEBUG Volumen: Cambio de volumen insignificante ({round(newVolumeLv * 100, 2)}%)")

        except Exception as e:
            print(f"ERROR Volumen: Ocurrió un error al cambiar el volumen: {e}")


    def scrollVertical():
        """Realiza un desplazamiento vertical en pantalla."""
        try:
            # Ajusta el valor 120 para mayor o menor velocidad de scroll
            scroll_amount = 120 if Controller.pinchlv > 0.0 else -120
            pyautogui.scroll(scroll_amount)
            print(f"DEBUG Scroll: Desplazamiento vertical: {scroll_amount}")
        except Exception as e:
            print(f"ERROR Scroll Vertical: {e}")


    def scrollHorizontal():
        """Realiza un desplazamiento horizontal en pantalla."""
        try:
            pyautogui.keyDown('shift') # Shift para scroll horizontal en muchas aplicaciones
            scroll_amount = -120 if Controller.pinchlv > 0.0 else 120 # Invertido para que sea intuitivo
            pyautogui.scroll(scroll_amount)
            pyautogui.keyUp('shift')
            print(f"DEBUG Scroll: Desplazamiento horizontal: {scroll_amount}")
        except Exception as e:
            print(f"ERROR Scroll Horizontal: {e}")

    def get_position(hand_result):
        """
        Devuelve las coordenadas actuales de la posición de la mano.
        Localiza la mano para obtener la posición del cursor y estabiliza el cursor
        suavizando movimientos bruscos.
        """
        if not hand_result or not hand_result.landmark or len(hand_result.landmark) <= 8:
            return pyautogui.position()

        point = 8 # Landmark para la punta del dedo índice (comúnmente usado para el cursor)

        position = [hand_result.landmark[point].x, hand_result.landmark[point].y]
        sx, sy = pyautogui.size()
        x_old, y_old = pyautogui.position()

        x = int(position[0] * sx)
        y = int(position[1] * sy)

        if Controller.prev_hand is None:
            Controller.prev_hand = x, y
            return (x_old, y_old)

        delta_x = x - Controller.prev_hand[0]
        delta_y = y - Controller.prev_hand[1]

        distsq = delta_x**2 + delta_y**2
        ratio = 1
        Controller.prev_hand = [x, y]

        if distsq <= 25:
            ratio = 0
        elif distsq <= 900:
            ratio = 0.07 * (distsq ** (1 / 2))
        else:
            ratio = 2.1

        final_x, final_y = x_old + delta_x * ratio, y_old + delta_y * ratio

        return (final_x, final_y)

    def pinch_control_init(hand_result):
        """Inicializa los atributos para el gesto de pinza."""
        if not hand_result or not hand_result.landmark or len(hand_result.landmark) <= 8:
            return

        Controller.pinchstartxcoord = hand_result.landmark[8].x
        Controller.pinchstartycoord = hand_result.landmark[8].y
        Controller.pinchlv = 0
        Controller.prevpinchlv = 0
        Controller.framecount = 0
        print("DEBUG Pinch: Pinch control inicializado.")


    def pinch_control(hand_result, controlHorizontal, controlVertical):
        """
        Llama a `controlHorizontal` o `controlVertical` según el movimiento del gesto de pinza.
        """
        if not hand_result or not hand_result.landmark or len(hand_result.landmark) <= 8:
            return

        # Ajuste: el framecount debería ser el número de frames para estabilizar el valor de pinchlv,
        # no para disparar la acción. La acción debe dispararse continuamente mientras el gesto se mantiene
        # y hay un cambio significativo en pinchlv.
        # Simplificamos la lógica para que la acción se dispare cada vez que el pinchlv cambie y haya pasado un mínimo de frames.

        lvx = Controller.getpinchxlv(hand_result)
        lvy = Controller.getpinchylv(hand_result)

        # Determinar la dirección dominante del pinch
        current_pinch_direction_flag = None # False para Y, True para X
        current_pinch_value = 0

        if abs(lvy) > abs(lvx) and abs(lvy) > Controller.pinch_threshold:
            current_pinch_direction_flag = False # Vertical
            current_pinch_value = lvy
        elif abs(lvx) > Controller.pinch_threshold:
            current_pinch_direction_flag = True # Horizontal
            current_pinch_value = lvx

        # Solo si hay un cambio significativo en la dirección o el valor
        if current_pinch_direction_flag is not None:
            if Controller.pinchdirectionflag is None or \
               current_pinch_direction_flag != Controller.pinchdirectionflag or \
               abs(Controller.prevpinchlv - current_pinch_value) >= Controller.pinch_threshold:

                Controller.pinchdirectionflag = current_pinch_direction_flag
                Controller.prevpinchlv = current_pinch_value
                Controller.pinchlv = current_pinch_value
                Controller.framecount = 0 # Resetear framecount para un nuevo movimiento significativo

                # Disparar la acción inmediatamente al detectar un cambio significativo
                if Controller.pinchdirectionflag:
                    controlHorizontal()
                else:
                    controlVertical()
            else:
                Controller.framecount += 1 # Incrementar framecount si el valor no ha cambiado significativamente
        else:
            # Si no hay movimiento de pinch significativo, pero la bandera aún está activa,
            # podríamos querer resetear o al menos no hacer nada.
            Controller.framecount = 0 # Reseteamos el framecount si el pinch no es activo


    def handle_controls(gesture, hand_result):
        """Implementa la funcionalidad para todos los gestos detectados."""

        # print(f"DEBUG: Gesto recibido en handle_controls: {gesture.name}") # Para depuración

        x, y = None, None

        # Obtener posición solo si el gesto es para mover el cursor
        if gesture == Gest.ONE:
            x, y = Controller.get_position(hand_result)
            safe_move_to(x, y, duration=0.01) # Mover el cursor continuamente
        else:
            # Si el gesto no es para mover el cursor, reiniciamos prev_hand
            Controller.prev_hand = None

        # Reinicio de banderas: Muy importante para evitar acciones continuas o no deseadas.
        # Las banderas se deben resetear si el gesto actual NO es el que las usa.

        if gesture != Gest.TWO_UP and Controller.grabflag:
            Controller.grabflag = False

        if gesture not in [Gest.PEACE, Gest.THREE] and Controller.flag:
            Controller.flag = False

        if gesture != Gest.FOUR and Controller.scrollflag:
            Controller.scrollflag = False
            # print("DEBUG: scrollflag reseteada.")

        if gesture != Gest.OK and Controller.pinchmajorflag:
            Controller.pinchmajorflag = False
            # print("DEBUG: pinchmajorflag reseteada.")
            # Reiniciar los valores de pinch al soltar el gesto OK
            Controller.pinchstartxcoord = None
            Controller.pinchstartycoord = None
            Controller.pinchlv = 0
            Controller.prevpinchlv = 0
            Controller.framecount = 0
            Controller.pinchdirectionflag = None


        # Implementación de gestos con los nuevos mapeos
        # Las acciones que solo deben ocurrir una vez por gesto
        if gesture == Gest.PEACE: # Click izquierdo con PEACE
            if not Controller.flag:
                pyautogui.click(button="left")
                Controller.flag = True
                print("DEBUG: Click izquierdo disparado (PEACE).")

        elif gesture == Gest.THREE: # Click derecho con THREE
            if not Controller.flag:
                pyautogui.click(button='right')
                Controller.flag = True
                print("DEBUG: Click derecho disparado (THREE).")

        elif gesture == Gest.FIST: # FIST (Puño cerrado) - Ya no hace nada.
            pass # No hacer nada para el gesto FIST

        elif gesture == Gest.TWO_UP: # Doble click izquierdo con TWO_UP
            if not Controller.grabflag:
                pyautogui.doubleClick()
                Controller.grabflag = True
                print("DEBUG: Doble click disparado (TWO_UP).")

        # Acciones continuas (pinch controls)
        elif gesture == Gest.FOUR: # Scroll con FOUR
            if not Controller.scrollflag:
                Controller.pinch_control_init(hand_result)
                Controller.scrollflag = True
                print("DEBUG: Inicio de scroll con Gest.FOUR")
            Controller.pinch_control(hand_result, Controller.scrollHorizontal, Controller.scrollVertical)

        elif gesture == Gest.OK: # Control de brillo/volumen con OK
            if not Controller.pinchmajorflag:
                Controller.pinch_control_init(hand_result)
                Controller.pinchmajorflag = True
                print("DEBUG: Inicio de control de brillo/volumen con Gest.OK")
            Controller.pinch_control(hand_result, Controller.changesystembrightness, Controller.changesystemvolume)