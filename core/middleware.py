from django.conf import settings

# Nombre de la cookie exclusiva para el admin
ADMIN_SESSION_COOKIE = 'admin_sessionid'


class SeparateAdminSessionMiddleware:
    """
    Middleware que mantiene sesiones completamente separadas entre el panel de
    administración (/admin/) y el sitio principal.

    - Admin usa la cookie:    'admin_sessionid'
    - Sitio normal usa:       'sessionid'

    Esto permite que el superadmin esté logueado en el admin mientras que
    otro usuario (o el mismo) esté logueado en el sitio en otra pestaña,
    sin que una sesión interfiera con la otra.

    IMPORTANTE: Este middleware debe colocarse ANTES de SessionMiddleware
    en la lista MIDDLEWARE de settings.py.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_admin = request.path.startswith('/admin/')

        if is_admin:
            # ── FASE REQUEST ──────────────────────────────────────────────
            # Antes de que SessionMiddleware lea la cookie, la intercambiamos:
            # Si existe una cookie de sesión de admin, la ponemos en el slot
            # estándar para que Django la procese normalmente.
            admin_cookie_value = request.COOKIES.get(ADMIN_SESSION_COOKIE)
            regular_cookie_value = request.COOKIES.get(settings.SESSION_COOKIE_NAME)

            if admin_cookie_value is not None:
                # Usar la sesión del admin
                request.COOKIES[settings.SESSION_COOKIE_NAME] = admin_cookie_value
            elif regular_cookie_value is not None:
                # No hay sesión de admin; eliminar la del usuario para que el
                # admin empiece con sesión limpia (evita el conflicto)
                del request.COOKIES[settings.SESSION_COOKIE_NAME]

        response = self.get_response(request)

        if is_admin:
            # ── FASE RESPONSE ─────────────────────────────────────────────
            # Después de que SessionMiddleware haya escrito la cookie estándar,
            # la renombramos a 'admin_sessionid' para no tocar la del usuario.
            if settings.SESSION_COOKIE_NAME in response.cookies:
                morsel = response.cookies[settings.SESSION_COOKIE_NAME]

                # Copiar la cookie bajo el nombre exclusivo del admin
                response.set_cookie(
                    ADMIN_SESSION_COOKIE,
                    morsel.value,
                    max_age=morsel.get('max-age') or None,
                    expires=morsel.get('expires') or None,
                    path='/',
                    domain=morsel.get('domain') or None,
                    secure=bool(morsel.get('secure')),
                    httponly=True,
                    samesite='Lax',
                )
                # Eliminar la cookie estándar de la respuesta del admin
                del response.cookies[settings.SESSION_COOKIE_NAME]

        return response
