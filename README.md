# Misión Órbita
 
## Descripción
Simulador básico de exploración espacial desarrollado en Python para el curso
Principios de Programación 1 (SOFT-01, sección SCV3) de la Universidad CENFOTEC.
El proyecto se construyó en tres avances:
- **Avance 1 – Preparación de la misión:** cuatro algoritmos independientes.
- **Avance 2 – Ejecución de la misión:** exploración científica y evaluación del regreso.
- **Avance 3 – Sistema integrado (entrega final):** un único programa, `mision_orbita.py`,
  que administra el ciclo completo de la misión: preparación, autorización, viaje de ida,
  exploración con bitácora, regreso y supervivencia, reporte final ordenado, menú principal
  e historial de misiones.
## Integrantes
- Josue Monge Miranda
## Estructura del repositorio
```
mision-orbita/
├── README.md
├── avance1/
├── avance2/
├── avance3/
│   └── mision_orbita.py
└── documentacion/
    ├── (documentos de los avances 1 y 2)
    └── avance3_mision_orbita.pdf
```
## Instrucciones de ejecución
Se necesita Python 3. Desde la carpeta del repositorio:
```
python avance3/mision_orbita.py
```
Todo se maneja por consola. Los datos numéricos se ingresan como enteros positivos y
solo se validan las opciones de los menús (destino, actividad y menú principal).
 
## Convenciones y estilos
- Variables y funciones en snake_case, con nombres descriptivos y en minúscula.
- Constantes en MAYÚSCULAS con guion bajo, declaradas al inicio del archivo; sin números
  mágicos en las fórmulas y con constantes de posición (por ejemplo `recursos[OXIGENO]`).
- Indentación de 4 espacios y espacios alrededor de los operadores.
- Encabezado en el archivo (archivo, curso, integrantes, fecha, versión y descripción).
- Un comentario antes de cada bloque lógico que explica el porqué de la decisión.
- Sin variables globales, diccionarios, `break`, `continue`, `lambda` ni importaciones;
  cada función que devuelve un valor tiene un único `return` al final.
- Commits con mensajes que describen el cambio realizado.
