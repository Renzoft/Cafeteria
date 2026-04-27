# Café Premium - Sistema de Reservas (Django)

Este es un proyecto monolítico desarrollado en Django, diseñado como un sistema moderno y estilizado para la gestión de reservas en una cafetería premium. Permite a los clientes registrados explorar un menú interactivo, agregar bebidas o alimentos a su carrito, y confirmar su reserva para recogerla y pagarla directamente en el local.

El sistema se distingue por una interfaz de usuario cálida y armónica, inspirada en las texturas y colores del café, desarrollada nativamente con Bootstrap 5 y optimizada para dispositivos móviles y de escritorio.

## Características Principales

*   **Interfaz Tematizada**: Diseño exclusivo "Coffee Shop" con paleta de colores cálida, tarjetas redondeadas y micro-animaciones (CSS puro).
*   **Catálogo Interactivo**: Listado dinámico de productos organizados por categorías.
*   **Carrito Persistente**: Sistema de carrito de compras integrado directamente a la base de datos que se vincula al iniciar sesión.
*   **Perfiles de Usuario Completos**: Registro y edición de perfil con foto, teléfono, fecha de nacimiento y dirección.
*   **Historial de Reservas**: Vista dedicada para que los usuarios puedan dar seguimiento al estado de sus pedidos (Pendiente, Listo, Entregado, Cancelado).
*   **Panel de Administración Moderno**: Impulsado por `django-jazzmin`, proporciona una interfaz de administración altamente intuitiva para gestionar productos, stock y usuarios.
*   **Seguridad y Sesiones**: Redirecciones protegidas y cierre de sesión estricto vinculado a las pestañas del navegador para maximizar la seguridad en equipos compartidos.

## Requisitos Previos

Asegúrate de tener instalado en tu sistema Windows:

*   [Python 3.10 o superior]
*   pip

## Instrucciones de Instalación y Ejecución (Exclusivo para Windows)

Sigue estos pasos detallados para levantar el proyecto en tu entorno local Windows.

### 1. Preparar el repositorio

Abre una terminal Bash (por ejemplo, **Git Bash**) y asegúrate de estar dentro de la carpeta raíz del proyecto (`Cafeteria_Django/`).

### 2. Crear y activar el entorno virtual

Es indispensable utilizar un entorno virtual para no afectar otras instalaciones de Python en tu sistema:

```bash
python -m venv my_env
source my_env/Scripts/activate
```
*(Sabrás que funcionó porque aparecerá `(my_env)` al principio de la línea en tu terminal).*

### 3. Instalar las dependencias

Con el entorno virtual activado, instala todos los paquetes necesarios requeridos por el sistema:

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

El proyecto utiliza un archivo `.env` para manejar la configuración. Crea un archivo llamado `.env` en la raíz del proyecto (en la misma carpeta donde está `manage.py`) y agrega el siguiente contenido:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-de-django-aqui
```

### 5. Aplicar las migraciones de la Base de Datos

El sistema usa SQLite3 por defecto. Prepara la base de datos creando las tablas necesarias:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear un administrador principal (Superusuario)

Para poder acceder al panel de administración y gestionar el catálogo y las reservas:

```bash
python manage.py createsuperuser
```
*(Sigue las instrucciones en consola para definir tu usuario y contraseña. Nota: la contraseña no se mostrará mientras la escribes).*

### 7. Ejecutar el Servidor

Inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

¡Listo! El servidor estará corriendo localmente y podrás acceder desde tu navegador.

## Enlaces Rápidos

*   **Página Principal (Redirige al Login)**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **Catálogo de la Cafetería**: [http://127.0.0.1:8000/tienda/](http://127.0.0.1:8000/tienda/)
*   **Panel de Administración (Jazzmin)**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
*   **Mi Perfil**: [http://127.0.0.1:8000/account/profile/](http://127.0.0.1:8000/account/profile/)
*   **Mis Reservas**: [http://127.0.0.1:8000/account/history/](http://127.0.0.1:8000/account/history/)
