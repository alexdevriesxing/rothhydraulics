(() => {
  const menu = document.querySelector('.mobile-menu');
  const panel = document.querySelector('.mobile-panel');
  if(menu && panel) menu.addEventListener('click', () => panel.classList.toggle('open'));
  const form = document.querySelector('[data-contact-form]');
  if(form){
    form.addEventListener('submit', e => {
      e.preventDefault();
      const data = new FormData(form);
      const subject = encodeURIComponent('Roth Hydraulics aanvraag – ' + (data.get('onderwerp') || 'technisch advies'));
      const body = encodeURIComponent(
        'Naam: ' + (data.get('naam')||'') + '\n' +
        'Bedrijf: ' + (data.get('bedrijf')||'') + '\n' +
        'E-mail: ' + (data.get('email')||'') + '\n' +
        'Telefoon: ' + (data.get('telefoon')||'') + '\n' +
        'Onderwerp: ' + (data.get('onderwerp')||'') + '\n\n' +
        (data.get('bericht')||'')
      );
      window.location.href = 'mailto:info@hobohydrauliek.nl?subject=' + subject + '&body=' + body;
    });
  }
  const cookie = document.querySelector('.cookie');
  if(cookie && !localStorage.getItem('roth-cookie-choice')) cookie.classList.add('show');
  document.querySelectorAll('[data-cookie-choice]').forEach(btn => btn.addEventListener('click', () => {
    localStorage.setItem('roth-cookie-choice', btn.dataset.cookieChoice);
    cookie?.classList.remove('show');
  }));

  const productAccordion = document.querySelector('.product-accordion');
  if(productAccordion){
    Promise.all([
      fetch('product-details-1.html').then(r => { if(!r.ok) throw new Error('Productdetails 1 konden niet worden geladen'); return r.text(); }),
      fetch('product-details-2.html').then(r => { if(!r.ok) throw new Error('Productdetails 2 konden niet worden geladen'); return r.text(); })
    ]).then(parts => {
      productAccordion.innerHTML = parts.join('');
      const openHashTarget = () => {
        const target = document.querySelector(window.location.hash);
        if(target && target.matches('details.product-detail')){
          target.open = true;
          setTimeout(() => target.scrollIntoView({behavior:'smooth', block:'start'}), 50);
        }
      };
      openHashTarget();
      window.addEventListener('hashchange', openHashTarget);
    }).catch(err => {
      productAccordion.innerHTML = '<p class="load-error">De uitgebreide productinformatie kon niet worden geladen. Neem contact op met Hobo Hydrauliek voor technische documentatie.</p>';
      console.error(err);
    });
  }
})();
