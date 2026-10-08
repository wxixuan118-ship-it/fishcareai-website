(function () {
  'use strict';

  var CONSENT_KEY      = 'fishcare-consent-v1';
  var ADSENSE_CLIENT   = 'ca-pub-6697313643773879';
  var CLARITY_PROJECT_ID = 'xqyo3mgsli';

  // ── Single source of truth for all navigation items ───────────────────────
  var NAV_ITEMS = [
    { label: 'Home',          href: '/',                                    section: 'home' },
    { label: 'Guides',        href: '/guides/',                             section: 'guides' },
    { label: 'Tools',         href: '/tools/',                              section: 'tools' },
    { label: 'Encyclopedia',  href: '/species',                              section: 'wiki' },
    { label: 'Fish Diseases', href: '/fish-health/',                        section: 'fish-diseases' },
    { label: 'Fish Identification', href: '/identify/',     section: '' },
    { label: 'About',         href: '/about/',                              section: 'about' },
    { label: '📱 App',        href: '/app/',                                section: 'app', extraClass: 'nl-app-btn' },
  ];

  // ── Footer link configuration ──────────────────────────────────────────────
  var FOOTER_EXPLORE = [
    { label: 'Fish Species',  href: '/species' },
    { label: 'Fish Diseases', href: '/fish-health/' },
    { label: 'Clownfish Health Problems', href: '/aquarium-fish-diseases/clownfish/' },
    { label: 'Guides',        href: '/guides/' },
    { label: 'Aquarium Tools',href: '/tools/' },
    { label: 'Fish Identification', href: '/identify/' },
  ];
  var FOOTER_TOOLS = [
    { label: 'Aquarium Size Calculator',  href: '/tools/aquarium-size-calculator/' },
    { label: 'Fish Compatibility Checker',href: '/tools/fish-compatibility-checker/' },
    { label: 'Water Parameter Checker',   href: '/tools/water-parameter-checker/' },
    { label: 'Fish Feeding Calculator',   href: '/tools/fish-feeding-calculator/' },
    { label: 'Aquarium Planner',          href: '/tools/aquarium-planner/' },
  ];
  var FOOTER_COMPANY = [
    { label: 'About',         href: '/about/' },
    { label: 'Contact',       href: '/contact/' },
    { label: 'Privacy Policy',href: '/privacy/' },
    { label: 'Terms',         href: '/terms/' },
    { label: 'Editorial Policy', href: '/editorial-policy/' },
    { label: 'Resources',     href: '/resources/' },
    { label: 'Add Your Site', href: '/add-your-site/' },
  ];

  // ── Analytics / Ads ───────────────────────────────────────────────────────
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    ad_storage: 'denied', analytics_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied',
    wait_for_update: 500
  });

  function loadScript(src, id, attrs) {
    if (document.getElementById(id)) return;
    var s = document.createElement('script');
    s.id = id; s.async = true; s.src = src;
    Object.keys(attrs || {}).forEach(function (k) { s.setAttribute(k, attrs[k]); });
    document.head.appendChild(s);
  }

  function enableAnalytics() {
    loadScript('https://www.googletagmanager.com/gtag/js?id=G-1L92P7VP30', 'fishcare-ga');
    window.gtag('js', new Date());
    window.gtag('config', 'G-1L92P7VP30', { anonymize_ip: true });
    enableClarity();
  }

  function enableClarity() {
    if (!CLARITY_PROJECT_ID || document.getElementById('fishcare-clarity')) return;
    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    loadScript('https://www.clarity.ms/tag/' + encodeURIComponent(CLARITY_PROJECT_ID), 'fishcare-clarity');
  }

  function enableAds() {
    if (document.documentElement.dataset.adsenseContent !== 'true') return;
    if (document.documentElement.dataset.adsenseApproved !== 'true') return;
    loadScript(
      'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_CLIENT,
      'fishcare-adsense', { crossorigin: 'anonymous' }
    );
  }

  function applyConsent(value) {
    var granted = value === 'accepted';
    window.gtag('consent', 'update', {
      ad_storage: granted ? 'granted' : 'denied',
      analytics_storage: granted ? 'granted' : 'denied',
      ad_user_data: 'denied', ad_personalization: 'denied'
    });
    if (granted) { enableAnalytics(); enableAds(); }
  }

  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (e) {}
    applyConsent(value);
    var banner = document.getElementById('fishcare-consent');
    if (banner) banner.hidden = true;
  }

  // ── Global chrome opt-out ─────────────────────────────────────────────────
  // Pages that ship their own header/footer and do not load
  // fishcare-glass-redesign.css set <html data-global-chrome="false">. They
  // still get analytics and the consent banner, but keep their own layout.
  function globalChromeEnabled() {
    return document.documentElement.getAttribute('data-global-chrome') !== 'false';
  }

  // Minimal consent-banner styling for pages without the global stylesheet.
  function injectConsentBannerStyles() {
    if (document.getElementById('fishcare-consent-css')) return;
    var css = document.createElement('style');
    css.id = 'fishcare-consent-css';
    css.textContent =
      '.consent-banner{position:fixed;z-index:1000;left:18px;right:18px;bottom:18px;' +
      'display:flex;align-items:center;justify-content:space-between;gap:20px;' +
      'max-width:980px;margin:auto;padding:18px 20px;color:#fff;' +
      'background:rgba(4,25,41,.97);border:1px solid rgba(125,235,255,.35);' +
      'border-radius:18px;box-shadow:0 24px 80px rgba(0,0,0,.52);font-size:.88rem}' +
      '.consent-banner[hidden]{display:none}' +
      '.consent-banner strong{font-size:.95rem}' +
      '.consent-banner p{margin:4px 0 0;font-size:.88rem}' +
      '.consent-banner a{color:#7debff}' +
      '.consent-actions{display:flex;gap:10px;flex-shrink:0}' +
      '.consent-actions button{padding:9px 14px;font-size:.82rem;cursor:pointer;' +
      'border-radius:10px;border:1px solid rgba(255,255,255,.45);' +
      'background:transparent;color:#fff}' +
      '.consent-actions button.consent-accept{background:#27AE60;border-color:#27AE60}' +
      '@media(max-width:620px){.consent-banner{flex-direction:column;align-items:stretch}}';
    document.head.appendChild(css);
  }

  function setupConsentBanner() {
    var saved = null;
    try { saved = localStorage.getItem(CONSENT_KEY); } catch (e) {}
    if (saved === 'accepted' || saved === 'rejected') { applyConsent(saved); return; }
    var banner = document.createElement('section');
    banner.id = 'fishcare-consent';
    banner.className = 'consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Privacy choices');
    banner.innerHTML =
      '<div><strong>Your privacy choices</strong>' +
      '<p>We use optional analytics and advertising cookies only with your consent. ' +
      '<a href="/privacy/">Read our privacy policy</a>.</p></div>' +
      '<div class="consent-actions">' +
      '<button type="button" data-consent="rejected">Reject optional cookies</button>' +
      '<button type="button" class="consent-accept" data-consent="accepted">Accept</button>' +
      '</div>';
    document.body.appendChild(banner);
    banner.querySelectorAll('[data-consent]').forEach(function (btn) {
      btn.addEventListener('click', function () { setConsent(btn.dataset.consent); });
    });
  }

  // ── Determine active section from URL path ─────────────────────────────────
  function getActiveSection() {
    var path = window.location.pathname;
    if (path === '/')                                         return 'home';
    if (path.indexOf('/guides/')  === 0)                     return 'guides';
    if (path.indexOf('/tools/')   === 0)                     return 'tools';
    if (path.indexOf('/wiki/')    === 0 ||
        path.indexOf('/encyclopedia/') === 0 ||
        path.indexOf('/species')  === 0)                     return 'wiki';
    if (path.indexOf('/aquarium-fish-diseases') === 0 ||
        path.indexOf('/fish-health') === 0)                   return 'fish-diseases';
    if (path.indexOf('/app/')     === 0)                     return 'app';
    if (path.indexOf('/about/')   === 0)                     return 'about';
    return '';
  }

  // ── Render the site header ─────────────────────────────────────────────────
  function renderHeader() {
    var section = getActiveSection();
    var links = NAV_ITEMS.map(function (item) {
      var isActive = item.section && item.section === section;
      var cls = 'nl' + (isActive ? ' act' : '') + (item.extraClass ? ' ' + item.extraClass : '');
      var ariaCurrent = isActive ? ' aria-current="page"' : '';
      return '<a class="' + cls + '" href="' + item.href + '"' + ariaCurrent + '>' + item.label + '</a>';
    }).join('');

    return (
      '<a class="brand" href="/" aria-label="FishCare AI home">' +
        '<img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36">' +
      '</a>' +
      '<div class="nlinks" id="fishcare-nlinks">' + links + '</div>'
    );
  }

  // ── Render a footer column ─────────────────────────────────────────────────
  function renderFooterCol(heading, items) {
    var links = items.map(function (item) {
      return '<a href="' + item.href + '">' + item.label + '</a>';
    }).join('');
    return '<div class="ftcol"><h3>' + heading + '</h3>' + links + '</div>';
  }

  // ── Inject global header ───────────────────────────────────────────────────
  function setupGlobalNavigation() {
    if (/^\/(?:admin\/|__forms\.html$|yandex_[^/]+\.html$)/.test(window.location.pathname)) return;

    // Remove duplicate navs; keep or create the first one
    var navs = document.querySelectorAll('body > nav.nb, body > nav.site-nav');
    var nav = navs[0];
    navs.forEach(function (el, i) { if (i > 0) el.remove(); });

    if (!nav) {
      nav = document.createElement('nav');
      document.body.insertBefore(nav, document.body.firstChild);
    }

    nav.className = 'nb fishcare-global-nav';
    nav.id = 'fishcare-global-navigation';
    nav.setAttribute('aria-label', 'Main navigation');
    nav.innerHTML = renderHeader();
  }

  // ── Global footer styles ───────────────────────────────────────────────────
  // Every page (static, proxied apps, chrome-opt-out pages) gets the same
  // footer look from here, independent of the page's own stylesheet.
  function injectFooterStyles() {
    if (document.getElementById('fishcare-footer-css')) return;
    // :root + doubled class out-ranks page rules such as
    // body.tools-dark-page a:not(.btn):not(.bp):not(.tbtn){color:...!important}
    var f = ':root body footer.ft.fc-footer.fc-footer';
    var css = document.createElement('style');
    css.id = 'fishcare-footer-css';
    css.textContent =
      f + '{display:block;background:#051A2C!important;border-top:1px solid rgba(255,255,255,.08)!important;' +
        'padding:64px 24px 32px!important;margin:0!important;color:rgba(255,255,255,.66);text-align:left;' +
        'font-family:inherit;line-height:1.6;font-size:16px;box-shadow:none!important;border-radius:0!important;max-width:none!important;width:auto!important}' +
      f + ' .con{max-width:1200px;margin:0 auto;padding:0}' +
      f + ' .ftg{display:grid;grid-template-columns:1.6fr repeat(3,1fr);gap:36px;margin:0 0 40px}' +
      f + ' .ftbr .logo{display:inline-block;margin:0 0 16px;line-height:0}' +
      f + ' .ftbr img{display:block;height:40px;width:auto;filter:none}' +
      f + ' .ftbr p{max-width:300px;margin:0;font-size:14px;line-height:1.65;color:rgba(255,255,255,.6)!important}' +
      f + ' .ftcol h3{margin:0 0 14px;padding:0;color:#fff!important;font-size:12px;font-weight:700;' +
        'text-transform:uppercase;letter-spacing:.12em;border:0;background:none}' +
      f + ' .ftcol a{display:block;margin:0;padding:4px 0;font-size:14px;color:rgba(255,255,255,.66)!important;text-decoration:none}' +
      f + ' a:hover{color:#8FF0E2!important}' +
      f + ' .ftb{margin:0;padding:20px 0 0;border-top:1px solid rgba(255,255,255,.1);text-align:left;font-size:13px;color:rgba(255,255,255,.5)!important}' +
      f + ' .ftb.badge-rail-wrap{border-top:0;padding-top:0;margin-top:12px}' +
      f + ' .legal-links{display:flex;flex-wrap:wrap;justify-content:flex-start;gap:6px 22px;margin:14px 0 0;padding:0}' +
      f + ' .legal-links a{padding:0;font-size:13px;color:rgba(255,255,255,.5)!important;text-decoration:none}' +
      '@media(max-width:900px){' + f + ' .ftg{grid-template-columns:1fr 1fr;gap:28px}' + f + ' .ftbr{grid-column:1/-1}}' +
      '@media(max-width:600px){' + f + '{padding:48px 16px 28px!important}}';
    document.head.appendChild(css);
  }

  // ── Inject global footer ───────────────────────────────────────────────────
  // One footer for the whole site. Any existing footer markup is replaced;
  // only the homepage badge rail (.badge-rail-wrap) is carried over.
  function setupGlobalFooter() {
    if (/^\/(?:admin\/|__forms\.html$|yandex_[^/]+\.html$)/.test(window.location.pathname)) return;

    var footer = document.querySelector('body > footer.ft');
    if (!footer && !globalChromeEnabled()) {
      // chrome-opt-out pages ship a plain <footer>; take over the last one
      // that is not part of an article
      var plain = Array.prototype.filter.call(document.querySelectorAll('footer'), function (el) {
        return !el.closest('article, main, section');
      });
      footer = plain[plain.length - 1] || null;
    }
    if (!footer) {
      footer = document.createElement('footer');
      document.body.appendChild(footer);
    }
    if (footer.getAttribute('data-global-footer') === '1') return;

    injectFooterStyles();
    var badges = footer.querySelector('.badge-rail-wrap');
    if (badges) badges.parentNode.removeChild(badges);

    footer.className = 'ft fc-footer';
    footer.setAttribute('data-global-footer', '1');

    var year = new Date().getFullYear();
    var grid =
      '<div class="con">' +
        '<div class="ftg">' +
          '<div class="ftbr">' +
            '<a class="logo" href="/" aria-label="FishCare AI home"><img class="fishcare-footer-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="158" height="40"></a>' +
            '<p>Practical aquarium care guides, fish encyclopedia, and free tools for freshwater and saltwater fishkeepers.</p>' +
          '</div>' +
          renderFooterCol('Explore', FOOTER_EXPLORE) +
          renderFooterCol('Popular Tools', FOOTER_TOOLS) +
          renderFooterCol('Company', FOOTER_COMPANY) +
        '</div>' +
        '<div class="ftb">© ' + year + ' EverTrend LLC. FishCare AI is a product of EverTrend LLC. All rights reserved.</div>' +
        '<nav class="legal-links" aria-label="Legal and company information">' +
          '<a href="/about/">About</a><a href="/contact/">Contact</a>' +
          '<a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a>' +
          '<a href="/image-credits/">Image Credits</a>' +
          '<a href="/add-your-site/">Add Your Site</a>' +
        '</nav>' +
      '</div>';

    footer.innerHTML = grid;
    if (badges) {
      var con = footer.querySelector('.con');
      con.insertBefore(badges, con.querySelector('.legal-links'));
    }
  }

  function addLegalLinks() {
    document.querySelectorAll('footer').forEach(function (footer) {
      if (footer.querySelector('.legal-links')) return;
      var nav = document.createElement('nav');
      nav.className = 'legal-links';
      nav.setAttribute('aria-label', 'Legal and company information');
      nav.innerHTML =
        '<a href="/about/">About</a><a href="/contact/">Contact</a>' +
        '<a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a>' +
        '<a href="/image-credits/">Image Credits</a>' +
        '<a href="/add-your-site/">Add Your Site</a>';
      footer.appendChild(nav);
    });
  }

  // ── Mobile navigation (hamburger menu) ────────────────────────────────────
  function setupMobileNavigation() {
    document.querySelectorAll('.nb').forEach(function (nav, index) {
      var links = nav.querySelector('#fishcare-nlinks, .nlinks, .nav');
      if (!links) return;
      if (!links.id) links.id = 'site-nav-' + index;

      // Replace or create the hamburger toggle
      var oldToggle = nav.querySelector('.hbg');
      var toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'hbg';
      toggle.setAttribute('aria-label', 'Open navigation menu');
      toggle.setAttribute('aria-controls', links.id);
      toggle.setAttribute('aria-expanded', 'false');
      toggle.innerHTML = '<span></span><span></span><span></span>';
      if (oldToggle) oldToggle.replaceWith(toggle);
      else nav.appendChild(toggle);

      function openMenu() {
        links.classList.add('open');
        toggle.setAttribute('aria-expanded', 'true');
        toggle.setAttribute('aria-label', 'Close navigation menu');
        toggle.classList.add('hbg-open');
      }

      function closeMenu() {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open navigation menu');
        toggle.classList.remove('hbg-open');
      }

      toggle.addEventListener('click', function () {
        links.classList.contains('open') ? closeMenu() : openMenu();
      });

      // Escape closes the menu
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMenu();
      });

      // Click outside closes the menu
      document.addEventListener('click', function (e) {
        if (!nav.contains(e.target)) closeMenu();
      });
    });
  }

  // ── Article schema injection ───────────────────────────────────────────────
  function ensureContentSchema() {
    if (document.querySelector('script[type="application/ld+json"]')) return;
    if (!/^\/(guides|wiki)\//.test(window.location.pathname)) return;
    var canonical   = document.querySelector('link[rel="canonical"]');
    var description = document.querySelector('meta[name="description"]');
    var headline    = document.querySelector('h1');
    if (!canonical || !headline) return;
    var schema = {
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: headline.textContent.trim(),
      description: description ? description.content : '',
      mainEntityOfPage: canonical.href,
      author: { '@type': 'Organization', name: 'FishCare AI Editorial Team' },
      publisher: { '@type': 'Organization', name: 'FishCare AI', url: 'https://www.fishcareai.com/' }
    };
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify(schema);
    document.head.appendChild(s);
  }

  // ── App popup banner ───────────────────────────────────────────────────────
  function setupAppBanner() {
    // pages that opt out of the app popup (they also drop the iOS smart-banner meta)
    if (['/calculators/zebra-danio-tank-size/', '/calculators/koi-fish-tank-size/', '/calculators/goldfish-tank-size/', '/calculators/discus-fish-tank-size/', '/calculators/betta-fish-tank-size/', '/calculators/oscar-fish-tank-size/', '/calculators/angelfish-tank-size/', '/calculators/guppy-tank-size/', '/calculators/molly-fish-tank-size/', '/calculators/swordtail-fish-tank-size/', '/guides/fish-care-for-beginners/'].indexOf(window.location.pathname) !== -1) return;
    if (/^\/(?:app\/|admin\/|aquarium-fish-diseases\/|tools\/|__forms\.html$|yandex_[^/]+\.html$)/.test(window.location.pathname)) return;
    // iOS Safari already shows the native Smart App Banner
    if (/iP(?:hone|ad|od)/.test(navigator.userAgent) &&
        /Safari/.test(navigator.userAgent) && !/CriOS|FxiOS/.test(navigator.userAgent)) return;
    var KEY = 'fishcare-app-banner-v1';
    try { if (localStorage.getItem(KEY) === 'dismissed') return; } catch (e) {}
    setTimeout(function () {
      var banner = document.createElement('div');
      banner.id = 'fishcare-app-banner';
      banner.innerHTML =
        '<div class="fab-content">' +
          '<div class="fab-text">' +
            '<div class="fab-text-top">' +
              '<span class="fab-text-store">App Store</span>' +
              '<span class="fab-text-stars">★★★★★</span>' +
            '</div>' +
            '<div class="fab-text-name">FishCare AI</div>' +
            '<div class="fab-text-sub">AI Health Check &amp; Care Plans</div>' +
          '</div>' +
          '<a class="fab-cta" href="https://apps.apple.com/app/fishcare-ai/id6793299571" target="_blank" rel="noopener">Get the app</a>' +
          '<button class="fab-close" type="button" aria-label="Dismiss">&times;</button>' +
        '</div>';
      document.body.appendChild(banner);
      setTimeout(function () { banner.classList.add('fab-show'); }, 60);
      banner.querySelector('.fab-close').addEventListener('click', function () {
        banner.classList.remove('fab-show');
        setTimeout(function () { banner.remove(); }, 350);
        try { localStorage.setItem(KEY, 'dismissed'); } catch (e) {}
      });
    }, 3000);
  }

  function init() {
    if (globalChromeEnabled()) {
      setupGlobalNavigation();
      setupGlobalFooter();
      setupMobileNavigation();
      addLegalLinks();
      setupAppBanner();
    } else {
      injectConsentBannerStyles();
      setupGlobalFooter();
    }
    ensureContentSchema();
    setupConsentBanner();
    registerServiceWorker();
  }

  // Makes the site installable (PWA) and serves /offline.html when a page
  // can't load. sw.js only intercepts failed navigations, so it is safe for
  // the proxied /species, /fish-health and /identify apps too.
  function registerServiceWorker() {
    if (!('serviceWorker' in navigator) || location.hostname !== 'www.fishcareai.com') return;
    var register = function () {
      navigator.serviceWorker.register('/sw.js').catch(function () {});
    };
    // The Next.js apps inject this script after the load event has fired.
    if (document.readyState === 'complete') register();
    else window.addEventListener('load', register);
  }

  // The script is normally deferred, but it is also injected after load by the
  // Next.js apps behind /species and /fish-health, where DOMContentLoaded has
  // already fired.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
