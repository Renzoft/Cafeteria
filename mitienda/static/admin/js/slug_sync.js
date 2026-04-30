(function() {
    'use strict';
    document.addEventListener('DOMContentLoaded', function() {
        const nameInput = document.getElementById('id_name');
        const slugInput = document.getElementById('id_slug');

        // Sincronización de Slug
        if (nameInput && slugInput) {
            slugInput.readOnly = true;
            slugInput.style.backgroundColor = '#f4f4f4';
            slugInput.style.cursor = 'not-allowed';
            slugInput.title = 'El slug se genera automáticamente a partir del nombre';

            nameInput.addEventListener('input', function() {
                const slug = nameInput.value
                    .toLowerCase()
                    .normalize('NFD')
                    .replace(/[\u0300-\u036f]/g, '')
                    .replace(/[^a-z0-9 -]/g, '')
                    .trim()
                    .replace(/\s+/g, '-')
                    .replace(/-+/g, '-');
                
                slugInput.value = slug;
            });
        }

        // Previsualización de imagen en el admin
        const imageInput = document.getElementById('id_image');
        const previewImg = document.querySelector('.admin-image-preview');

        if (imageInput && previewImg) {
            imageInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewImg.src = e.target.result;
                    }
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }

        // =====================================================
        // Resaltar filtros activos y persistir selección
        // =====================================================
        const urlParams = new URLSearchParams(window.location.search);
        const filterSelects = document.querySelectorAll('select.search-filter');

        function syncFilters() {
            filterSelects.forEach(select => {
                // Buscar si alguna opción con data-name coincide con un parámetro actual de la URL
                let matched = false;
                const options = select.querySelectorAll('option[data-name]');

                for (let option of options) {
                    const dataName = option.getAttribute('data-name');
                    const optionValue = option.value;

                    if (dataName && optionValue) {
                        const urlVal = urlParams.get(dataName);
                        if (urlVal !== null) {
                            // Comparación flexible: decodificar ambos lados
                            const cleanUrlVal = decodeURIComponent(urlVal.replace(/\+/g, ' '));
                            const cleanOptVal = decodeURIComponent(optionValue.replace(/\+/g, ' '));

                            if (cleanUrlVal === cleanOptVal || 
                                cleanUrlVal.substring(0, 10) === cleanOptVal.substring(0, 10)) {
                                // Forzar selección nativa
                                select.value = optionValue;
                                option.selected = true;

                                // Forzar Select2 a actualizar su display
                                if (typeof jQuery !== 'undefined' && jQuery(select).data('select2')) {
                                    jQuery(select).val(optionValue).trigger('change.select2');
                                }

                                select.classList.add('filter-active');
                                matched = true;
                                break;
                            }
                        }
                    }
                }

                // También verificar filtros simples (category, available, etc.)
                if (!matched) {
                    const options2 = select.querySelectorAll('option[data-name]');
                    for (let option of options2) {
                        const dataName = option.getAttribute('data-name');
                        const optionValue = option.value;
                        if (dataName && optionValue && urlParams.get(dataName) === optionValue) {
                            select.value = optionValue;
                            option.selected = true;
                            if (typeof jQuery !== 'undefined' && jQuery(select).data('select2')) {
                                jQuery(select).val(optionValue).trigger('change.select2');
                            }
                            select.classList.add('filter-active');
                            matched = true;
                            break;
                        }
                    }
                }

                if (!matched) {
                    select.classList.remove('filter-active');
                }
            });
        }

        // Ejecutar la sincronización con múltiples intentos para ganarle a Select2
        syncFilters();
        setTimeout(syncFilters, 200);
        setTimeout(syncFilters, 600);
        setTimeout(syncFilters, 1200);

        // =====================================================
        // Botón de Limpiar Filtros
        // =====================================================
        const filterForm = document.getElementById('changelist-search');
        if (filterForm && window.location.search && !document.getElementById('clear-filters-btn')) {
            const clearBtn = document.createElement('a');
            clearBtn.id = 'clear-filters-btn';
            clearBtn.href = window.location.pathname;
            clearBtn.className = 'btn btn-outline-danger btn-sm';
            clearBtn.innerHTML = '<i class="fas fa-times"></i> Limpiar filtros aplicados';
            clearBtn.style.borderRadius = '6px';
            clearBtn.style.padding = '6px 15px';
            clearBtn.style.fontWeight = '600';
            clearBtn.style.whiteSpace = 'nowrap';

            const submitBtn = filterForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.parentNode.insertBefore(clearBtn, submitBtn.nextSibling);
            } else {
                filterForm.appendChild(clearBtn);
            }
        }
    });
})();
