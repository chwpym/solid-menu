---
name: solidmenu-patterns
description: Padrões de Interface e Comportamento para o Sistema SolidMenu (Admin e PDV). Garante que todas as telas sigam a mesma "cara" e lógica.
---

# SolidMenu - Padrões de UI & UX

Use esta skill para garantir que QUALQUER nova funcionalidade ou refatoração no sistema SolidMenu siga os padrões estabelecidos de design, nomenclatura e comportamento.

## ⚠️ Regras de Ouro

1. **Sincronia Global:** Preferências do usuário (como modo Lista/Cards) devem ser salvas no `localStorage` e aplicadas a TODAS as abas relacionadas simultaneamente.
2. **Nomenclatura Semântica:** Use sempre **CÓDIGO** em vez de ID em labels voltadas ao usuário.
3. **Consistência de Ação:** Ações de exclusão/inativação devem estar sempre na primeira coluna da tabela (esquerda).
4. **Paridade de Visualização:** Se um item pode ser visto em Lista, ele DEVE ter uma versão em Cards.

## 🎨 Design System (Tokens)

- **Primary:** Navy Blue `#07355B` (Sidebar, Headers).
- **Accent:** Green `#86BC78` (Status Ativo, Ícones de Sucesso).
- **Error/Delete:** Red `#e74c3c` (Inativação, Excluir).
- **Radius:** `var(--radius-lg)` (8px a 12px) para containers e botões.

## 📋 Componentes Padrão

### Tabelas (List Mode)

- Colunas: [Ações] | [Código] | [Nome] | [Informações Adicionais...] | [Status]
- Status: Use "● Ativo" (Verde) ou "○ Inativo" (Vermelho).
- Linhas: `border-bottom: 1px solid var(--border-color)`.

### Cards (Grid Mode)

- Grid: `display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`.
- Header do Card: Mostrar Código (`#ID`) à esquerda e Ações (Editar/Excluir) à direita.
- Transições: `transition: all 0.2s ease` para hovers e opacidade em inativos (0.6).

### Modais

- Título: Inserir ID/Código no título ao editar (ex: "Editar Produto #123").
- Botões: "Cancelar" (Ghost/Outline) e "Salvar" (Solid Brand Primary).
- Reset: Sempre resetar o formulário e limpar o `dataset.editId` ao fechar.

## 🛠️ Comportamentos Obrigatórios

- **Confirmação:** Pedir confirmação via `confirm()` antes de inativar qualquer item.
- **Tooltips:** Usar `title` em botões de ícones e descrições longas.
- **PWA:** Sempre incrementar `CACHE_NAME` no `sw.js` após mudanças significativas em UI/JS/CSS.
