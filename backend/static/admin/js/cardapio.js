import { apiFetch } from './api.js';

let categoriasBase = [];
let currentViewMode = localStorage.getItem('solidmenu_view_mode') || 'list';

export async function carregarCategorias() {
    try {
        categoriasBase = await apiFetch('/categorias');
        
        const filtro = document.getElementById('filtroCategoria');
        const selectModal = document.getElementById('prodCategoria_modal');
        
        const opts = categoriasBase.map(c => `<option value="${c.id}">${c.nome}</option>`).join('');
        
        if(filtro) {
            filtro.innerHTML = '<option value="todas">Todas Categorias</option>' + opts;
        }
        if(selectModal) {
            selectModal.innerHTML = opts;
        }
    } catch(err) {
        console.error("Erro categorias:", err);
    }
}

let currentTab = 'produtos_container';

window.setViewMode = (mode) => {
    currentViewMode = mode;
    localStorage.setItem('solidmenu_view_mode', mode);
    
    // Recarrega TODAS as visualizações para manter sincronia global
    carregarProdutos();
    carregarCategoriasTab();
    carregarAdicionais();
};

export async function carregarCategoriasTab() {
    const container = document.getElementById('categorias_container');
    if (!container) return;
    
    const checkStore = document.getElementById('checkShowInativos');
    const showInativos = checkStore ? checkStore.checked : false;

    try {
        const urlParams = showInativos ? '?inativos=true' : '';
        const categorias = await apiFetch('/categorias' + urlParams);
        
        if (currentViewMode === 'list') {
            let html = `
            <div class="data-table-container" style="width: 100%; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead style="background: hsla(var(--brand-primary-h), var(--brand-primary-s), var(--brand-primary-l), 0.05); border-bottom: 1px solid var(--border-color);">
                        <tr>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Ações</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Código</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Nome</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            categorias.forEach(cat => {
                const actionBtn = cat.ativo 
                    ? `<button onclick="excluirCategoria(${cat.id})" style="border: none; background: transparent; cursor: pointer; color: var(--error);" title="Inativar">🗑️</button>`
                    : `<button onclick="reativarCategoria(${cat.id})" style="border: none; background: transparent; cursor: pointer; color: var(--success);" title="Reativar">♻️</button>`;

                html += `
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 1rem;">
                            <button onclick="editarCategoria(${cat.id}, '${cat.nome.replace(/'/g, "\\'")}')" style="border: none; background: transparent; cursor: pointer; color: var(--brand-primary); margin-right: 0.5rem;" title="Editar">✏️</button>
                            ${actionBtn}
                        </td>
                        <td style="padding: 1rem; color: var(--text-muted);">#${cat.id}</td>
                        <td style="padding: 1rem; font-weight: 500;">${cat.nome}</td>
                        <td style="padding: 1rem;"><span style="color: ${cat.ativo ? 'var(--success)' : 'var(--error)'}">${cat.ativo ? '● Ativo' : '○ Inativo'}</span></td>
                    </tr>
                `;
            });
            html += `</tbody></table></div>`;
            container.innerHTML = html;
        } else {
            let html = `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; padding: 0.5rem 0;">`;
            categorias.forEach(cat => {
                const actionBtn = cat.ativo 
                    ? `<button onclick="excluirCategoria(${cat.id})" style="border: none; background: transparent; cursor: pointer; color: var(--error);" title="Inativar">🗑️</button>`
                    : `<button onclick="reativarCategoria(${cat.id})" style="border: none; background: transparent; cursor: pointer; color: var(--success);" title="Reativar">♻️</button>`;

                html += `
                    <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.5rem; display: flex; flex-direction: column; transition: all 0.2s ease; opacity: ${cat.ativo ? 1 : 0.6}">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                            <span style="font-size: 0.8rem; color: var(--brand-primary); background: hsla(var(--brand-primary-h), var(--brand-primary-s), var(--brand-primary-l), 0.1); padding: 0.2rem 0.6rem; border-radius: 12px; font-weight: 600;">#${cat.id}</span>
                            <div>
                                <button onclick="editarCategoria(${cat.id}, '${cat.nome.replace(/'/g, "\\'")}')" style="border: none; background: transparent; cursor: pointer; color: var(--brand-primary); margin-right: 0.5rem;" title="Editar">✏️</button>
                                ${actionBtn}
                            </div>
                        </div>
                        <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem;">${cat.nome}</h3>
                        <div style="color: ${cat.ativo ? 'var(--success)' : 'var(--error)'}; font-weight: 600; font-size: 0.85rem;">${cat.ativo ? '● Ativo' : '○ Inativo'}</div>
                    </div>
                `;
            });
            html += `</div>`;
            container.innerHTML = html;
        }
        atualizarBotoesToggle();
    } catch(err) {
        container.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--error);">Erro: ${err.message}</div>`;
    }
}

