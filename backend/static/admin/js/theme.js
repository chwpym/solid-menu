/**
 * Gestão de Tema Light / Dark (SolidMenu)
 * Salva a preferência no localStorage.
 */

const btnToggle = document.getElementById("themeToggle");
const htmlEl = document.documentElement;

// Ícones SVG simplificados
const iconSun = `<svg viewBox="0 0 24 24"><path d="M12 7A5 5 0 1 1 7 12A5 5 0 0 1 12 7M12 21V19M12 5V3M3 12H5M19 12H21M4.22 19.78L5.64 18.36M18.36 5.64L19.78 4.22M4.22 4.22L5.64 5.64M18.36 18.36L19.78 19.78" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>`;
const iconMoon = `<svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="currentColor"/></svg>`;

function setTheme(theme) {
  htmlEl.setAttribute("data-theme", theme);
  localStorage.setItem("solidmenu_theme", theme);
  if (btnToggle) {
    btnToggle.innerHTML = theme === "dark" ? iconSun : iconMoon;
  }
}

function toggleTheme() {
  const currentTheme = htmlEl.getAttribute("data-theme");
  setTheme(currentTheme === "dark" ? "light" : "dark");
}

// Inicialização
function initTheme() {
  const savedTheme = localStorage.getItem("solidmenu_theme");
  if (savedTheme) {
    setTheme(savedTheme);
  } else {
    // Detecta preferência do SO
    if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      setTheme("dark");
    } else {
      setTheme("light");
    }
  }
}

if (btnToggle) {
  btnToggle.addEventListener("click", toggleTheme);
}

initTheme();
