/**
 * API Wrapper Core
 * Lida com chamadas Fetch, Injeção de JWT e Erros de Autenticação.
 */

 const API_BASE = '/api'; // Como o front está no mesmo server, usamos path relativo.

 export async function apiFetch(endpoint, options = {}) {
     const token = localStorage.getItem('solidmenu_token');
     
     const headers = {
         'Content-Type': 'application/json',
         ...options.headers
     };
 
     if (token) {
         headers['Authorization'] = `Bearer ${token}`;
     }
 
     const res = await fetch(`${API_BASE}${endpoint}`, {
         ...options,
         headers
     });
 
     // Trata 401 (Token Expirado ou Inválido) de forma global
     if (res.status === 401) {
         localStorage.removeItem('solidmenu_token');
         localStorage.removeItem('solidmenu_user');
         if (!window.location.pathname.includes('login.html')) {
             window.location.href = 'login.html';
         }
         throw new Error("Sessão expirada.");
     }
 
     const data = await res.json();
 
     if (!res.ok) {
         throw new Error(data.detail || "Erro desconhecido na API.");
     }
 
     return data;
 }
