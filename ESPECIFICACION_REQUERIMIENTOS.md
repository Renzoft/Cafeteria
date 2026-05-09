# Documento de Especificación de Requerimientos - Rico Destino

## 1. Introducción
**Rico Destino** es un sistema integral de gestión de reservas para una cafetería premium. El objetivo principal es proporcionar una experiencia de usuario fluida, visualmente atractiva y optimizada para dispositivos móviles, permitiendo a los clientes realizar pedidos y a los administradores gestionar la operación en tiempo real.

## 2. Usuarios del Sistema
*   **Cliente**: Usuario registrado que puede navegar por el menú, gestionar su carrito, realizar reservas y consultar sus comprobantes digitales.
*   **Administrador**: Personal de la cafetería con acceso al panel de control para gestionar stock, productos, usuarios y monitorear pedidos en tiempo real.

## 3. Requerimientos Funcionales

### 3.1 Gestión de Usuarios y Perfiles
*   **RF01 - Registro de Usuarios**: El sistema debe permitir el registro de nuevos clientes solicitando datos personales básicos.
*   **RF02 - Autenticación**: El sistema debe permitir el inicio y cierre de sesión seguro.
*   **RF03 - Gestión de Perfil**: El usuario puede actualizar su información personal (foto, teléfono, dirección, fecha de nacimiento).
*   **RF04 - Multilogin Independiente**: El sistema debe permitir que un administrador mantenga una sesión abierta en el panel de control y una sesión de cliente en el sitio público de forma simultánea e independiente en el mismo navegador.

### 3.2 Catálogo y Carrito de Compras
*   **RF05 - Visualización de Menú**: Los productos deben estar organizados por categorías dinámicas con un diseño adaptable.
*   **RF06 - Carrito Persistente**: El carrito de compras debe guardarse en la base de datos vinculado a la cuenta del usuario.
*   **RF07 - Validación de Disponibilidad**: El sistema no debe permitir agregar productos al carrito que no tengan stock disponible.

### 3.3 Gestión de Reservas y Comprobantes
*   **RF08 - Creación de Reserva**: El usuario puede confirmar su reserva desde el carrito, la cual se registrará con estado "Pendiente".
*   **RF09 - Historial de Pedidos**: Los usuarios pueden consultar sus pedidos con tablas responsivas optimizadas para móviles.
*   **RF10 - Generación de QR**: Al crear una reserva, el sistema genera automáticamente un código QR único vinculado a un comprobante digital.
*   **RF11 - Comprobante Digital Público**: Vista de solo lectura accesible mediante un token UUID (sin login) que funciona como recibo digital para validar el pedido en el local.

### 3.4 Sistema de Notificaciones en Tiempo Real (Admin)
*   **RF12 - Monitor de Pedidos**: El administrador debe contar con una vista dedicada que se actualice automáticamente cada 30 segundos.
*   **RF13 - Notificaciones Visuales y Sonoras**: El sistema debe emitir alertas (Toasts y sonido) al detectar nuevos pedidos.
*   **RF14 - Indicadores de Sidebar**: Resaltado visual y badges con el conteo de órdenes pendientes en el panel administrativo.

### 3.5 Administración y Stock
*   **RF15 - Gestión de Inventario**: Descuento automático de stock al confirmar reserva y restauración al cancelar/eliminar.
*   **RF16 - UI de Administración Simplificada**: Formularios optimizados que presentan solo acciones esenciales (Guardar, Eliminar, Histórico).

## 4. Requerimientos No Funcionales

### 4.1 Interfaz de Usuario (UI) y Experiencia (UX)
*   **RNF01 - Estética Premium**: Interfaz moderna con temática de cafetería (#6f4e37, #ffc107) y micro-animaciones CSS.
*   **RNF02 - Diseño Mobile-First**: Optimización agresiva para dispositivos móviles, incluyendo tablas con desplazamiento horizontal y navegación simplificada.
*   **RNF03 - Accesibilidad Táctil**: Botones y campos de entrada con dimensiones adecuadas para interacción táctil.

### 4.2 Seguridad y Sesiones
*   **RNF04 - Aislamiento de Pestañas**: Uso de `sessionStorage` para asegurar que las sesiones de usuario no persistan entre pestañas diferentes, reforzando la seguridad en dispositivos compartidos.
*   **RNF05 - Tokens de Acceso**: Uso de UUIDs para el acceso seguro a comprobantes digitales públicos sin requerir credenciales.

### 4.3 Rendimiento
*   **RNF06 - Actualización Asíncrona**: Uso de AJAX/Fetch para el monitoreo de pedidos sin refrescar la página.

## 5. Tecnologías Utilizadas
*   **Backend**: Django (Python).
*   **Frontend**: HTML5, Vanilla JavaScript, Bootstrap 5.3+.
*   **Librerías**: `qrcode` (generación de QR), `Jazzmin` (Admin UI).
*   **Base de Datos**: SQLite3.