import math
from .enums.gesture_enums import Gest, HLabel

class HandRecog:

    def __init__(self, hand_label):
        self.finger = 0
        self.ori_gesture = Gest.PALM
        self.prev_gesture = Gest.PALM
        self.frame_count = 0
        self.hand_result = None
        self.hand_label = hand_label


    def update_hand_result(self, hand_result):
        self.hand_result = hand_result

    def get_signed_dist(self, point):
        if not self.hand_result or not self.hand_result.landmark or \
            point[0] >= len(self.hand_result.landmark) or point[1] >= len(self.hand_result.landmark): # Added bounds check
            return 0.0
        sign = -1
        if self.hand_result.landmark[point[0]].y < self.hand_result.landmark[point[1]].y:
            sign = 1
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x) ** 2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y) ** 2
        dist = math.sqrt(dist)
        return dist * sign

    def get_dist(self, point):
        if not self.hand_result or not self.hand_result.landmark or \
            point[0] >= len(self.hand_result.landmark) or point[1] >= len(self.hand_result.landmark): # Added bounds check
            return 0.0
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x) ** 2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y) ** 2
        dist = math.sqrt(dist)
        return dist

    def get_dz(self, point):
        """
        Calcula la diferencia absoluta en el eje Z entre dos puntos.
        """
        if not self.hand_result or not self.hand_result.landmark or \
            point[0] >= len(self.hand_result.landmark) or point[1] >= len(self.hand_result.landmark): # Added bounds check
            return 0.0
        return abs(self.hand_result.landmark[point[0]].z - self.hand_result.landmark[point[1]].z)

    def set_finger_state(self):
        """
        **Visión Artificial**: Actualiza el estado de los dedos
        Returns
        -------
        None
        """
        if not self.hand_result or not self.hand_result.landmark:
            return

        # Para los dedos Índice, Medio, Anular, Meñique (bits 1 al 4)
        points_four_fingers = [[8, 5, 0], [12, 9, 0], [16, 13, 0], [20, 17, 0]]
        self.finger = 0 # Reiniciamos el estado de los dedos

        # Lógica para el pulgar (bit 0):
        is_thumb_extended = False
        if self.hand_result.landmark and len(self.hand_result.landmark) > 4: # Asegurarse de que el landmark 4 exista
            thumb_tip_x = self.hand_result.landmark[4].x
            thumb_base_x = self.hand_result.landmark[2].x # Landmark 2 es la base del pulgar
            # Consideramos el pulgar extendido si su punta está significativamente alejada de la base del índice en el eje X
            # y también si la distancia entre la punta del pulgar y la base del índice es mayor a un umbral
            if self.hand_label == HLabel.MAJOR: # Mano derecha
                if thumb_tip_x < thumb_base_x and self.get_dist([4, 5]) > 0.07: # Ajustado el umbral para mayor precisión
                    is_thumb_extended = True
            else: # Mano izquierda
                if thumb_tip_x > thumb_base_x and self.get_dist([4, 5]) > 0.07: # Ajustado el umbral para mayor precisión
                    is_thumb_extended = True

        if is_thumb_extended:
            self.finger |= (1 << 0) # Bit 0 para el pulgar extendido

        # Índice (bit 1), Medio (bit 2), Anular (bit 3), Meñique (bit 4)
        finger_base_points = [5, 9, 13, 17] # Base de cada dedo: Índice, Medio, Anular, Meñique
        finger_tip_points = [8, 12, 16, 20] # Punta de cada dedo: Índice, Medio, Anular, Meñique

        for i in range(4): # Para índice, medio, anular, meñique
            # Asegurarse de que los landmarks existen antes de acceder a ellos
            if len(self.hand_result.landmark) > finger_tip_points[i] and \
                len(self.hand_result.landmark) > finger_base_points[i]:
                # Si la punta del dedo está por encima de su base en el eje Y (para manos orientadas hacia arriba)
                # o si la distancia entre la punta y la base es significativa.
                # Una heurística común es que la punta del dedo esté "arriba" de su base.
                if self.hand_result.landmark[finger_tip_points[i]].y < self.hand_result.landmark[finger_base_points[i]].y:
                    self.finger |= (1 << (i + 1)) # Asigna el bit correspondiente (1 para índice, 2 para medio, etc.)

        # print(f"Finger state: {bin(self.finger)}") # Para depuración


    def get_gesture(self):
        """
        **Visión Artificial**:Determina el gesto actual.
        """
        if not self.hand_result or not self.hand_result.landmark:
            return Gest.PALM

        current_gesture = Gest.UNKNOWN

        # GESTOS PREDETERMINADOS (basados en tu `finger` bitmask)
        # Recuerda que el bit 0 es el pulgar, bit 1 el índice, bit 2 el medio, bit 3 el anular, bit 4 el meñique.

        # FIST (Puño cerrado): Ningún dedo extendido (0b00000)
        if self.finger == 0b00000:
            current_gesture = Gest.FIST

        # ONE (Dedo índice): Solo índice extendido (0b00010)
        elif self.finger == 0b00010:
            current_gesture = Gest.ONE

        # PEACE (indice y dedo medio): Índice y medio extendidos (0b00110)
        # Este será ahora el gesto para click izquierdo
        elif self.finger == 0b00110:
            current_gesture = Gest.PEACE

        # THREE (Tres dedos): Índice, medio y anular extendidos (0b01110)
        elif self.finger == 0b01110:
            current_gesture = Gest.THREE

        # FOUR: Cuatro dedos extendidos (índice, medio, anular, meñique) (0b11110)
        elif self.finger == 0b11110:
            current_gesture = Gest.FOUR

        # PALM (Mano abierta): Todos los dedos extendidos (0b11111)
        elif self.finger == 0b11111:
            current_gesture = Gest.PALM

        # CALL (Pulgar y meñique extendidos): (0b10001)
        elif self.finger == 0b10001:
            current_gesture = Gest.CALL

        # TWO_UP (dedo indice y del medio arriba y cerrados):
        # Como se definió, esto es idéntico a PEACE en términos de dedos extendidos.
        # Necesitamos diferenciarlo si PEACE ya tiene una acción.
        # Si la definición de TWO_UP es "índice y medio extendidos, y los demás doblados",
        # entonces el bitmask es 0b00110. Si PEACE también es 0b00110, se superponen.
        # Para diferenciarlos, PEACE puede ser el gesto por defecto 0b00110
        # y TWO_UP podría requerir una condición adicional, como la distancia entre los dedos.
        # Si TWO_UP es simplemente la detección de 0b00110, y PEACE también lo es,
        # entonces el que se defina primero en la cadena `if/elif` será el que se detecte.
        # Dado que PEACE ya está definido como 0b00110 y ahora hará el click izquierdo,
        # TWO_UP también se basará en 0b00110 pero con una condición adicional.

        # GESTOS BASADOS EN DISTANCIA (más específicos, como OK y potencialmente TWO_UP)

        # OK (Pulgar e índice en contacto, otros extendidos):
        # Se verifica que los landmarks 4 (punta pulgar) y 8 (punta índice) existan
        if (self.hand_result and self.hand_result.landmark and
            len(self.hand_result.landmark) > 8 and len(self.hand_result.landmark) > 4):
            if self.get_dist([8, 4]) < 0.05: # Umbral de distancia para que el pulgar y el índice se consideren "tocando"
                # Opcional: Asegurarse de que los otros dedos estén doblados para un 'OK' clásico.
                # Si el 'OK' es con los otros dedos levantados (como 0b01110 para los últimos 3),
                # la condición sería `self.get_dist([8, 4]) < 0.05 and (self.finger & 0b01110) == 0b01110`
                # Pero en tu caso parece que OK es solo el círculo de pulgar e índice.
                # Si el gesto OK solo involucra que el pulgar y el índice se toquen y los otros dedos están doblados.
                # Esto significa que el bitmask debería ser 0b00000 o 0b00001 (pulgar si está extendido pero tocando).
                # La definición común de OK es pulgar e índice formando un círculo y los demás dedos extendidos.
                # Si es este el caso, el `self.finger` debería ser algo como 0b01110 (para los 3 dedos restantes extendidos)
                # O si los otros dedos están doblados, el `self.finger` podría ser 0b00001 (solo pulgar si está extendido al tocar)
                # o incluso 0b00000 si todos los dedos están esencialmente "doblados" o "en reposo"
                # excepto el pulgar y el índice que se tocan.
                # Dada la descripción original "Pulgar e índice en contacto, otros extendidos",
                # el bitmask para los otros tres dedos (medio, anular, meñique) debería ser 0b01110.
                # Sin embargo, en el código actual, el bitmask ya se usa para los gestos principales.
                # Si queremos que OK sea prioritario y más específico:
                if (self.finger & 0b01110) == 0b01110: # Si los 3 últimos dedos (medio, anular, meñique) están extendidos
                    current_gesture = Gest.OK
                # Si la definición de OK es pulgar e índice tocándose y los demás dedos están doblados,
                # entonces la condición sería: `self.get_dist([8, 4]) < 0.05 and (self.finger & 0b11100) == 0b00000`
                # Considerando la descripción de "OK" como Pulgar e índice en contacto, los otros extendidos.
                # El bitmask para (índice, medio, anular, meñique) con pulgar en bit 0:
                # 0b11111 (PALM)
                # 0b00010 (ONE)
                # 0b00110 (PEACE)
                # Para OK, la combinación de dedos extendidos con el pulgar e índice tocándose es lo que define el gesto.
                # Si la definición de OK es que el pulgar y el índice se tocan y los otros tres dedos están extendidos,
                # entonces el bitmask de los dedos (medio, anular, meñique) debería ser 0b01110.
                # Se usará la condición: si el pulgar y el índice están cerca Y los otros tres dedos están extendidos.
                # Bit 0 (pulgar), Bit 1 (índice), Bit 2 (medio), Bit 3 (anular), Bit 4 (meñique)
                # Para "OK" con pulgar e índice tocando y los otros TRES dedos extendidos (medio, anular, meñique):
                # self.finger debe tener los bits 2, 3 y 4 en 1.
                # (self.finger & 0b11100) verifica los bits del medio, anular y meñique.
                # Si esos bits son 0b11100 (es decir, medio, anular, meñique extendidos), entonces es OK.
                # Se priorizará la detección de OK si la distancia es pequeña y los otros dedos están extendidos.
                # Esto asume que el gesto OK clásico es con los otros 3 dedos extendidos.
                # Si es con los otros 3 doblados (como en el emoji), entonces el bitmask cambia.
                if (self.finger & 0b11100) == 0b11100: # Medio, Anular, Meñique extendidos
                    current_gesture = Gest.OK
        # Si la definición de OK es solo pulgar e índice tocándose y los demás doblados (como el emoji de OK),
        # entonces la condición sería: `self.get_dist([8, 4]) < 0.05 and (self.finger & 0b11110) == 0b00000` (pulgar y los 4 dedos doblados)
        # o `(self.finger & 0b11100) == 0b00000` (solo los 3 dedos doblados).
        # Para evitar el cierre, se ha añadido la verificación de existencia de landmarks antes de get_dist.

        # TWO_UP: Índice y medio extendidos (0b00110). Para diferenciar de PEACE,
        # podríamos requerir que la distancia entre las puntas del índice y el medio sea pequeña,
        # indicando que están "juntos".
        # PERO, el enunciado dice "dedo indice y del medio arriba y *cerrados*", lo cual es ambiguo.
        # Si "cerrados" significa cerca el uno del otro, podemos usar la distancia.
        # Si "cerrados" significa doblados, entraría en conflicto con "arriba" (extendidos).
        # Asumiendo "arriba" (extendidos) y "cerca" (juntos):
        # PEACE ya es 0b00110. Para que TWO_UP sea distinto, debe tener una condición extra.
        # Por ejemplo, si PEACE es solo índice y medio extendidos, y TWO_UP es índice y medio extendidos Y *cerca*.
        # Para este caso, redefiniremos PEACE y TWO_UP.
        # PEACE: Índice y Medio extendidos (0b00110), sin una condición de cercanía estricta.
        # TWO_UP: Índice y Medio extendidos (0b00110) Y distancia entre sus puntas es pequeña.

        if self.finger == 0b00110: # Índice y medio extendidos, otros doblados
            if self.get_dist([8, 12]) < 0.05: # Distancia entre punta del índice (8) y punta del medio (12) es pequeña
                current_gesture = Gest.TWO_UP
            else:
                current_gesture = Gest.PEACE # Si no están tan cerca, es PEACE

        # Lógica de estabilización del gesto (mantener el gesto por unos frames)
        if current_gesture == self.prev_gesture:
            self.frame_count += 1
        else:
            self.frame_count = 0

        self.prev_gesture = current_gesture

        if self.frame_count > 4: # Mantener el umbral de 4 frames para estabilidad
            self.ori_gesture = current_gesture
        return self.ori_gesture