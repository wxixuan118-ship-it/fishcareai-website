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
    { label: 'Fish Diseases', href: '/fish-health',                        section: 'fish-diseases' },
    { label: 'Fish Identification', href: '/identify/',     section: '' },
    { label: 'About',         href: '/about/',                              section: 'about' },
    { label: '📱 App',        href: '/app/',                                section: 'app', extraClass: 'nl-app-btn' },
  ];

  // ── Footer link configuration ──────────────────────────────────────────────
  var FOOTER_EXPLORE = [
    { label: 'Fish Species',  href: '/species' },
    { label: 'Fish Diseases', href: '/fish-health' },
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
    { label: '☕ Buy me a coffee', href: 'https://buymeacoffee.com/vikiyananw6' },
  ];

  var COFFEE_URL     = 'https://buymeacoffee.com/vikiyananw6';
  // FormSubmit relays the form to this inbox. The first submission sends an
  // activation email there; nothing is delivered until that link is clicked.
  var FEEDBACK_ENDPOINT = 'https://formsubmit.co/ajax/dev@evetrend.com';

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

  // ── App banner ─────────────────────────────────────────────────────────────
  // Runs on every page, including the Next.js apps that turn the global chrome
  // off (/fish-health, /identify), so it carries its own CSS.
  //   iPhone/iPad: App Store bar, except in iOS Safari on pages with the
  //                apple-itunes-app meta, where Safari shows its own banner.
  //   Android:     Google Play bar once PLAY_LIVE is true; nothing before that.
  //   Desktop:     a small card with a QR code to /app/.
  // Copy must match the live app (hard paywall): no "free" or rating claims.
  var APP_STORE_URL = 'https://apps.apple.com/app/fishcare-ai/id6793299571';
  var PLAY_URL = 'https://play.google.com/store/apps/details?id=com.fishcareai.app';
  // Flip to true once the Play listing stops returning 404.
  var PLAY_LIVE = false;
  // App Store Connect > App Analytics > Campaigns. Installs are only attributed once set.
  var APP_PROVIDER_TOKEN = '';
  var APP_BANNER_KEY = 'fishcare-app-banner-v2';
  var APP_BANNER_SNOOZE_DAYS = 7;

  function appPlatform() {
    var ua = navigator.userAgent;
    if (/iPhone|iPod|iPad/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1)) return 'ios';
    if (/Android/.test(ua)) return 'android';
    if (/Mobi|Tablet/.test(ua)) return 'other-mobile';
    return 'desktop';
  }

  function appStoreLink(placement) {
    var params = 'ct=' + encodeURIComponent('web-' + placement).slice(0, 40) + '&mt=8';
    if (APP_PROVIDER_TOKEN) params = 'pt=' + APP_PROVIDER_TOKEN + '&' + params;
    return APP_STORE_URL + '?' + params;
  }

  function playLink(placement) {
    var ref = 'utm_source=fishcareai.com&utm_medium=web&utm_campaign=' + placement;
    return PLAY_URL + '&referrer=' + encodeURIComponent(ref);
  }

  function trackApp(name, placement, variant) {
    try {
      if (typeof window.gtag === 'function') {
        window.gtag('event', name, { placement: placement, variant: variant, page_path: location.pathname });
      }
    } catch (e) {}
  }

  function appBannerSnoozed() {
    try {
      var until = parseInt(localStorage.getItem(APP_BANNER_KEY), 10);
      return until > Date.now();
    } catch (e) { return false; }
  }

  function injectAppBannerStyles() {
    if (document.getElementById('fishcare-app-bar-css')) return;
    var css = document.createElement('style');
    css.id = 'fishcare-app-bar-css';
    var b = '#fishcare-app-bar';
    css.textContent =
      b + '{position:fixed;z-index:180;left:12px;right:72px;bottom:12px;max-width:460px;box-sizing:border-box;' +
      'display:flex;align-items:center;gap:8px;padding:9px 8px 9px 10px;border-radius:16px;' +
      'background:rgba(5,26,44,.97);border:1px solid rgba(125,235,255,.28);box-shadow:0 14px 40px rgba(0,0,0,.4);' +
      'color:#fff;font:14px/1.3 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;text-align:left;' +
      'transform:translateY(140%);transition:transform .35s ease}' +
      b + '.fcab-show{transform:translateY(0)}' +
      b + ' *{box-sizing:border-box}' +
      b + ' .fcab-icon{width:38px;height:38px;border-radius:10px;flex:0 0 auto;display:block;background:#fff}' +
      b + ' .fcab-text{flex:1;min-width:0}' +
      b + ' .fcab-name{font-weight:700;font-size:.92rem;color:#fff;margin:0}' +
      b + ' .fcab-sub{font-size:.75rem;color:rgba(234,251,255,.7);margin:2px 0 0}' +
      b + ':not(.fcab-desktop) .fcab-name{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
      b + ':not(.fcab-desktop) .fcab-sub{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}' +
      b + ' .fcab-cta{flex:0 0 auto;padding:8px 12px;border-radius:10px;background:#2EB8FF;color:#03223A!important;' +
      'font-weight:700;font-size:.85rem;text-decoration:none!important;white-space:nowrap}' +
      b + ' .fcab-close{flex:0 0 auto;width:24px;height:28px;margin:0;padding:0;border:0;background:none;' +
      'color:rgba(234,251,255,.55);font-size:20px;line-height:28px;cursor:pointer;align-self:flex-start}' +
      b + ' .fcab-close:hover{color:#fff}' +
      b + '.fcab-desktop{left:20px;right:auto;bottom:20px;width:300px;flex-wrap:wrap;padding:14px}' +
      b + ' .fcab-qr{display:flex;gap:12px;align-items:center;width:100%;margin-top:4px}' +
      b + ' .fcab-qr img{width:92px;height:92px;border-radius:8px;background:#fff;padding:4px;flex:0 0 auto}' +
      b + ' .fcab-qr p{margin:0;font-size:.78rem;color:rgba(234,251,255,.75)}' +
      b + ' .fcab-qr a{color:#7debff;font-weight:600}' +
      '@media (max-width:760px){' + b + '.fcab-desktop{display:none}}' +
      '@media print{' + b + '{display:none}}';
    document.head.appendChild(css);
  }

  function setupAppBanner() {
    var path = window.location.pathname;
    // /app/ is the download page; koi pages are left out because the app has no pond tank type.
    if (/^\/(?:app\/|admin\/|delete-account\/|__forms\.html$|yandex_[^/]+\.html$)/.test(path)) return;
    if (/koi/.test(path)) return;
    if (document.getElementById('fishcare-app-bar') || appBannerSnoozed()) return;

    var platform = appPlatform();
    var ua = navigator.userAgent;
    var iosSafari = platform === 'ios' && /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS|GSA\//.test(ua);
    if (iosSafari && document.querySelector('meta[name="apple-itunes-app"]')) return;
    if (platform === 'android' && !PLAY_LIVE) return;
    if (platform === 'other-mobile') return;

    var placement = 'floating-bar';
    var variant = platform === 'desktop' ? 'desktop-qr' : platform;
    var name = 'FishCare AI';
    var sub = 'Fish health check, reminders and water records';
    var html;
    if (platform === 'desktop') {
      var stores = PLAY_LIVE ? 'iPhone, iPad and Android' : 'iPhone and iPad';
      html =
        '<img class="fcab-icon" src="/assets/pwa/apple-touch-icon.png" alt="" width="42" height="42">' +
        '<div class="fcab-text"><p class="fcab-name">' + name + ' for ' + stores + '</p>' +
        '<p class="fcab-sub">' + sub + '</p></div>' +
        '<button class="fcab-close" type="button" aria-label="Dismiss">&times;</button>' +
        '<div class="fcab-qr"><img src="/assets/app-qr.svg" alt="QR code for the FishCare AI app page" width="92" height="92">' +
        '<p>Scan with your phone camera to get the app.<br><a class="fcab-link" href="/app/?utm_source=web&amp;utm_medium=floating-card">See the app</a></p></div>';
    } else {
      var href = platform === 'ios' ? appStoreLink(placement) : playLink(placement);
      html =
        '<img class="fcab-icon" src="/assets/pwa/apple-touch-icon.png" alt="" width="42" height="42">' +
        '<div class="fcab-text"><p class="fcab-name">' + name + '</p>' +
        '<p class="fcab-sub">Health checks &amp; reminders</p></div>' +
        '<a class="fcab-cta fcab-link" href="' + href + '" target="_blank" rel="noopener">Get the app</a>' +
        '<button class="fcab-close" type="button" aria-label="Dismiss">&times;</button>';
    }

    function show() {
      if (document.getElementById('fishcare-app-bar')) return;
      injectAppBannerStyles();
      var bar = document.createElement('aside');
      bar.id = 'fishcare-app-bar';
      bar.setAttribute('aria-label', 'Get the FishCare AI app');
      if (platform === 'desktop') bar.className = 'fcab-desktop';
      bar.innerHTML = html;
      document.body.appendChild(bar);
      setTimeout(function () { bar.classList.add('fcab-show'); }, 60);
      trackApp('app_cta_view', placement, variant);
      Array.prototype.forEach.call(bar.querySelectorAll('.fcab-link'), function (a) {
        a.addEventListener('click', function () { trackApp('app_cta_click', placement, variant); });
      });
      bar.querySelector('.fcab-close').addEventListener('click', function () {
        bar.classList.remove('fcab-show');
        setTimeout(function () { bar.remove(); }, 350);
        trackApp('app_cta_dismiss', placement, variant);
        try {
          localStorage.setItem(APP_BANNER_KEY, String(Date.now() + APP_BANNER_SNOOZE_DAYS * 864e5));
        } catch (e) {}
      });
    }

    // Wait for the consent banner to go away so the two never stack.
    function whenConsentClear(fn) {
      var consent = document.getElementById('fishcare-consent');
      if (!consent || consent.hidden) return fn();
      var obs = new MutationObserver(function () {
        if (!document.body.contains(consent) || consent.hidden) { obs.disconnect(); setTimeout(fn, 1500); }
      });
      obs.observe(consent, { attributes: true, attributeFilter: ['hidden'] });
    }

    setTimeout(function () { whenConsentClear(show); }, 3000);
  }

  // ── Floating "Buy me a coffee" + feedback buttons ─────────────────────────
  // Self-contained styles so it also works on pages without the global CSS.
  // Sits below the app and consent banners (z-index 200 / 1000).
  function setupFloatingActions() {
    if (/^\/(?:admin\/|__forms\.html$|yandex_[^/]+\.html$)/.test(window.location.pathname)) return;
    if (document.getElementById('fishcare-fab')) return;

    var css = document.createElement('style');
    css.id = 'fishcare-fab-css';
    css.textContent =
      '#fishcare-fab{position:fixed;right:20px;bottom:24px;z-index:190;display:flex;' +
      'flex-direction:column;gap:12px;align-items:flex-end;font-family:inherit}' +
      '#fishcare-fab .ffab-btn{width:52px;height:52px;border-radius:50%;border:0;margin:0;cursor:pointer;display:flex;' +
      'align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,.35);' +
      'transition:transform .15s ease;text-decoration:none;padding:0}' +
      '#fishcare-fab .ffab-btn:hover{transform:scale(1.08)}' +
      '#fishcare-fab .ffab-coffee{background:#FFDD00;color:#000;font-size:24px}' +
      '#fishcare-fab .ffab-feedback{background:#fff!important;color:#0F3D6E!important;border:0!important;padding:0!important}' +
      '#fishcare-feedback.ffab-panel{position:fixed;right:20px;bottom:150px;z-index:1001;width:320px;max-width:calc(100vw - 32px);' +
      'background:rgba(4,25,41,.98);color:#fff;border:1px solid rgba(125,235,255,.35);border-radius:16px;' +
      'box-shadow:0 24px 80px rgba(0,0,0,.52);padding:18px;font-size:.9rem}' +
      '#fishcare-feedback[hidden]{display:none}' +
      '#fishcare-feedback h2{margin:0 0 4px;font-size:1.05rem;color:#fff}' +
      '#fishcare-feedback p{margin:0 0 12px;color:rgba(255,255,255,.7);font-size:.82rem}' +
      '#fishcare-feedback textarea,#fishcare-feedback input{width:100%;box-sizing:border-box;margin:0 0 10px;padding:10px;' +
      'border-radius:10px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.06);' +
      'color:#fff;font:inherit;font-size:.88rem}' +
      '#fishcare-feedback textarea{min-height:110px;resize:vertical}' +
      '#fishcare-feedback .ffab-actions{display:flex;gap:8px;justify-content:flex-end}' +
      '#fishcare-feedback .ffab-actions button{padding:9px 14px;border-radius:10px;cursor:pointer;font-size:.85rem;' +
      'border:1px solid rgba(255,255,255,.45)!important;background:transparent!important;color:#fff!important;box-shadow:none!important;margin:0}' +
      '#fishcare-feedback .ffab-actions .ffab-send{background:#27AE60!important;border-color:#27AE60!important}' +
      '#fishcare-feedback .ffab-actions button:disabled{opacity:.6;cursor:default}' +
      '#fishcare-feedback .ffab-status{min-height:1em;margin:0 0 8px;font-size:.82rem;color:#7debff}' +
      '#fishcare-feedback .ffab-hp{position:absolute;left:-9999px}' +
      '@media(max-width:620px){#fishcare-fab{right:14px;bottom:18px}#fishcare-fab .ffab-btn{width:46px;height:46px}' +
      '#fishcare-fab .ffab-coffee{font-size:21px}#fishcare-feedback.ffab-panel{right:16px;bottom:130px}}';
    document.head.appendChild(css);

    var wrap = document.createElement('div');
    wrap.id = 'fishcare-fab';
    wrap.innerHTML =
      '<a class="ffab-btn ffab-coffee" href="' + COFFEE_URL + '" target="_blank" rel="noopener" ' +
        'aria-label="Buy me a coffee" title="Buy me a coffee">☕</a>' +
      '<button class="ffab-btn ffab-feedback" type="button" aria-label="Send feedback" title="Send feedback" ' +
        'aria-expanded="false" aria-controls="fishcare-feedback">' +
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.6 8.6 0 0 1-3.8-.9L3 20.5l1.5-4.6A8.4 8.4 0 1 1 21 11.5z"/></svg>' +
      '</button>';

    var panel = document.createElement('form');
    panel.id = 'fishcare-feedback';
    panel.className = 'ffab-panel';
    panel.hidden = true;
    panel.setAttribute('aria-label', 'Send feedback');
    panel.innerHTML =
      '<h2>Send us feedback</h2>' +
      '<p>Found a mistake, have an idea, or need help? We read every message.</p>' +
      '<textarea name="message" required maxlength="4000" placeholder="Your feedback"></textarea>' +
      '<input type="email" name="email" maxlength="200" placeholder="Your email (optional, for a reply)">' +
      '<input class="ffab-hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<div class="ffab-status" role="status"></div>' +
      '<div class="ffab-actions">' +
        '<button type="button" class="ffab-cancel">Close</button>' +
        '<button type="submit" class="ffab-send">Send</button>' +
      '</div>';

    document.body.appendChild(wrap);
    document.body.appendChild(panel);

    var toggle = wrap.querySelector('.ffab-feedback');
    var status = panel.querySelector('.ffab-status');
    var send = panel.querySelector('.ffab-send');

    function setOpen(open) {
      panel.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
      if (open) panel.querySelector('textarea').focus();
    }
    toggle.addEventListener('click', function () { setOpen(panel.hidden); });
    panel.querySelector('.ffab-cancel').addEventListener('click', function () { setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) setOpen(false); });

    panel.addEventListener('submit', function (e) {
      e.preventDefault();
      var message = panel.message.value.trim();
      if (!message) return;
      if (panel._honey.value) { setOpen(false); return; }
      send.disabled = true;
      status.textContent = 'Sending…';
      var email = panel.email.value.trim();
      var payload = {
        _subject: 'FishCare AI feedback',
        _template: 'table',
        _captcha: 'false',
        message: message,
        page: window.location.href
      };
      if (email) { payload.email = email; payload._replyto = email; }
      fetch(FEEDBACK_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (r) { return r.json(); }).then(function (data) {
        if (String(data.success) !== 'true') throw new Error(data.message || 'failed');
        panel.reset();
        status.textContent = 'Thanks! Your feedback was sent.';
        setTimeout(function () { setOpen(false); status.textContent = ''; }, 2500);
      }).catch(function () {
        status.innerHTML = 'Could not send. Please email <a style="color:#7debff" ' +
          'href="mailto:dev@evetrend.com">dev@evetrend.com</a>.';
      }).then(function () { send.disabled = false; });
    });
  }

  function init() {
    setupFloatingActions();
    if (globalChromeEnabled()) {
      setupGlobalNavigation();
      setupGlobalFooter();
      setupMobileNavigation();
      addLegalLinks();
    } else {
      injectConsentBannerStyles();
      setupGlobalFooter();
    }
    ensureContentSchema();
    setupConsentBanner();
    setupAppBanner();
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
