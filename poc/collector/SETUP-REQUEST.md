# Ficha técnica de preparación — PoC de Collector (solo lectura)

> Para el técnico/administrador del vCenter y XClarity del entorno de prueba. Es un formulario de llenado directo: cada campo corresponde exactamente a una variable de `.env.example`. Las contraseñas nunca se completan en este documento ni se envían por chat/correo — se entregan por un canal seguro (gestor de contraseñas) directamente a quien va a ejecutar `collector.py`.

## Qué va a hacer el script, en concreto

`collector.py` abre una sesión HTTPS contra tu vCenter y tu XClarity Administrator con una cuenta de solo lectura, hace un puñado de peticiones GET, y cierra. No escribe nada. Los endpoints exactos que toca son:

**vSphere (REST API, vía `VSPHERE_HOST`):**

| Método | Endpoint | Para qué |
| --- | --- | --- |
| POST | `/api/session` | Abrir sesión (autenticación) |
| GET | `/api/vcenter/cluster` | Listar clusters |
| GET | `/api/vcenter/host` | Listar hosts |
| GET | `/api/vcenter/host?filter.clusters={id}` | Hosts por cluster (relación `contains`) |
| GET | `/api/vcenter/vm` | Listar VMs |
| GET | `/api/vcenter/vm?filter.hosts={id}` | VMs por host (relación `runs_on`) |
| GET | `/api/vcenter/datastore` | Listar datastores |

**XClarity Administrator (REST API, vía `XCLARITY_HOST`):**

| Método | Endpoint | Para qué |
| --- | --- | --- |
| POST | `/login` | Abrir sesión (autenticación) |
| GET | `/nodes` | Listar servidores gestionados, con `health`/`powerStatus` |

Si hay un firewall o WAF entre la máquina donde corre el script y estos hosts, solo estos endpoints necesitan estar permitidos (todo por HTTPS, puerto 443 salvo que uses otro).

## Ficha a completar

### A. vCenter / vSphere

| Campo (variable en `.env`) | Valor a completar | Notas |
| --- | --- | --- |
| `VSPHERE_HOST` | `https://______________` | URL base del vCenter, sin ruta al final (ej. `https://vcenter.lab.local`) |
| Versión de vCenter/vSphere | `______________` | Necesario para saber si los endpoints de arriba están disponibles tal cual |
| `VSPHERE_USER` | `______________` | Usuario de la cuenta **dedicada**, no personal ni admin |
| `VSPHERE_PASSWORD` | (entregar por canal seguro, no aquí) | |
| Rol asignado a esa cuenta | `______________` | Ver mínimo requerido abajo |
| `VSPHERE_VERIFY_SSL` | `true` / `false` | `true` si el certificado del vCenter es válido/confiable; `false` **solo** si es autofirmado y aceptas el riesgo en este laboratorio |

**Permiso mínimo necesario para la cuenta de vCenter:** el rol predefinido **"Read-Only"** de vCenter, asignado a nivel de vCenter Server o del datacenter que se va a leer, es suficiente — ese rol ya incluye `System.View` y permisos de lectura sobre inventario (datacenters, clusters, hosts, VMs, datastores). No se necesita ningún permiso de `System.Write`, `VirtualMachine.*` de configuración, ni roles personalizados.

### B. Lenovo XClarity Administrator

| Campo (variable en `.env`) | Valor a completar | Notas |
| --- | --- | --- |
| `XCLARITY_HOST` | `https://______________` | URL base de XClarity Administrator |
| Versión de XClarity Administrator | `______________` | |
| `XCLARITY_USER` | `______________` | Usuario de la cuenta **dedicada** |
| `XCLARITY_PASSWORD` | (entregar por canal seguro, no aquí) | |
| Rol asignado a esa cuenta | `______________` | Ver mínimo requerido abajo |
| `XCLARITY_VERIFY_SSL` | `true` / `false` | Igual que arriba |

**Permiso mínimo necesario para la cuenta de XClarity:** rol **"lxc-supervisor"** o el rol de solo lectura/monitor equivalente en tu versión (nombre exacto varía por versión de XClarity) — necesita poder listar `/nodes` (inventario y salud de servidores gestionados), sin permisos de gestión de energía, firmware ni configuración.

### C. Conectividad (confirmar, no completar valores sensibles)

| Pregunta | Respuesta |
| --- | --- |
| ¿La máquina donde correré `collector.py` tiene alcance HTTPS directo a `VSPHERE_HOST` y `XCLARITY_HOST`? | Sí / No — si no, ¿qué hace falta (VPN, misma red, jump host)? |
| ¿Hay proxy HTTP/HTTPS de por medio? | Sí / No — si sí, indicar si el script necesita configuración de proxy adicional (no está implementado en esta PoC; avisar si es obligatorio) |
| ¿El certificado TLS de vCenter/XClarity es válido (CA reconocida) o autofirmado? | ______________ |
| Si es autofirmado, ¿pueden entregar el certificado CA en vez de usar `VERIFY_SSL=false`? | Sí / No |

### D. Alcance y ventana

| Campo | Valor |
| --- | --- |
| Alias no sensible del entorno (`TENANT_ALIAS`) | `______________` (ej. `lab-interno`) |
| Datacenter/cluster incluido en la prueba | `______________` (si aplica un subconjunto) |
| Ventana de ejecución autorizada | `______________` |

### E. Entorno donde se ejecuta el script

- Python 3.9+ instalado.
- Permiso para `pip install requests`.
- El script no requiere privilegios de administrador del sistema operativo, solo poder hacer peticiones HTTPS salientes.

## Qué NO se necesita

- Sin permisos de escritura, administración, energía o firmware en ninguna de las dos fuentes.
- Sin acceso a la interfaz web, solo a la API vía la cuenta de solo lectura.
- Sin instalación de nada persistente en vCenter, XClarity ni en la red del cliente.

## Al terminar

Revocar o desactivar ambas cuentas de prueba si no se van a reutilizar. El script no guarda ni imprime hostnames, IPs ni seriales — solo un resumen con conteos y alias no reversibles (ver `poc/README.md`).