export async function carregarAdicionais() {
    const container = document.getElementById('adicionais_container');
    if (!container) return;
    
    const checkStore = document.getElementById('checkShowInativos');
    const showInativos = checkStore ? checkStore.checked : false;

    try {
        const urlParams = showInativos ? '?inativos=true' : '';
        const adicionais = await apiFetch('/adicionais' + urlParams);
        if (currentViewMode === 'list') {
            let html = `
            <div class="data-table-container" style="width: 100%; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead style="background: hsla(var(--brand-primary-h), var(--brand-primary-s), var(--brand-primary-l), 0.05); border-bottom: 1px solid var(--border-color);">
                        <tr>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Ações</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Código</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Nome</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Preço</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            adicionais.forEach(add => {
                const deco = add.ativo ? 'none' : 'line-through';
                const color = add.ativo ? 'var(--text-on-base)' : 'var(--text-muted)';
                const actionBtn = add.ativo 
                    ? `<button onclick="excluirAdicional(${add.id})" style="border: none; background: transparent; cursor: pointer; color: var(--error);" title="Inativar">🗑️</button>`
                    : `<button onclick="reativarAdicional(${add.id})" style="border: none; background: transparent; cursor: pointer; color: var(--success);" title="Reativar">♻️</button>`;

                html += `
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 1rem;">
                            <button onclick="editarAdicional(${add.id}, '${add.nome.replace(/'/g, "\\'")}', ${add.preco})" style="border: none; background: transparent; cursor: pointer; color: var(--brand-primary); margin-right: 0.5rem;" title="Editar">✏️</button>
                            ${actionBtn}
                        </td>
                        <td style="padding: 1rem; color: var(--text-muted);">#${add.id}</td>
                        <td style="padding: 1rem; font-weight: 500; text-decoration: ${deco}; color: ${color};">${add.nome}</td>
                        <td style="padding: 1rem; color: var(--success); font-weight: 600;">R$ ${parseFloat(add.preco).toFixed(2).replace('.', ',')}</td>
                    </tr>
                `;
            });
            html += `</tbody></table></div>`;
            container.innerHTML = html;
        } else {
            let html = `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; padding: 0.5rem 0;">`;
            adicionais.forEach(add => {
                const deco = add.ativo ? 'none' : 'line-through';
                const color = add.ativo ? 'var(--text-on-base)' : 'var(--text-muted)';
                const actionBtn = add.ativo 
                    ? `<button onclick="excluirAdicional(${add.id})" style="border: none; background: transparent; cursor: pointer; color: var(--error);" title="Inativar">🗑️</button>`
                    : `<button onclick="reativarAdicional(${add.id})" style="border: none; background: transparent; cursor: pointer; color: var(--success);" title="Reativar">♻️</button>`;

                html += `
                    <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.5rem; display: flex; flex-direction: column; transition: all 0.2s ease; opacity: ${add.ativo ? 1 : 0.6}">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                            <span style="font-size: 0.8rem; color: var(--brand-primary); background: hsla(var(--brand-primary-h), var(--brand-primary-s), var(--brand-primary-l), 0.1); padding: 0.2rem 0.6rem; border-radius: 12px; font-weight: 600;">#${add.id}</span>
                            <div>
                                <button onclick="editarAdicional(${add.id}, '${add.nome.replace(/'/g, "\\'")}', ${add.preco})" style="border: none; background: transparent; cursor: pointer; color: var(--brand-primary); margin-right: 0.5rem;" title="Editar">✏️</button>
                                ${actionBtn}
                            </div>
                        </div>
                        <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem; text-decoration: ${deco}; color: ${color};">${add.nome}</h3>
                        <div style="font-size: 1.25rem; color: var(--success); font-weight: 700;">R$ ${parseFloat(add.preco).toFixed(2).replace('.', ',')}</div>
                    </div>
                `;
            });
            html += `</div>`;
            container.innerHTML = html;
        }
        atualizarBotoesToggle();
    } catch(err) {
        container.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--error);">Erro: ${err.message}</div>`;
    }
}

