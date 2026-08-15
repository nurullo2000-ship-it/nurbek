document.querySelector('.menu-button')?.addEventListener('click', () => {
  const button = document.querySelector('.menu-button');
  const nav = document.querySelector('nav');
  const isOpen = nav.style.display === 'flex';
  nav.style.display = isOpen ? '' : 'flex';
  button.setAttribute('aria-expanded', String(!isOpen));
});
