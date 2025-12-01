// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-link');
    const navIndicator = document.querySelector('.nav-indicator');
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const currentYear = document.getElementById('current-year');
    const contactForm = document.querySelector('.contact-form');
    
    // Configurar año actual en el footer
    if (currentYear) {
        currentYear.textContent = new Date().getFullYear();
    }
    
    // ===== OBSERVER PARA ANIMACIONES =====
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.2
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Actualizar URL hash sin hacer scroll
                const id = entry.target.getAttribute('id');
                if (id && id !== 'inicio') {
                    history.replaceState(null, null, `#${id}`);
                } else {
                    history.replaceState(null, null, ' ');
                }
                
                // Actualizar enlace activo en el menú
                updateActiveNavLink(id);
            }
        });
    }, observerOptions);
    
    // Observar todas las secciones
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // ===== ACTUALIZAR ENLACE ACTIVO =====
    function updateActiveNavLink(activeId) {
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            const href = link.getAttribute('href').replace('#', '');
            if ((!activeId && href === 'inicio') || href === activeId) {
                link.classList.add('active');
                updateNavIndicator(link);
            }
        });
    }
    
    // ===== ACTUALIZAR INDICADOR DEL NAV =====
    function updateNavIndicator(activeLink) {
        if (!navIndicator) return;
        
        const linkRect = activeLink.getBoundingClientRect();
        const navRect = activeLink.closest('.nav-container').getBoundingClientRect();
        
        navIndicator.style.width = `${linkRect.width}px`;
        navIndicator.style.left = `${linkRect.left - navRect.left}px`;
    }
    
    // Inicializar el indicador
    const activeLink = document.querySelector('.nav-link.active');
    if (activeLink) {
        updateNavIndicator(activeLink);
    }
    
    // ===== TOGGLE MENÚ MÓVIL =====
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            menuToggle.classList.toggle('active');
            
            // Animar las líneas del hamburger
            const spans = menuToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
    
    // Cerrar menú al hacer clic en un enlace (móvil)
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
                
                const spans = menuToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    });
    
    // ===== SCROLL SUAVE =====
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#inicio') {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
                return;
            }
            
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                // Calcular posición considerando el navbar fijo
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetSection.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ===== FORMULARIO DE CONTACTO =====
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validación básica
            const inputs = this.querySelectorAll('input, textarea');
            let isValid = true;
            
            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'var(--accent-1)';
                } else {
                    input.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                alert('Por favor, completa todos los campos requeridos.');
                return;
            }
            
            // Simular envío (aquí iría tu lógica real de envío)
            const submitBtn = this.querySelector('.btn-submit');
            const originalText = submitBtn.textContent;
            
            submitBtn.textContent = 'Enviando...';
            submitBtn.disabled = true;
            
            setTimeout(() => {
                alert('¡Mensaje enviado! Te contactaremos pronto.');
                contactForm.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 1500);
        });
    }
    
    // ===== REAJUSTAR INDICADOR AL REDIMENSIONAR =====
    window.addEventListener('resize', () => {
        const activeLink = document.querySelector('.nav-link.active');
        if (activeLink) {
            updateNavIndicator(activeLink);
        }
    });
    
    // ===== SCROLL REVEAL INICIAL =====
    // Marcar la sección inicial como visible
    const initialSection = document.querySelector('.section');
    if (initialSection) {
        initialSection.classList.add('visible');
    }
    
    // ===== EFECTO PARALLAX SUAVE =====
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.section-number');
        
        parallaxElements.forEach(element => {
            const speed = 0.3;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
});