/**
 * Lógica da Tela de Login
 */
 import { apiFetch } from './api.js';

 const loginForm = document.getElementById('loginForm');
 const errorAlert = document.getElementById('errorAlert');
 const btnSubmit = document.getElementById('btnSubmit');
 
 if (loginForm) {
     loginForm.addEventListener('submit', async (e) => {
         e.preventDefault();
         
         const email = document.getElementById('email').value;
         const senha = document.getElementById('senha').value;
         
         // Limpa erro / Loading state
         errorAlert.classList.remove('show');
         btnSubmit.disabled = true;
         btnSubmit.textContent = "Autenticando...";
 
         try {
             // Chamamos a rota de login padrão (não a token do swagger, mas a nossa /login que aceita JSON)
             const data = await apiFetch('/auth/login', {
                 method: 'POST',
                 body: JSON.stringify({ email, senha })
             });
             
             // Sucesso!
             localStorage.setItem('solidmenu_token', data.access_token);
             localStorage.setItem('solidmenu_user', JSON.stringify({
                 id: data.user_id,
                 nome: data.nome,
                 role: data.role
             }));
 
             // Animação de sucesso
             btnSubmit.style.backgroundColor = 'var(--success)';
             btnSubmit.textContent = "Bem-vindo!";
             
             setTimeout(() => {
                 window.location.href = 'index.html'; // Shell principal que criaremos em seguida
             }, 800);
 
         } catch (error) {
             // Mostra Erro
             errorAlert.textContent = typeof error === 'string' ? error : error.message;
             errorAlert.classList.add('show');
             btnSubmit.disabled = false;
             btnSubmit.textContent = "Acessar Painel";
         }
     });
 }
