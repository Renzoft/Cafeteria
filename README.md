# Rico Destino - Sistema de Reservas

Este es un proyecto monolítico desarrollado en Django, diseñado como un sistema moderno y estilizado para la gestión de reservas en una cafetería premium. Permite a los clientes registrados explorar un menú interactivo, agregar bebidas o alimentos a su carrito, y confirmar su reserva para recogerla y pagarla directamente en el local.

El sistema se distingue por una interfaz de usuario cálida y armónica, inspirada en las texturas y colores del café, desarrollada nativamente con Bootstrap 5 y optimizada para dispositivos móviles y de escritorio.

## Características Principales

*   **Interfaz Tematizada**: Diseño exclusivo "Coffee Shop" con paleta de colores cálida, tarjetas redondeadas y micro-animaciones (CSS puro).
*   **Diseño Mobile-First**: Interfaz 100% optimizada para dispositivos móviles con navegación simplificada, tablas con scroll horizontal y campos táctiles.
*   **Comprobantes Digitales (QR)**: Generación automática de códigos QR para cada reserva, permitiendo a los clientes acceder a un recibo digital público y seguro sin necesidad de iniciar sesión.
*   **Catálogo Interactivo**: Listado dinámico de productos organizados por categorías con carga optimizada.
*   **Carrito Persistente**: Sistema de carrito vinculado directamente a la base de datos para no perder la selección al cambiar de dispositivo.
*   **Perfiles de Usuario**: Gestión completa de información personal y preferencias.
*   **Historial de Reservas**: Seguimiento en tiempo real del estado de los pedidos (Pendiente, Listo, Entregado, Cancelado).
*   **Seguridad de Sesiones**: Aislamiento estricto de sesiones por pestaña del navegador (`sessionStorage`) y cookies independientes para administración.

## Sistema de Notificaciones en Tiempo Real (Admin)

El panel de administración cuenta con un robusto sistema de monitoreo en tiempo vivo:

*   **Monitor de Pedidos**: Panel dedicado que muestra las reservas entrantes sin necesidad de recargar la página (polling de 30s).
*   **Alertas Visuales y Sonoras**: Notificaciones tipo *Toast* y alertas sonoras al detectar nuevos pedidos.
*   **Sidebar Dinámico**: Resaltado visual (pulsación ámbar) y badges para pedidos pendientes.

## Administración y UI/UX

*   **Panel Jazzmin Optimizado**: Interfaz administrativa moderna y estilizada.
*   **Simplificación de Flujos**: Eliminación de botones redundantes en la edición de pedidos para mayor agilidad.
*   **Gestión de Stock Inteligente**: Restauración automática de stock al cancelar o eliminar reservas.

## Requisitos Previos

Asegúrate de tener instalado en tu sistema Windows:

*   [Python 3.10 o superior]
*   pip

## Instrucciones de Instalación y Ejecución (Exclusivo para Windows)

Sigue estos pasos detallados para levantar el proyecto en tu entorno local Windows.

### 1. Preparar el repositorio

Asegúrate de estar dentro de la carpeta raíz del proyecto (`Cafeteria_Django/`).

### 2. Crear y activar el entorno virtual

Es indispensable utilizar un entorno virtual para no afectar otras instalaciones de Python en tu sistema:

```bash
python -m venv my_env
source my_env\Scripts\activate
```

### 3. Instalar las dependencias

Con el entorno virtual activado, instala todos los paquetes necesarios:

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo llamado `.env` en la raíz del proyecto y agrega:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-de-django-aqui
```

### 5. Aplicar las migraciones

Prepara la base de datos creando las tablas necesarias:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Ejecutar el Servidor

Inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver
```