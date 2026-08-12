(() => {
  const search = document.querySelector('#catalogue-search');
  const buttons = [...document.querySelectorAll('.catalogue-filter')];
  const cards = [...document.querySelectorAll('.catalogue-card')];
  const sections = [...document.querySelectorAll('.catalogue-section')];
  const status = document.querySelector('#catalogue-status');
  const noResults = document.querySelector('#catalogue-no-results');
  let activeCategory = 'all';

  // Keep every catalogue image local. If a specific local image cannot load,
  // fall back to another locally stored official Roth family image.
  document.querySelectorAll('img[data-fallback]').forEach((img) => {
    img.addEventListener('error', () => {
      const fallback = img.dataset.fallback;
      if (fallback && img.getAttribute('src') !== fallback) img.setAttribute('src', fallback);
    }, { once: true });
  });

  // These named items do not have a separately published exact photo in the
  // public source set used for the catalogue. Make the representative status
  // explicit rather than implying that the related Roth image is the exact item.
  ['standaard-drukvat', 'speciaal-drukvat', 'rvs-accumulatoren'].forEach((id) => {
    const card = document.getElementById(id);
    const caption = card?.querySelector('.photo-label');
    if (caption) caption.textContent = 'Officiële Roth-familiefoto · representatief';
  });

  ['breekplaten', 'smeltzekeringen-fusible-plugs'].forEach((id) => {
    const card = document.getElementById(id);
    const image = card?.querySelector('img');
    const caption = card?.querySelector('.photo-label');
    if (image) image.src = 'assets/products/diaphragm-family-fallback.webp';
    if (caption) caption.textContent = 'Officiële Roth-familiefoto · representatief';
  });

  const normalize = (value) => (value || '')
    .toLocaleLowerCase('nl-NL')
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '');

  function applyFilters() {
    const query = normalize(search?.value);
    let visible = 0;

    cards.forEach((card) => {
      const categoryMatch = activeCategory === 'all' || card.dataset.category === activeCategory;
      const textMatch = !query || normalize(card.dataset.search).includes(query);
      const show = categoryMatch && textMatch;
      card.hidden = !show;
      if (show) visible += 1;
    });

    sections.forEach((section) => {
      const sectionCards = [...section.querySelectorAll('.catalogue-card')];
      section.hidden = sectionCards.length > 0 && sectionCards.every((card) => card.hidden);
    });

    if (status) status.textContent = `${visible} van ${cards.length} benoemde producten, opties en oplossingen zichtbaar`;
    if (noResults) noResults.classList.toggle('show', visible === 0);
  }

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      activeCategory = button.dataset.filter;
      buttons.forEach((item) => item.classList.toggle('active', item === button));
      applyFilters();
    });
  });

  search?.addEventListener('input', applyFilters);
  applyFilters();
})();
