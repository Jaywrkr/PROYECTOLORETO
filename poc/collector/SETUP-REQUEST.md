# Solicitud de preparación — PoC de Collector (solo lectura)

> Enviar a quien administra el vCenter y el XClarity del entorno de prueba. Ninguna de las respuestas debe incluir contraseñas, tokens ni IPs sensibles por este medio — solo confirmaciones.

## Contexto breve

Vamos a ejecutar una prueba de solo lectura para ver si podemos leer inventario básico de infraestructura (VMs, hosts, servidores físicos) de forma automatizada, sin hacer ningún cambio. Es una prueba de concepto interna, no toca producción ni hace escritura.

## Lo que necesito que prepares

### 1. Cuenta de solo lectura en vCenter

- Cuenta dedicada (no una cuenta personal ni la de administrador).
- Rol con permisos de **solo lectura** a nivel de datacenter/cluster (sin permisos de creación, edición, eliminación ni ejecución de tareas).
- Confirmar: ¿qué versión de vCenter/vSphere es?
- Entregar usuario y contraseña por un canal seguro (gestor de contraseñas, no chat ni correo plano).

### 2. Cuenta de solo lectura en XClarity Administrator

- Cuenta dedicada con rol de solo lectura/monitor (sin permisos de gestión de firmware, energía ni configuración).
- Confirmar: ¿qué versión de XClarity Administrator es?
- Entregar usuario y contraseña por un canal seguro.

### 3. Conectividad

- Confirmar que la máquina donde voy a correr el script tiene alcance de red (HTTPS) hacia el vCenter y hacia el XClarity — misma red interna, VPN, o lo que ya tengan.
- Confirmar si usan certificado TLS propio/self-signed (para saber si hay que instalar una CA o usar verificación relajada solo en este laboratorio).
- Confirmar si hay proxy HTTP/HTTPS de por medio.

### 4. Alcance y ventana

- Confirmar el alcance: ¿todo el datacenter/cluster de laboratorio, o limitarlo a un subconjunto de VMs/hosts/servidores?
- Confirmar una ventana de tiempo para la prueba (aunque sea informal, para tener registro).
- Un alias no sensible para identificar este entorno en la documentación (ej. "lab-interno"), nunca el nombre real.

### 5. Entorno donde corre el script

- Python 3.9+ disponible en la máquina que va a ejecutar `collector.py`.
- Permiso para instalar la librería `requests` (`pip install requests`), si no está ya.

## Qué NO necesito

- No necesito permisos de escritura, administración ni cuentas con privilegios elevados.
- No necesito acceso a la interfaz web de vCenter/XClarity, solo a la API vía la cuenta de solo lectura.
- No voy a instalar nada persistente en el entorno; el script corre una vez y termina.

## Al terminar

Voy a revocar o pedir que revoquen las cuentas de prueba si no se van a seguir usando, y no voy a dejar ningún dato sensible (IP, hostname, serial) fuera del entorno de laboratorio — solo un resumen con conteos y alias.
