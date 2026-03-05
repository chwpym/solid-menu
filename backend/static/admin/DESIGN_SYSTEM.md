# SolidMenu - Design System & UI Patterns

Este documento define os padrões visuais e de interação que **devem** ser seguidos em todas as telas do sistema para garantir uma experiência consistente e profissional.

---

## 1. Identidade Visual (Cores)

- **Marca Principal (Navy):** `#07355B` (Uso: Sidebar, cabeçalhos secundários).
- **Acento (Verde):** `#86BC78` (Uso: Detalhes, ícones de sucesso, status ativo).
- **Ação Primária:** Azul da marca (Botões de "Salvar", "Novo", "Confirmar").
- **Alertas/Erros:** Vermelho vibrante (`#e74c3c`) para "Inativar", "Excluir" ou mensagens de erro.

## 2. Componentes de Interface

### Tabelas (Modo Lista)

- **Ações:** Devem ser a **primeira coluna** à esquerda.
- **Cabeçalho:** Texto em uppercase, fonte menor (0.85rem), cor muted.
- **Linhas:** Borda inferior sutil, hover state para facilitar a leitura.
- **Status:** Cores semânticas (Verde para Ativo, Vermelho para Inativo).

### Cards (Modo Grid)

- **Dimensões:** Grid responsivo com `minmax(280px, 1fr)`.
- **Conteúdo:** Título em destaque, informações secundárias em `text-muted`, preço ou valor principal no final com fonte maior.
- **Interação:** Sombra (`shadow-md`) ao passar o mouse.

### Modais

- **Título:** H2 no topo, à esquerda.
- **Botão Fechar:** Ícone de "&times;" no canto superior direito.
- **Rodapé de Ação:** Botões alinhados à direita ("Cancelar" à esquerda de "Salvar").
- **Campos:** Labels sempre acima do input, placeholders claros.

## 3. Comportamentos Padrão

- **Feedback de Carregamento:** Sempre mostrar "Carregando..." ou um spinner ao buscar dados.
- **Confirmação:** Pedir confirmação apenas para ações destrutivas (Inativar/Excluir).
- **Persistência:** Salvar preferências de visualização (ex: Lista/Cards) no `localStorage`.
- **Tooltips:** Usar o atributo `title` para explicar ícones ou mostrar descrições longas.

---

> [!IMPORTANT]
> Se uma nova funcionalidade for criada, ela **deve** obrigatoriamente suportar os modos Lista e Cards para manter a paridade com o restante do sistema.