function atualizarBotoesToggle() {
    const btnViewList = document.getElementById('btnViewList');
    const btnViewCard = document.getElementById('btnViewCard');
    if (btnViewList && btnViewCard) {
        btnViewList.style.background = currentViewMode === 'list' ? 'var(--border-color)' : 'transparent';
        btnViewList.style.color = currentViewMode === 'list' ? 'var(--text-on-base)' : 'var(--text-muted)';
        btnViewCard.style.background = currentViewMode === 'card' ? 'var(--border-color)' : 'transparent';
        btnViewCard.style.color = currentViewMode === 'card' ? 'var(--text-on-base)' : 'var(--text-muted)';
    }
}

export async function carregarProdutos() {
    const container = document.getElementById('produtos_container');
    if (!container) return;

    const checkStore = document.getElementById('checkShowInativos');
    const showInativos = checkStore ? checkStore.checked : false;
    const filtroVal = document.getElementById('filtroCategoria')?.value || 'todas';

    try {
        const urlParams = showInativos ? '?inativos=true' : '';
        let produtos = await apiFetch('/produtos' + urlParams);
        
        if (filtroVal !== 'todas') {
            produtos = produtos.filter(p => p.categoria_id == filtroVal);
        }

        if (produtos.length === 0) {
            container.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--text-muted);">Nenhum produto encontrado.</div>`;
            return;
        }

        if (currentViewMode === 'list') {
            let html = `
            <div class="data-table-container" style="width: 100%; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead style="background: hsla(var(--brand-primary-h), var(--brand-primary-s), var(--brand-primary-l), 0.05); border-bottom: 1px solid var(--border-color);">
                        <tr>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Ações</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Código</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Nome</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Categoria</th>
                            <th style="padding: 1rem; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Preço</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            produtos.forEach(prod => {
                const textColor = prod.ativo ? 'var(--text-on-base)' : 'var(--text-muted)';
                const decor = prod.ativo ? 'none' : 'line-through';
                const actionBtn = prod.ativo 
                    ? `<button onclick="excluirProduto(${prod.id})" style="border: none; background: transparent; cursor: pointer; color: var(--error);" title="Inativar">🗑️</button>`
                    : `<button onclick="reativarProduto(${prod.id})" style="border: none; background: transparent; cursor: pointer; color: var(--success);" title="Reativar">♻️</button>`;
                
                html += `
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 1rem;">
                            <button onclick="editarProduto(${prod.id}, '${prod.nome.replace(/'/g, "\\'")}', '${prod.descricao ? prod.descricao.replace(/'/g, "\\'") : ''}', ${prod.preco}, ${prod.categoria_id})" style="border: none; background: transparent; cursor: pointer; color: var(--brand-primary); margin-right: 0.5rem;" title="Editar">✏️</button>
                            ${actionBtn}
                        </td>
                        <td style="padding: 1rem; color: var(--text-muted);">#${prod.produto_id || prod.id}</td>
                        <td style="padding: 1rem; font-weight: 500; color: ${textColor}; text-decoration: ${decor}; cursor: help;" title="Ingredientes/Detalhes: ${prod.descricao || 'Nenhuma descrição'}">${prod.nome}</td>
                        <td style="padding: 1rem; color: var(--text-muted);">${(prod.categoria && prod.categoria.nome) ? prod.categoria.nome : (prod.categoria_id || 'Sem Cat')}</td>
                        <td style="padding: 1rem; color: var(--success); font-weight: 600;">R$ ${parseFloat(prod.preco).toFixed(2).replace('.', ',')}</td>
                    </tr>
                `;
            });
            html += `</tbody></table></div>`;
            container.innerHTML = html;
        } else {
            let html = `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; padding: 0.5rem 0;">`;
            produtos.forEach(prod => {
                const textColor = prod.ativo ? 'var(--text-on-base)' : 'var(--text-muted)';
                const decor = prod.ativo ? 'none' : 'line-through';
                const actionBtn = prod.ativo 
                    ? `<button onclick="excluirProduto(${prod.id})" style="border: none; background: transparent; cursor: pointer; color: var(--error);" title="Inativar">🗑️</button>`
                    : `<button onclick="reativarProduto(${prod.id})" style="border: none; background: transparent; cursor: pointer; color: var(--success);" title="Reativar">♻️</button>`;
                
                html += `
                    <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.5rem; display: flex; flex-direction: column; opacity: ${prod.ativo ? 1 : 0.6}; transition: all 0.2s ease;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                            <span style="font-size: 0.8rem; color: var(--brand-primary); background: hsla(var(--brand-primary-h), var(--brand-primary-s), var(--brand-primary-l), 0.1); padding: 0.2rem 0.6rem; border-radius: 12px; font-weight: 600;">#${prod.produto_id || prod.id}</span>
                            <div>
                                <button onclick="editarProduto(${prod.id}, '${prod.nome.replace(/'/g, "\\'")}', '${prod.descricao ? prod.descricao.replace(/'/g, "\\'") : ''}', ${prod.preco}, ${prod.categoria_id})" style="border: none; background: transparent; cursor: pointer; color: var(--brand-primary); margin-right: 0.5rem;" title="Editar">✏️</button>
                                ${actionBtn}
                            </div>
                        </div>
                        <h3 style="font-size: 1.1rem; color: ${textColor}; text-decoration: ${decor}; margin-bottom: 0.5rem; cursor: help;" title="Ingredientes: ${prod.descricao || ''}">${prod.nome}</h3>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem; flex: 1;">${(prod.categoria && prod.categoria.nome) ? prod.categoria.nome : 'Sem Cat'}</p>
                        <div style="font-size: 1.25rem; color: var(--success); font-weight: 700;">R$ ${parseFloat(prod.preco).toFixed(2).replace('.', ',')}</div>
                    </div>
                `;
            });
            html += `</div>`;
            container.innerHTML = html;
        }

        atualizarBotoesToggle();
    } catch (err) {
        container.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--error);">Erro: ${err.message}</div>`;
    }
}

