Trabajo: Tarea 3 - Redes
Nombre: Alexa Annais Galaz Barahona
Carrera: Ingeniería Civil en Informática y Telecomunicaciones
Ramo: Redes de Computadores
Profesor: Miguel Contreras
Fecha: 01 de julio de 2025

Descripción General:
Esta tarea tiene como objetivo principal analizar e intervenir el tráfico generado por una aplicación cliente-servidor, utilizando herramientas como Scapy y Docker. Se busca evidenciar cómo un atacante puede interceptar, modificar o inyectar tráfico malicioso en una red sin cifrado, evaluando las consecuencias en el funcionamiento de un servicio de base de datos MySQL.

Estructura del Informe:
El informe se encuentra organizado en los siguientes capítulos:

Capítulo I: Descripción del protocolo MySQL y análisis de su comportamiento en una red cliente-servidor simulada con Docker.

Capítulo II: Implementación de scripts en Python con Scapy para interceptar, modificar o inyectar tráfico MySQL. Se detallan los comandos utilizados y las pruebas realizadas.

Capítulo III: Análisis de resultados obtenidos al ejecutar las intervenciones al tráfico. Se presentan evidencias visuales y se evalúa el impacto generado en el sistema.

Capítulo IV: Conclusiones generales y lecciones aprendidas durante la realización de la tarea, destacando la importancia de aplicar mecanismos de seguridad en servicios expuestos.

Archivos Incluidos:
- modificar_trafico.py: Script principal para interceptar y modificar paquetes MySQL en tiempo real.
- evidencia_script.png: Imagen que muestra la ejecución del script con Scapy.
- evidencia: Captura del código final del script modificar_trafico.py.
- Tarea_3.pdf: Informe completo con análisis, resultados, evidencias y conclusiones.


## Paso 1 – Crear y activar entorno virtual con Scapy

```bash
python3 -m venv scapy-venv
source scapy-venv/bin/activate
pip install scapy
```

*Nota:* Si usas scripts con `sudo`, ejecuta con ruta completa:  
```bash
sudo ./scapy-venv/bin/python nombre_script.py
```

---

## Paso 2 – Preparar contenedores Docker

Debes tener:

- Un contenedor servidor con MySQL (por ejemplo, imagen `mysql-servidor-per`)
- Un contenedor cliente con el comando `mysql` (por ejemplo, imagen `mysql-cliente-per`)
- Ambos conectados a una red llamada `mysql-net`

Para ver las interfaces activas de Docker:

```bash
ip link
```

Anota la interfaz `br-xxxxx` correspondiente a tu red `mysql-net` (por ejemplo `br-de64afa7851c`), ya que deberás usarla en los scripts.

---

## Paso 3 – Interceptar tráfico

### Script: `mi_script_scapy.py`

Este script escucha el tráfico MySQL (puerto 3306) y muestra los paquetes capturados:

```python
sniff(filter="tcp port 3306",prn=mostrar_paquete)
```

Ejecución:

```bash
sudo ./scapy-venv/bin/python mi_script_scapy.py
```

Mientras corre, ejecuta consultas desde el cliente Docker para generar tráfico.

---

## Paso 4 – Inyectar tráfico con Fuzzing

### Script: `inyeccion_fuzz.py`

Este script envía paquetes TCP al servidor MySQL con cargas malformadas (`@@@FAKE_SQL_COMMAND@@@`), simulando un ataque de fuzzing:

```bash
sudo ./scapy-venv/bin/python inyeccion_fuzz.py
```

Repite la ejecución varias veces y verifica si el servidor se ve afectado.

---

## Paso 5  Modificar trafico en tiempo real

### Script: `modificar_trafico.py`

Este script intercepta trafico que contiene comandos SQL enviados por el cliente y los modifica antes de reenviarlos al servidor MySQL. Se probaron tres tipos de modificación:

####  Modificación 1: Reemplazo de `UPDATE` por `DELETE`

```python
if b"UPDATE" in carga:
    nueva_carga = carga.replace(b"UPDATE", b"DELETE")
```

Transforma comandos `UPDATE` en `DELETE`, con el objetivo de alterar la lógica del cliente y provocar perdida de datos.

####  Modificación 2: Reemplazo de `UPDATE` por `DROP`

```python
elif b"UPDATE" in carga:
    nueva_carga = carga.replace(b"UPDATE", b"DROP")
```

Intenta ejecutar una instrucción `DROP`, aunque sin estructura válida no se espera un resultado efectivo. Es tal como prueba de reacción del servidor.

####  Modificación 3: Reemplazo con datos aleatorios (fuzzing)

```python
else:
    nueva_carga = os.urandom(len(carga))
```

Reemplaza completamente el contenido del paquete con datos aleatorios para simular corrupción o pruebas de fuzzing.

#### Ejecución:

```bash
sudo ./scapy-venv/bin/python modificar_trafico.py
```

Desde el cliente, realiza consultas `UPDATE` como esta:

```sql
UPDATE clientes SET nombre = "PRUEBA" WHERE id = 1;
```

Y observa como se modifican en tiempo real a comandos `DELETE`, `DROP` o se reemplazan por basura binaria. Los resultados pueden ser evaluados desde la consola MySQL o con herramientas como `tcpdump`.
## Capturas

Todas las imágenes de consola y resultados están en la carpeta `imagenes/`, e ilustran:

- Instalación de Scapy
- Interfaces Docker (`ip link`)
- Ejecución de cada script
- Tráfico capturado y modificado

---

## Resultado Esperado

Al final del proceso deberías tener:

- Evidencia de tráfico MySQL capturado.
- Inyecciones con comandos anómalos realizadas exitosamente.
- Al menos una modificación detectada (SELECT → DELETE).
- Scripts Scapy funcionales que puedes reutilizar o adaptar.

---


Notas Finales:
Todos los scripts fueron ejecutados en un entorno Linux Ubuntu dentro de una máquina virtual configurada con Docker. La red bridge y el contenedor del servidor MySQL fueron utilizados para emular un escenario realista de comunicación cliente-servidor. Las pruebas se realizaron con fines exclusivamente académicos, reforzando los conocimientos adquiridos en la asignatura de Redes de Computadores.

Fin del documento.
