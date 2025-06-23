# 🖐️ Control por Gestos Basado en Visión Artificial

## Descripción del Proyecto

El proyecto "Control por Gestos Basado en Visión Artificial" tiene como objetivo desarrollar un sistema que permita a los usuarios interactuar con dispositivos mediante gestos de la mano, reemplazando los métodos tradicionales de entrada como el teclado y el ratón. Este sistema utiliza técnicas avanzadas de visión artificial y aprendizaje profundo para detectar y clasificar gestos en tiempo real, proporcionando una alternativa intuitiva y accesible para la interacción humano-computadora.

## Estudiante

- **Nombre:** Miguel Angel Choque Garcia
- **Carrera:** Ingeniería en Ciencias de la Computación
- **Universidad:** Universidad Mayor Real y Pontificia San Francisco Xavier de Chuquisaca
- **Materia:** SIS330 Desarrollo de Aplicaciones Inteligentes
- **Semestre:** Septimo
- **Docente:** Ing. Walter Pacheco

## 📬 Contacto

📌 Encuéntrame en:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/miguel-choque-garcia/)

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mickychog)

📧 **Correo:** [choque.garcia.miguelangel@usfx.bo](mailto:choque.garcia.miguelangel@usfx.bo)

## 📚 Artículo Científico Final

📄 El documento completo del proyecto se encuentra en la carpeta `Documents/Control-por-Gestos-Basado-en-Vision-Artificial.pdf`.

Este artículo científico presenta:

- Un **resumen ejecutivo** del sistema de control por gestos.
- Una descripción detallada de la **metodología**, basada en técnicas de visión artificial y aprendizaje profundo.
- Los **resultados obtenidos**, incluyendo una precisión superior al 95% en la clasificación de gestos.
- Las **conclusiones y recomendaciones** para futuras mejoras del sistema.

📥 [Descargar documento del proyecto ](Documents/Control-por-Gestos-Basado-en-Vision-Artificial.pdf)

## ¿Cómo Funciona el Proyecto? 🤔

¡Bienvenido a la sección donde te explicamos cómo funciona este emocionante proyecto de Control por Gestos Basado en Visión Artificial! 🌟 Aquí te cuento de una manera sencilla para que puedas entenderlo.

### 1. Captura de Video 📹

Todo comienza cuando enciendes la cámara web de tu computadora. 📸 Nuestra aplicación captura el video en tiempo real, lo que significa que ve todo lo que la cámara ve, ¡justo en el momento en que ocurre!

<!-- ![Captura de Video](images/captura_video.png) -->

### 2. Detección de Manos 🖐️

Una vez que la cámara está encendida, nuestro sistema utiliza una tecnología llamada MediaPipe Hands para detectar tus manos en el video. 🤲 MediaPipe es como un mago que puede encontrar y seguir tus manos en cada cuadro del video, identificando puntos clave en tus dedos y palmas.

<!-- ![Detección de Manos](images/deteccion_manos.png) -->

### 3. Clasificación de Gestos ✋

Aquí es donde entra en juego la inteligencia artificial. 🧠 Utilizamos un modelo llamado Vision Transformer (ViT), que es como un cerebro entrenado para reconocer diferentes gestos de la mano. 🤟 Este modelo ha sido entrenado con miles de imágenes de gestos, por lo que puede decirte qué gesto estás haciendo en tiempo real.

Por ejemplo, si levantas tu dedo índice, el modelo puede reconocer que estás haciendo el gesto de "señalar". 👆 Si levantas dos dedos, puede reconocer el gesto de "paz". ✌️

<!-- ![Clasificación de Gestos](images/clasificacion_gestos.png) -->

### 4. Mapeo de Gestos a Acciones 🖱️

Una vez que el modelo ha clasificado el gesto, nuestro sistema traduce ese gesto en una acción específica en tu computadora. 💻 Por ejemplo:

- **Movimiento del Cursor:** Si mueves tu dedo índice, el cursor en la pantalla se moverá en la misma dirección. 🖱️
- **Clic Izquierdo:** Si haces el gesto de "paz" (dedo índice y medio levantados), el sistema realizará un clic izquierdo. ✌️
- **Clic Derecho:** Si levantas tres dedos, el sistema realizará un clic derecho. 👌
- **Doble Clic:** Si haces dos dedos juntos (indice y medio), el sistema realizará un doble clic. 👊
- **Ajustar brillo-Volumen:** Si haces el gesto de "ok" (dedo índice y pulgar formando un círculo), podrás ajustar el brillo y volumen del sistema. 👌
- **Scroll:** Si levantas cuatro dedos y mueves tu dedo índice hacia arriba o abajo, podrás desplazarte por la pantalla. 👆👇