// Inicializa Eventos da View
export function setupCardapioView() {
    window.carregarProdutos = carregarProdutos; 
    window.carregarCategoriasTab = carregarCategoriasTab;
    window.carregarAdicionais = carregarAdicionais;

    carregarCategorias().then(() => {
        carregarProdutos(); 
        carregarCategoriasTab();
        carregarAdicionais();
    });

    // Lógica de Abas
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');
    const btnNovoProd = document.getElementById('btnOpenModalProduto');
    const btnNovoCat = document.getElementById('btnOpenModalCategoria');
    const btnNovoAdd = document.getElementById('btnOpenModalAdicional');

    tabs.forEach(btn => {
        btn.onclick = () => {
            tabs.forEach(t => {
                t.classList.remove('active');
                t.style.borderBottomColor = 'transparent';
                t.style.color = 'var(--text-muted)';
            });
            contents.forEach(c => c.style.display = 'none');
            
            btn.classList.add('active');
            btn.style.borderBottomColor = 'var(--brand-primary)';
            btn.style.color = 'var(--brand-primary)';
            
            const targetId = btn.getAttribute('data-target');
            currentTab = targetId;
            const target = document.getElementById(targetId);
            if (target) target.style.display = 'block';

            // Ajusta visibilidade do filtro de categoria (apenas para produtos)
            const filtroCat = document.getElementById('filtroCategoria');
            if (filtroCat) filtroCat.style.display = targetId === 'produtos_container' ? 'block' : 'none';

            // Recarrega a aba ao trocar para garantir sincronia
            if (targetId === 'produtos_container') carregarProdutos();
            else if (targetId === 'categorias_container') carregarCategoriasTab();
            else if (targetId === 'adicionais_container') carregarAdicionais();

            // Ajusta botões de "Novo"
            if (btnNovoProd) btnNovoProd.style.display = targetId === 'produtos_container' ? 'block' : 'none';
            if (btnNovoCat) btnNovoCat.style.display = targetId === 'categorias_container' ? 'block' : 'none';
            if (btnNovoAdd) btnNovoAdd.style.display = targetId === 'adicionais_container' ? 'block' : 'none';
        };
    });

    // Modal Produto
    const modalProd = document.getElementById('modalProduto');
    const btnOpenProd = document.getElementById('btnOpenModalProduto');
    const btnCloseProd = document.getElementById('btnCloseModalProduto');
    const btnCancelProd = document.getElementById('btnCancelModalProduto');
    const formProd = document.getElementById('formNovoProduto');

    const closeProd = () => { modalProd.classList.remove('active'); formProd.reset(); delete formProd.dataset.editId; };
    if(btnOpenProd) btnOpenProd.onclick = () => { formProd.querySelector('h2').textContent = "Novo Produto"; closeProd(); modalProd.classList.add('active'); };
    if(btnCloseProd) btnCloseProd.onclick = closeProd;
    if(btnCancelProd) btnCancelProd.onclick = closeProd;

    if(formProd) {
        formProd.onsubmit = async (e) => {
            e.preventDefault();
            const isEdit = formProd.dataset.editId;
            const payload = {
                nome: document.getElementById('prodNome').value,
                descricao: document.getElementById('prodDescricao').value || null,
                preco: parseFloat(document.getElementById('prodPreco').value),
                categoria_id: parseInt(document.getElementById('prodCategoria_modal').value) || 1,
                local_producao_id: 1
            };
            try {
                if(isEdit) await apiFetch(`/produtos/${isEdit}`, { method: 'PUT', body: JSON.stringify(payload) });
                else await apiFetch('/produtos', { method: 'POST', body: JSON.stringify(payload) });
                closeProd();
                carregarProdutos();
            } catch(err) { alert(err.message); }
        };
    }

    // Modal Categoria
    const modalCat = document.getElementById('modalCategoria');
    const btnOpenCat = document.getElementById('btnOpenModalCategoria');
    const btnCloseCat = document.getElementById('btnCloseModalCategoria');
    const btnCancelCat = document.getElementById('btnCancelModalCategoria');
    const formCat = document.getElementById('formNovaCategoria');

    const closeCat = () => { modalCat.classList.remove('active'); formCat.reset(); delete formCat.dataset.editId; };
    if(btnOpenCat) btnOpenCat.onclick = () => { modalCat.querySelector('h2').textContent = "Nova Categoria"; closeCat(); modalCat.classList.add('active'); };
    if(btnCloseCat) btnCloseCat.onclick = closeCat;
    if(btnCancelCat) btnCancelCat.onclick = closeCat;

    if(formCat) {
        formCat.onsubmit = async (e) => {
            e.preventDefault();
            const isEdit = formCat.dataset.editId;
            const payload = { nome: document.getElementById('catNome').value };
            try {
                if(isEdit) await apiFetch(`/categorias/${isEdit}`, { method: 'PUT', body: JSON.stringify(payload) });
                else await apiFetch('/categorias', { method: 'POST', body: JSON.stringify(payload) });
                closeCat();
                carregarCategorias();
                carregarCategoriasTab();
            } catch(err) { alert(err.message); }
        };
    }

    // Modal Adicional
    const modalAdd = document.getElementById('modalAdicional');
    const btnOpenAdd = document.getElementById('btnOpenModalAdicional');
    const btnCloseAdd = document.getElementById('btnCloseModalAdicional');
    const btnCancelAdd = document.getElementById('btnCancelModalAdicional');
    const formAdd = document.getElementById('formNovoAdicional');

    const closeAdd = () => { modalAdd.classList.remove('active'); formAdd.reset(); delete formAdd.dataset.editId; };
    if(btnOpenAdd) btnOpenAdd.onclick = () => { modalAdd.querySelector('h2').textContent = "Novo Adicional"; closeAdd(); modalAdd.classList.add('active'); };
    if(btnCloseAdd) btnCloseAdd.onclick = closeAdd;
    if(btnCancelAdd) btnCancelAdd.onclick = closeAdd;

    if(formAdd) {
        formAdd.onsubmit = async (e) => {
            e.preventDefault();
            const isEdit = formAdd.dataset.editId;
            const payload = { 
                nome: document.getElementById('addNome').value,
                preco: parseFloat(document.getElementById('addPreco').value)
            };
            try {
                if(isEdit) await apiFetch(`/adicionais/${isEdit}`, { method: 'PUT', body: JSON.stringify(payload) });
                else await apiFetch('/adicionais', { method: 'POST', body: JSON.stringify(payload) });
                closeAdd();
                carregarAdicionais();
            } catch(err) { alert(err.message); }
        };
    }
}

