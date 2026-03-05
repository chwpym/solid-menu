# SolidMenu - Sistema de Gestão para Restaurantes

Bem-vindo ao **SolidMenu**, um sistema moderno e intuitivo para gestão de cardápio, pedidos e PDV (Ponto de Venda), focado em eficiência e design premium.

## 🚀 Funcionalidades Atuais

- **Cardápio Digital:** Gestão completa de Produtos, Categorias e Adicionais (Extras).
- **Interface Inteligente:** Suporte a visualização em **Lista** e **Cards** com sincronização global.
- **PWA (Progressive Web App):** Funciona offline (cache de assets) e pode ser instalado no desktop ou celular.
- **Tema Dinâmico:** Alternância entre modo Dark e Light via Topbar.
- **Design System:** Skill exclusiva de padronização para garantir consistência visual em todo o sistema.

## 🛠️ Tecnologias

- **Backend:** Python 3.x com **FastAPI**.
- **Banco de Dados:** SQLite com **SQLAlchemy** (ORM).
- **Frontend:** Vanilla JavaScript e CSS Moderno (Glassmorphism e Variáveis de Tema).
- **Segurança:** Autenticação via JWT.

## 📦 Como Rodar o Projeto

1. Certifique-se de ter o Python instalado.
2. Clone o repositório.
3. No terminal da pasta raiz, execute o script de automação:
   ```powershell
   .\run_dev.bat
   ```
4. O sistema estará disponível em: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🎨 Padrões de Design

O projeto utiliza um **Design System** proprietário definido em `backend/static/admin/DESIGN_SYSTEM.md`. Todas as novas telas devem seguir estas diretrizes para manter a identidade visual Navy Blue e Green.

## ⚠️ Sobre o Deploy

Este projeto utiliza um backend em Python (FastAPI). Por este motivo, **não pode ser hospedado diretamente no GitHub Pages** (que suporta apenas sites estáticos). Recomendamos o uso de plataformas como Render, Railway ou Fly.io para hospedagem completa.

---

_Desenvolvido com foco na experiência do usuário e agilidade operacional._
