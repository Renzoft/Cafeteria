/**
 * Sistema de Notificaciones en Tiempo Real para el Panel de Administración
 * Rico Destino - Notificaciones de pedidos pendientes
 */

(function () {
    'use strict';

    // Configuración
    const POLLING_INTERVAL = 30000; // 30 segundos
    const API_URL = '/admin/orders/order/api/pending-count/';
    const MONITOR_URL = '/admin/orders/order/monitor/';
    const SOUND_URL = '/static/sounds/notification.mp3';

    let lastOrderId = null;
    let isFirstRun = true;

    // Inyectar estilos CSS directamente (evita problemas de carga/especificidad)
    function injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes notif-glow {
                0%, 100% { box-shadow: 0 0 8px rgba(255,193,7,0.4); }
                50% { box-shadow: 0 0 20px rgba(255,193,7,0.8); }
            }
            .monitor-alert-active {
                background: linear-gradient(135deg, #ffc107, #ffca2c) !important;
                color: #000 !important;
                font-weight: 800 !important;
                border-radius: 6px !important;
                animation: notif-glow 2s ease-in-out infinite !important;
                padding: 8px 12px !important;
                margin: 4px 8px !important;
            }
            .monitor-alert-active * {
                color: #000 !important;
                font-weight: 800 !important;
            }
            .monitor-alert-active .badge {
                background: #d63031 !important;
                color: #fff !important;
                font-weight: 700 !important;
                font-size: 11px !important;
                padding: 3px 8px !important;
                border-radius: 12px !important;
                animation: none !important;
            }
            .notif-toast-container {
                position: fixed;
                top: 15px;
                right: 15px;
                z-index: 99999;
                max-width: 380px;
                min-width: 340px;
            }
            .notif-toast-card {
                background: #fff;
                border-radius: 16px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.2);
                overflow: hidden;
                animation: slideInRight 0.4s ease-out;
                border-left: 5px solid #ffc107;
            }
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .notif-toast-header {
                background: linear-gradient(135deg, #ffc107, #ffca2c);
                padding: 12px 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .notif-toast-header h6 {
                margin: 0;
                font-weight: 800;
                color: #1a1a1a;
                font-size: 14px;
            }
            .notif-toast-close {
                background: none;
                border: none;
                font-size: 20px;
                color: #1a1a1a;
                cursor: pointer;
                line-height: 1;
                padding: 0 4px;
            }
            .notif-toast-body {
                padding: 16px;
            }
            .notif-toast-user {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 12px;
            }
            .notif-toast-avatar {
                width: 42px;
                height: 42px;
                border-radius: 50%;
                background: #fff3cd;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            .notif-toast-avatar i { color: #6f4e37; font-size: 18px; }
            .notif-toast-info strong { color: #4a3324; font-size: 15px; }
            .notif-toast-info small { color: #888; }
            .notif-toast-btn {
                display: block;
                width: 100%;
                padding: 10px;
                background: linear-gradient(135deg, #ffc107, #ffca2c);
                color: #1a1a1a !important;
                font-weight: 700;
                border: none;
                border-radius: 10px;
                text-align: center;
                text-decoration: none !important;
                font-size: 13px;
                transition: all 0.2s;
                cursor: pointer;
            }
            .notif-toast-btn:hover {
                background: linear-gradient(135deg, #e6ac00, #ffc107);
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(255,193,7,0.4);
            }
        `;
        document.head.appendChild(style);
    }

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function playNotificationSound() {
        const audio = new Audio(SOUND_URL);
        audio.play().catch(e => console.log("Audio bloqueado o archivo no encontrado:", e));
    }

    // Encontrar el enlace del Monitor en el sidebar (búsqueda robusta)
    function findMonitorLink() {
        // Buscar por texto en TODOS los enlaces del sidebar
        const allLinks = document.querySelectorAll('a');
        for (let link of allLinks) {
            const text = link.textContent.trim();
            if (text.includes('Monitor de Pedidos')) {
                return link;
            }
        }
        return null;
    }

    function showToast(orderId, userName) {
        // Eliminar toasts anteriores
        document.querySelectorAll('.notif-toast-container').forEach(el => el.remove());

        const container = document.createElement('div');
        container.className = 'notif-toast-container';
        container.innerHTML = `
            <div class="notif-toast-card">
                <div class="notif-toast-header">
                    <h6><i class="fas fa-mug-hot mr-2"></i> ¡Nuevo Pedido Entrante!</h6>
                    <button class="notif-toast-close" onclick="this.closest('.notif-toast-container').remove()">&times;</button>
                </div>
                <div class="notif-toast-body">
                    <div class="notif-toast-user">
                        <div class="notif-toast-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="notif-toast-info">
                            <strong>${userName}</strong><br>
                            <small>Pedido #${orderId}</small>
                        </div>
                    </div>
                    <a href="${MONITOR_URL}" class="notif-toast-btn">
                        <i class="fas fa-broadcast-tower mr-1"></i> Ir al Monitor en Vivo
                    </a>
                </div>
            </div>
        `;

        document.body.appendChild(container);

        // Auto-cerrar después de 12 segundos
        setTimeout(() => {
            if (container.parentNode) {
                container.style.transition = 'opacity 0.5s';
                container.style.opacity = '0';
                setTimeout(() => container.remove(), 500);
            }
        }, 12000);
    }

    function updateSidebarHighlight(count) {
        const monitorLink = findMonitorLink();
        if (!monitorLink) {
            console.log('Monitor link no encontrado en el sidebar');
            return;
        }

        if (count > 0) {
            // Activar resaltado
            monitorLink.classList.add('monitor-alert-active');

            // Actualizar o crear el badge
            let badge = monitorLink.querySelector('.badge-pending-notif');
            if (!badge) {
                badge = document.createElement('span');
                badge.className = 'badge badge-pending-notif ml-auto';
                badge.style.cssText = 'margin-left: auto;';
                monitorLink.appendChild(badge);
            }
            badge.textContent = count;
        } else {
            // Desactivar resaltado
            monitorLink.classList.remove('monitor-alert-active');
            const badge = monitorLink.querySelector('.badge-pending-notif');
            if (badge) badge.remove();
        }
    }

    // Actualiza el Monitor en Vivo si estamos en esa página
    function updateMonitorPage(data) {
        const list = document.getElementById('live-orders-list');
        const empty = document.getElementById('live-orders-empty');
        const updateTime = document.getElementById('last-update');

        if (!list) return;

        if (updateTime) {
            updateTime.textContent = `Última actualización: ${new Date().toLocaleTimeString()}`;
        }

        if (!data.orders || data.orders.length === 0) {
            list.classList.add('d-none');
            if (empty) empty.classList.remove('d-none');
        } else {
            if (empty) empty.classList.add('d-none');
            list.classList.remove('d-none');
            list.innerHTML = '';

            data.orders.forEach(order => {
                if (typeof renderOrderCard === 'function') {
                    list.insertAdjacentHTML('beforeend', renderOrderCard(order));
                }
            });
        }
    }

    async function checkUpdates() {
        try {
            const response = await fetch(API_URL, {
                method: 'GET',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });

            if (!response.ok) return;

            const data = await response.json();

            // Actualizar sidebar
            updateSidebarHighlight(data.count);

            // Actualizar monitor si estamos en esa página
            if (window.isMonitorPage) {
                updateMonitorPage(data);
            }

            // Primera ejecución: solo guardar el ID
            if (isFirstRun) {
                lastOrderId = data.last_id;
                isFirstRun = false;
                return;
            }

            // Nuevo pedido detectado
            if (data.last_id && data.last_id !== lastOrderId) {
                lastOrderId = data.last_id;
                playNotificationSound();
                showToast(data.last_id, data.last_user);
            }

        } catch (error) {
            console.error('Error en notificaciones:', error);
        }
    }

    // Función para ocultar botones redundantes en los formularios de cambio
    function hideRedundantButtons() {
        const selectors = [
            'input[name="_addanother"]',
            'button[name="_addanother"]',
            'input[name="_continue"]',
            'button[name="_continue"]',
            '.btn-info[name="_addanother"]',
            '.btn-info[name="_continue"]'
        ];
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => el.style.display = 'none');
        });
    }

    // Inicializar
    document.addEventListener('DOMContentLoaded', function () {
        injectStyles();
        checkUpdates();
        setInterval(checkUpdates, POLLING_INTERVAL);
        
        // Ejecutar ocultación de botones
        hideRedundantButtons();
        // Re-ejecutar tras un pequeño delay para manejar carga dinámica de Jazzmin
        setTimeout(hideRedundantButtons, 500);
        setTimeout(hideRedundantButtons, 2000);

        // Resaltar menú si estamos en la página del monitor
        if (window.isMonitorPage) {
            setTimeout(() => {
                const monitorLink = findMonitorLink();
                if (monitorLink) {
                    monitorLink.classList.add('active');
                    // También abrir el menú padre si es necesario
                    const parentMenu = monitorLink.closest('.nav-item.has-treeview');
                    if (parentMenu) parentMenu.classList.add('menu-open');
                }
            }, 500);
        }
    });

})();