// Funções globais necessárias no onclick do HTML renderizado
window.excluirProduto = async (id) => {
    if (confirm("Tem certeza que deseja inativar este produto?")) {
        try {
            await apiFetch(`/produtos/${id}`, { method: 'DELETE' });
            carregarProdutos(); // Recarrega
        } catch(err) {
            alert("Erro ao inativar: " + err.message);
        }
    }
};

window.reativarProduto = async (id) => {
    if (confirm("Deseja reativar este produto para aparecer de volta no Cardápio?")) {
        try {
            await apiFetch(`/produtos/${id}/ativar`, { method: 'PATCH' });
            carregarProdutos(); // Recarrega
        } catch(err) {
            alert("Erro ao reativar: " + err.message);
        }
    }
};

window.editarProduto = (id, nome, descricao, preco, categoria_id) => {
    const modal = document.getElementById('modalProduto');
    const form = document.getElementById('formNovoProduto');
    modal.querySelector('h2').textContent = "Editar Produto #" + id;
    document.getElementById('prodNome').value = nome;
    document.getElementById('prodDescricao').value = descricao || '';
    document.getElementById('prodPreco').value = preco;
    const catSelect = document.getElementById('prodCategoria_modal');
    if(catSelect && categoria_id) catSelect.value = categoria_id;
    form.dataset.editId = id;
    modal.classList.add('active');
};

