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
    { label: 'Encyclopedia',  href: '/wiki/',                               section: 'wiki' },
    { label: 'Fish Diseases', href: '/aquarium-fish-diseases/',              section: 'fish-diseases' },
    { label: 'Fish Identify', href: 'https://identify.fishcareai.com/',     section: '' },
    { label: 'About',         href: '/about/',                              section: 'about' },
    { label: '📱 App',        href: '/app/',                                section: 'app', extraClass: 'nl-app-btn' },
  ];

  // ── Footer link configuration ──────────────────────────────────────────────
  var FOOTER_EXPLORE = [
    { label: 'Fish Species',  href: '/wiki/' },
    { label: 'Fish Diseases', href: '/aquarium-fish-diseases/' },
    { label: 'Guides',        href: '/guides/' },
    { label: 'Aquarium Tools',href: '/tools/' },
    { label: 'Fish Identify', href: 'https://identify.fishcareai.com/' },
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
    return '<div class="ftcol"><h5>' + heading + '</h5>' + links + '</div>';
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

  // ── Inject global footer ───────────────────────────────────────────────────
  function setupGlobalFooter() {
    if (/^\/(?:admin\/|__forms\.html$|yandex_[^/]+\.html$)/.test(window.location.pathname)) return;

    var footer = document.querySelector('body > footer.ft');
    if (!footer) return; // page has its own custom footer, skip

    // If footer already has the full grid, don't duplicate
    if (footer.querySelector('.ftg')) return;

    var year = new Date().getFullYear();
    var grid =
      '<div class="con">' +
        '<div class="ftg">' +
          '<div class="ftbr">' +
            '<div class="logo">FishCare AI</div>' +
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
        '</nav>' +
      '</div>';

    footer.innerHTML = grid;
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
        '<a href="/image-credits/">Image Credits</a>';
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
          '<div class="fab-phone"><img src="/assets/app-screenshot.png" alt="FishCare AI app" loading="lazy"></div>' +
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

  document.addEventListener('DOMContentLoaded', function () {
    setupGlobalNavigation();
    setupGlobalFooter();
    setupMobileNavigation();
    addLegalLinks();
    ensureContentSchema();
    setupConsentBanner();
    setupAppBanner();
  });
})();
