(() => {
  const path = window.location.pathname.replace(/\/$/, '');
  const recommendations = {
    '/tools/tank-size-calculator': {
      targets: ['#vol-result'],
      eyebrow: 'Related tool',
      title: 'Now calculate how many fish you can stock',
      description: 'Compare adult size, water needs and temperament before adding fish.',
      href: '/tools/fish-compatibility-checker/',
      button: 'Fish Compatibility Checker →'
    },
    '/tools/aquarium-size-calculator': {
      targets: ['#vol-result'],
      eyebrow: 'Related tool',
      title: 'Check which fish fit this aquarium',
      description: 'Use your tank volume as the starting point, then compare compatible species.',
      href: '/tools/fish-compatibility-checker/',
      button: 'Fish Compatibility Checker →'
    },
    '/tools/fish-compatibility-checker': {
      targets: ['#compat-results'],
      eyebrow: 'Related tool',
      title: 'Confirm your tank has enough water volume',
      description: 'Calculate usable gallons before finalising a fish combination.',
      href: '/tools/tank-size-calculator/',
      button: 'Tank Size Calculator →'
    },
    '/tools/fish-feeding-calculator': {
      targets: ['#feeding-result'],
      eyebrow: 'Related tool',
      title: 'Keep feeding from affecting water quality',
      description: 'Check the readings that can change when a tank is overfed.',
      href: '/tools/water-parameter-checker/',
      button: 'Water Parameter Checker →'
    },
    '/tools/water-parameter-checker': {
      targets: ['#calc-result'],
      eyebrow: 'Related tool',
      title: 'Match equipment to your aquarium',
      description: 'Use your tank size to plan filtration, heating and circulation.',
      href: '/tools/aquarium-equipment-calculator/',
      button: 'Equipment Calculator →'
    },
    '/tools/aquarium-equipment-calculator': {
      targets: ['#equip-result'],
      eyebrow: 'Related tool',
      title: 'Check the water your equipment needs to protect',
      description: 'Review the core readings after setting up filtration and heating.',
      href: '/tools/water-parameter-checker/',
      button: 'Water Parameter Checker →'
    },
    '/tools/aquarium-planner': {
      targets: ['#tank-result'],
      eyebrow: 'Related tool',
      title: 'Calculate your aquarium’s usable water',
      description: 'Turn the recommended tank size into real gallons, litres and water weight.',
      href: '/tools/tank-size-calculator/',
      button: 'Tank Size Calculator →'
    }
  };

  const config = recommendations[path];
  if (!config) return;

  const placeholderPattern = /results? will show|choose a species|build a feeding plan|enter your water test|select (?:a |at least |two |fish)|add fish to compare|waiting for/i;
  const card = (item) => `<aside class="tool-related-card" aria-label="Related tool recommendation"><span class="tool-related-eyebrow">${config.eyebrow}</span><strong>${config.title}</strong><p>${config.description}</p><a href="${config.href}">${config.button}</a></aside>`;

  const addCardWhenReady = (target) => {
    const text = target.textContent.replace(/\s+/g, ' ').trim();
    const existing = target.querySelector('.tool-related-card');
    if (existing || !text || placeholderPattern.test(text)) return;
    target.insertAdjacentHTML('beforeend', card(config));
  };

  const start = () => {
    const style = document.createElement('style');
    style.textContent = '.tool-related-card{margin:18px 0 0;padding:18px;border:1px solid rgba(52,198,193,.55);border-radius:14px;background:linear-gradient(135deg,rgba(17,104,128,.24),rgba(28,180,166,.13));color:inherit}.tool-related-card strong{display:block;margin-top:4px;font-size:1.08rem;line-height:1.35}.tool-related-card p{margin:7px 0 14px;line-height:1.55}.tool-related-eyebrow{display:block;font-size:.72rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;opacity:.78}.tool-related-card a{display:inline-block;padding:10px 14px;border-radius:8px;background:#19b8ae;color:#06293a!important;font-weight:800;text-decoration:none}.tool-related-card a:hover,.tool-related-card a:focus-visible{background:#77f2e8;outline:2px solid currentColor;outline-offset:2px}';
    document.head.appendChild(style);
    config.targets.forEach((selector) => {
      const target = document.querySelector(selector);
      if (!target) return;
      addCardWhenReady(target);
      new MutationObserver(() => addCardWhenReady(target)).observe(target, { childList: true, subtree: true });
    });
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
