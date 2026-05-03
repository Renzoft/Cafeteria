# Rico Destino - Sistema de Reservas

Este es un proyecto monolítico desarrollado en Django, diseñado como un sistema moderno y estilizado para la gestión de reservas en una cafetería premium. Permite a los clientes registrados explorar un menú interactivo, agregar bebidas o alimentos a su carrito, y confirmar su reserva para recogerla y pagarla directamente en el local.

El sistema se distingue por una interfaz de usuario cálida y armónica, inspirada en las texturas y colores del café, desarrollada nativamente con Bootstrap 5 y optimizada para dispositivos móviles y de escritorio.

## Características Principales

*   **Interfaz Tematizada**: Diseño exclusivo "Coffee Shop" con paleta de colores cálida, tarjetas redondeadas y micro-animaciones (CSS puro).
*   **Catálogo Interactivo**: Listado dinámico de productos organizados por categorías.
*   **Carrito Persistente**: Sistema de carrito de compras integrado directamente a la base de datos que se vincula al iniciar sesión.
*   **Perfiles de Usuario Completos**: Registro y edición de perfil con foto, teléfono, fecha de nacimiento y dirección.
*   **Historial de Reservas**: Vista dedicada para que los usuarios puedan dar seguimiento al estado de sus pedidos (Pendiente, Listo, Entregado, Cancelado).
*   **Sesiones Independientes (Multilogin)**: Middleware personalizado que permite mantener sesiones abiertas simultáneamente como administrador y como usuario en el mismo navegador, utilizando cookies separadas (`admin_sessionid` y `sessionid`).

## Sistema de Notificaciones en Tiempo Real (Admin)

El panel de administración cuenta con un robusto sistema de monitoreo en tiempo vivo:

*   **Monitor de Pedidos**: Panel dedicado accesible desde `/admin/orders/order/monitor/` que muestra las reservas entrantes sin necesidad de recargar la página.
*   **Alertas Visuales y Sonoras**: Notificaciones tipo *Toast* personalizadas y alertas sonoras al detectar nuevos pedidos.
*   **Sidebar Dinámico**: Resaltado visual (pulsación ámbar) y badges en la barra lateral del admin para indicar la cantidad de pedidos pendientes de revisión.
*   **API Integrada**: Sistema de polling optimizado que consulta el estado de las órdenes directamente desde el ecosistema del admin para mayor seguridad.

## Administración y UI/UX

*   **Panel Jazzmin Optimizado**: Interfaz administrativa moderna con estilos personalizados en `admin_styles.css`.
*   **Simplificación de Formularios**: Eliminación de botones redundantes en la edición de pedidos para un flujo de trabajo más directo (manteniendo solo Guardar, Eliminar e Histórico).
*   **Gestión de Stock**: Lógica automática para restaurar el stock de productos al cancelar o eliminar reservas.

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