window.editarCategoria = (id, nome) => {
    const modal = document.getElementById('modalCategoria');
    const form = document.getElementById('formNovaCategoria');
    modal.querySelector('h2').textContent = "Editar Categoria #" + id;
    document.getElementById('catNome').value = nome;
    form.dataset.editId = id;
    modal.classList.add('active');
};

window.editarAdicional = (id, nome, preco) => {
    const modal = document.getElementById('modalAdicional');
    const form = document.getElementById('formNovoAdicional');
    modal.querySelector('h2').textContent = "Editar Adicional #" + id;
    document.getElementById('addNome').value = nome;
    document.getElementById('addPreco').value = preco;
    form.dataset.editId = id;
    modal.classList.add('active');
};

window.excluirCategoria = async (id) => {
    if (confirm("Tem certeza que deseja inativar esta categoria?")) {
        try {
            await apiFetch(`/categorias/${id}`, { method: 'DELETE' });
            carregarCategoriasTab();
        } catch(err) { alert(err.message); }
    }
};

window.reativarCategoria = async (id) => {
    try {
        await apiFetch(`/categorias/${id}/ativar`, { method: 'PATCH' });
        carregarCategoriasTab();
    } catch(err) { alert(err.message); }
};

window.excluirAdicional = async (id) => {
    if (confirm("Tem certeza que deseja inativar este adicional?")) {
        try {
            await apiFetch(`/adicionais/${id}`, { method: 'DELETE' });
            carregarAdicionais();
        } catch(err) { alert(err.message); }
    }
};

window.reativarAdicional = async (id) => {
    try {
        await apiFetch(`/adicionais/${id}/ativar`, { method: 'PATCH' });
        carregarAdicionais();
    } catch(err) { alert(err.message); }
};

window.recarregarAbaAtual = () => {
    if (currentTab === 'produtos_container') carregarProdutos();
    else if (currentTab === 'categorias_container') carregarCategoriasTab();
    else if (currentTab === 'adicionais_container') carregarAdicionais();
};
