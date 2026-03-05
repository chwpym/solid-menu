/**
 * SPA Router System (Vanilla JS)
 * Carrega fragmentos HTML da pasta /views/ e os injeta na #main-content
 */

const contentContainer = document.getElementById('main-content') || document.querySelector('.main-content');
const routes = {
    'dashboard': { url: 'views/dashboard.html', title: 'Dashboard - SolidMenu' },
    'cardapio': { url: 'views/cardapio.html', title: 'Cardápio - SolidMenu', module: './cardapio.js', init: 'setupCardapioView' },
};

// Evento disparado quando clica em links com atributo data-route
document.addEventListener('click', e => {
    const routeItem = e.target.closest('[data-route]');
    if (routeItem) {
        e.preventDefault();
        const routeName = routeItem.getAttribute('data-route');
        navigateTo(routeName);
    }
});

// Navegação Real
export async function navigateTo(routeName) {
    if (!routes[routeName]) {
        console.warn('Rota não encontrada:', routeName);
        return;
    }

    try {
        // Mostra um loading rápido se quiser
        contentContainer.innerHTML = '<div style="text-align:center; padding: 2rem; color: var(--text-muted);">Carregando...</div>';
        
        // Push State para manter a URL atualizada e permitir "Voltar" do navegador
        window.history.pushState({ route: routeName }, routes[routeName].title, `?view=${routeName}`);
        document.title = routes[routeName].title;

        // Fetch do HTML
        const response = await fetch(routes[routeName].url);
        if (!response.ok) throw new Error('Falha ao carregar a view');
        
        const html = await response.text();
        contentContainer.innerHTML = html;

        // Atualiza botões ativos na sidebar
        document.querySelectorAll('.sidebar [data-route]').forEach(el => {
            el.style.backgroundColor = 'transparent';
        });
        const activeLink = document.querySelector(`.sidebar [data-route="${routeName}"]`);
        if (activeLink) {
            activeLink.style.backgroundColor = 'hsla(var(--brand-primary-h), var(--brand-primary-s), var(--brand-primary-l), 0.1)';
        }

        // Executar script da View, se houver, pois tags <script> no innerHTML não rodam nativamente
        if (routes[routeName].module && routes[routeName].init) {
            try {
                const module = await import(routes[routeName].module);
                if (typeof module[routes[routeName].init] === 'function') {
                    module[routes[routeName].init]();
                }
            } catch (errModule) {
                console.error(`Erro ao carregar o controlador da rota ${routeName}:`, errModule);
            }
        } else {
            // Dispara evento global por fallback
            document.dispatchEvent(new CustomEvent(`viewLoaded:${routeName}`));
        }

    } catch (err) {
        contentContainer.innerHTML = `<div class="alert alert-error" style="display:block;">Erro ao carregar tela: ${err.message}</div>`;
    }
}

// Lida com botão Voltar/Avançar do navegador
window.addEventListener('popstate', (e) => {
    if (e.state && e.state.route) {
        navigateTo(e.state.route);
    } else {
        checkInitialRoute();
    }
});

function checkInitialRoute() {
    const params = new URLSearchParams(window.location.search);
    const view = params.get('view') || 'dashboard';
    navigateTo(view);
}

// Inicia verificação na primeira carga
if (window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/admin/')) {
    checkInitialRoute();
}