<!-- ![Mapeo de Gestos](images/mapeo_gestos.png) -->

### 5. Interacción en Tiempo Real ⏱️

Todo este proceso ocurre en tiempo real, lo que significa que no hay retrasos perceptibles entre el momento en que haces un gesto y el momento en que la acción se realiza en la pantalla. ⚡ Esto hace que la experiencia sea fluida y natural, como si estuvieras usando un ratón invisible. 🖱️👻

¡Y eso es todo! 🎉 Ahora ya sabes cómo funciona este proyecto de Control por Gestos Basado en Visión Artificial. Espero que te haya gustado y que te animes a probarlo. ¡Diviértete interactuando con tu computadora de una manera completamente nueva! 🚀

<img src="https://github.com/mickychog/control_por_gestos/blob/main/Images/ejemplo.png" alt="Ejemplo" width="700" height="450"/>

## 🛠️ Tecnologías Utilizadas:

- **Python**
- **Vision Transformer (ViT)** - Modelo de clasificación de imágenes
- **MediaPipe Hands** - Detección de puntos clave en las manos
- **OpenCV** - Captura y procesamiento de video
- **PyAutoGUI** - Automatización de acciones del sistema operativo
- **PyTorch & Transformers** - Entrenamiento e inferencia del modelo

## Instalación

1. **Clonar el Repositorio 📂:**
   Primero, necesitas clonar el repositorio del proyecto desde GitHub. Abre tu terminal o línea de comandos y ejecuta:

   ```bash
   git clone https://github.com/mickychog/control_por_gestos.git
   cd control_por_gestos
   ```

2. **Crear un Entorno Virtual 🌐:**
   Es una buena práctica crear un entorno virtual para manejar las dependencias del proyecto. Ejecuta el siguiente comando para crear un entorno virtual llamado gest:

   ```bash
   python -m venv gest
   ```

3. **Activar el Entorno Virtual 🔌:**
   Ahora, activa el entorno virtual. El comando depende de tu sistema operativo:

   ```bash
   gest\Scripts\activate
   ```

