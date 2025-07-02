
# Tarea 3 - Intervención de Tráfico MySQL con Scapy

Este proyecto demuestra cómo interceptar, inyectar y modificar tráfico MySQL entre un cliente y un servidor Docker utilizando Scapy. El objetivo es observar cómo reacciona el servicio ante tráfico inesperado o malicioso.

---

## Requisitos

- Python 3
- Docker
- Acceso sudo en tu sistema
- Git (opcional)

---

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

## Paso 5 – Modificar tráfico en tiempo real

### Script: `modificar_trafico.py`

Este script intercepta paquetes que contienen `SELECT` y los modifica a `DELETE` antes de reenviarlos.

```python
nueva_carga = carga.replace(b"SELECT", b"DELETE")
send(nuevo_pkt)
```

Ejecución:

```bash
sudo ./scapy-venv/bin/python modificar_trafico.py
```

Desde el cliente, ejecuta una consulta `SELECT` y observa cómo se transforma en `DELETE`.

---

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

## Notas adicionales

- Todos los scripts fueron probados en Ubuntu 22.04 sobre máquina virtual con Docker.
- Asegúrate de tener `sudo` para ejecutar los scripts con privilegios necesarios para capturar o enviar paquetes en red.

---
