document.querySelector('.menu-button')?.addEventListener('click', () => {
  const nav = document.querySelector('nav');
  nav.style.display = nav.style.display === 'flex' ? '' : 'flex';
});