4. **Instalar las Dependencias 📦:**
   Con el entorno virtual activo, instala las dependencias necesarias utilizando pip. Asegúrate de tener un archivo requirements.txt en el directorio del proyecto. Ejecuta el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```

5. **Descargar el Modelo 🤖:**
   Necesitarás descargar el modelo preentrenado para que el sistema funcione correctamente. Descarga el modelo desde el siguiente enlace y colócalo en el directorio models/ dentro del proyecto.
   [Modelo Preentrenado (model.safetensors)](https://drive.google.com/file/d/1sBTnkokPKcaYf9HjFDjU3fdn64dDCEEl/view?usp=sharing)

6. **Ejecutar el Proyecto 🏃**
   Finalmente, puedes ejecutar el proyecto principal. Asegúrate de estar en el directorio del proyecto y ejecuta el archivo principal del proyecto.En este caso el archivo principal se llama gui.py, usa el siguiente comando:

   ```bash
   python gui.py
   ```

7. **Solución de Problemas 🛠️**
   Si encuentras algún problema durante la instalación, aquí tienes algunos consejos:

- Error al activar el entorno virtual: Asegúrate de que estás utilizando la versión correcta de Python y que el entorno virtual se creó correctamente.

- Problemas con las dependencias: Verifica que el archivo requirements.txt esté completo y que todas las dependencias se instalen sin errores.

- Error al descargar el modelo: Asegúrate de tener una conexión a internet estable y de que el enlace de descarga sea correcto.

## Estructura del proyecto

```bash
control_por_gestos/
├── 📁 config/
│ └── settings.py
│
├── 📁 models/
│ └── model.safetensors
│
├── 📁 src/
│ ├── 📁 enums/
│ │  └── gesture_enums.py
│ ├── gesture_controller.py
│ ├── gesture_handlers.py
│ ├── hand_recognition.py
│
│
├── requirements.txt
├── README.md
├── .gitignore
└── gui.py
```

### Archivos Clave

- gui.py:

  - Función: Interfaz de Usuario (Frontend).
  - Descripción: Muestra la ventana principal de la aplicación, con controles para iniciar/detener la detección y una consola para ver los gestos reconocidos.

- gesture_controller.py:

  - Función: Controlador Principal (Backend de Visión).
  - Descripción: Gestiona la cámara, procesa fotogramas con MediaPipe Hands, y pasa los datos de la mano a hand_recognition.py para identificar gestos. Muestra la vista de la cámara en una pequeña ventana flotante y envía los gestos a gesture_handlers.py para la ejecución de acciones. Se comunica con gui.py a través de una cola de mensajes.

- hand_recognition.py:

  - Función: Reconocimiento de Gestos (IA/Lógica de ML).
  - Descripción: Recibe los puntos de referencia de la mano y utiliza el modelo model.safetensors (o lógica basada en reglas) para clasificar el tipo de gesto realizado (ej. FIST, PEACE, OK).

- gesture_handlers.py:

  - Función: Ejecutor de Acciones (Automatización).
  - Descripción: Contiene la lógica para traducir los gestos reconocidos en acciones del sistema (movimiento del ratón, clics, control de volumen/brillo, scroll) utilizando librerías como pyautogui, pycaw y screen_brightness_control. Implementa un sistema de banderas para asegurar que las acciones se disparen correctamente.

- enums/gesture_enums.py:

  - Función: Definiciones (Constantes).
  - Descripción: Define enumeraciones para los gestos (Gest) y las etiquetas de las manos (HLabel), lo que mejora la legibilidad y estandarización del código.

- config/settings.py:

  - Función: Configuración (Parámetros).
  - Descripción: Almacena parámetros configurables del sistema, como el índice de la cámara, umbrales de confianza para MediaPipe y el nombre de la ventana de visualización de la cámara.

- models/model.safetensors:

  - Función: Modelo de Machine Learning.
  - Descripción: Archivo que contiene el modelo entrenado para el reconocimiento de gestos, utilizado por hand_recognition.py para clasificar los gestos con mayor precisión.

## ✋ Gestos Implementados

- ONE (Dedo índice extendido): Mueve el cursor del ratón.
- PEACE (Dedos índice y medio extendidos): Click izquierdo del ratón.
- THREE (Tres dedos extendidos): Click derecho del ratón.
- TWO_UP (Dedos índice y pulgar extendidos, los demás doblados): Doble clic izquierdo del ratón.
- FOUR (Cuatro dedos extendidos): Activa el modo de scroll. Mueve la mano vertical u horizontalmente para desplazar la página.
- OK (Pulgar e índice en contacto, los demás extendidos): Activa el control de brillo/volumen. Mueve la mano verticalmente para ajustar el volumen y horizontalmente para el brillo.
- FIST (Puño cerrado): Sin acción asignada (neutral).
- PALM (Mano abierta): Sin acción asignada (neutral).
- CALL (Pulgar y meñique extendidos, los demás doblados): Sin acción asignada (neutral).
  <img src="Images/gestures.jpg" alt="Gestos" width="900" height="350"/>

## 🎥 Demostración

<img src="Images/demo.gif" alt="Demostracion" width="720" height="400"/>

## © Declaratoria de Autoría

Este trabajo es de autoría exclusiva de **Miguel Choque García**, estudiante de Ingeniería en Ciencias de la Computación de la **Universidad Mayor Real y Pontificia San Francisco Xavier de Chuquisaca**.

El proyecto **"Control por Gestos Basado en Visión Artificial"** fue desarrollado durante el año 2025 como parte del curso **SIS330 - Desarrollo de Aplicaciones Inteligentes**, bajo la orientación del docente **Ing. Walter Pacheco**.

Queda prohibida su reproducción total o parcial sin el consentimiento explícito del autor. Cualquier uso académico debe reconocer debidamente al autor y a la institución.

> _Este proyecto tiene fines académicos. Puede ser utilizado con fines de estudio, investigación y enseñanza siempre que se cite correctamente._

## 📜 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).  
Puedes usarlo, modificarlo y distribuirlo libremente, siempre que incluyas la debida atribución al autor original.
