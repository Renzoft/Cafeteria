# Documento de Especificación de Requerimientos - Rico Destino

## 1. Introducción
**Rico Destino** es un sistema integral de gestión de reservas para una cafetería premium. El objetivo principal es proporcionar una experiencia de usuario fluida y visualmente atractiva para que los clientes realicen pedidos y los administradores gestionen la operación del negocio en tiempo real.

## 2. Usuarios del Sistema
*   **Cliente**: Usuario registrado que puede navegar por el menú, gestionar su carrito y realizar reservas.
*   **Administrador**: Personal de la cafetería con acceso al panel de control para gestionar stock, productos, usuarios y monitorear pedidos en tiempo real.

## 3. Requerimientos Funcionales

### 3.1 Gestión de Usuarios y Perfiles
*   **RF01 - Registro de Usuarios**: El sistema debe permitir el registro de nuevos clientes solicitando datos personales básicos.
*   **RF02 - Autenticación**: El sistema debe permitir el inicio y cierre de sesión seguro.
*   **RF03 - Gestión de Perfil**: El usuario puede actualizar su información personal (foto, teléfono, dirección, fecha de nacimiento).
*   **RF04 - Multilogin Independiente**: El sistema debe permitir que un administrador mantenga una sesión abierta en el panel de control y una sesión de cliente en el sitio público de forma simultánea e independiente en el mismo navegador.

### 3.2 Catálogo y Carrito de Compras
*   **RF05 - Visualización de Menú**: Los productos deben estar organizados por categorías dinámicas.
*   **RF06 - Carrito Persistente**: El carrito de compras debe guardarse en la base de datos vinculado a la cuenta del usuario, manteniendo los productos incluso si se cierra la sesión.
*   **RF07 - Validación de Disponibilidad**: El sistema no debe permitir agregar productos al carrito que no tengan stock disponible.

### 3.3 Gestión de Reservas (Pedidos)
*   **RF08 - Creación de Reserva**: El usuario puede confirmar su reserva desde el carrito, la cual se registrará con estado "Pendiente".
*   **RF09 - Historial de Pedidos**: Los usuarios pueden consultar el estado de sus reservas anteriores y actuales.
*   **RF10 - Ciclo de Vida del Pedido**: Los estados permitidos son: Pendiente, Listo, Entregado y Cancelado.

### 3.4 Sistema de Notificaciones en Tiempo Real (Admin)
*   **RF11 - Monitor de Pedidos**: El administrador debe contar con una vista dedicada (`/admin/orders/order/monitor/`) que se actualice automáticamente cada 30 segundos sin refrescar la página.
*   **RF12 - Notificaciones Visuales**: El sistema debe mostrar mensajes emergentes (Toasts) al detectar un nuevo pedido.
*   **RF13 - Alerta Sonora**: El sistema debe emitir un sonido de notificación cuando ingrese un nuevo pedido.
*   **RF14 - Indicadores de Sidebar**: La barra lateral del admin debe resaltar el ítem "Monitor de Pedidos" con efectos visuales (pulsación ámbar) y mostrar badges con el conteo de órdenes pendientes.

### 3.5 Administración y Stock
*   **RF15 - Gestión de Inventario**: El sistema debe descontar stock automáticamente al confirmar una reserva y restaurarlo si el pedido es cancelado o eliminado.
*   **RF16 - UI de Administración Simplificada**: Los formularios de edición de pedidos deben presentar solo las acciones esenciales (Guardar, Eliminar, Histórico) para evitar redundancias.

## 4. Requerimientos No Funcionales

### 4.1 Interfaz de Usuario (UI) y Experiencia (UX)
*   **RNF01 - Estética Premium**: La interfaz debe seguir una temática de cafetería moderna con colores cálidos (#6f4e37, #ffc107), tarjetas redondeadas y micro-animaciones.
*   **RNF02 - Diseño Responsivo**: El sistema debe ser 100% funcional en dispositivos móviles, tablets y computadoras de escritorio.

### 4.2 Seguridad
*   **RNF03 - Aislamiento de Sesiones**: Las sesiones de administración deben usar una cookie dedicada (`admin_sessionid`) para evitar conflictos con la sesión de usuario final.
*   **RNF04 - Protección de Rutas**: Todas las vistas administrativas deben estar protegidas y ser accesibles únicamente por personal autorizado (staff).

### 4.3 Rendimiento y Disponibilidad
*   **RNF05 - Actualización Asíncrona**: El monitor de pedidos debe utilizar peticiones AJAX/Fetch para garantizar la fluidez del panel.

## 5. Tecnologías Utilizadas
*   **Backend**: Django (Python).
*   **Frontend**: HTML5, Vanilla JavaScript, Bootstrap 5.
*   **Admin UI**: Django-Jazzmin con personalización CSS.
*   **Base de Datos**: SQLite3 (desarrollo).