(function () {
  'use strict';

  var CONSENT_KEY = 'fishcare-consent-v1';
  var ADSENSE_CLIENT = 'ca-pub-6697313643773879';
  // Add the public Microsoft Clarity project ID here after creating the project.
  // Clarity is optional analytics and loads only after consent.
  var CLARITY_PROJECT_ID = 'xqyo3mgsli';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    ad_storage: 'denied',
    analytics_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500
  });

  function loadScript(src, id, attrs) {
    if (document.getElementById(id)) return;
    var script = document.createElement('script');
    script.id = id;
    script.async = true;
    script.src = src;
    Object.keys(attrs || {}).forEach(function (key) {
      script.setAttribute(key, attrs[key]);
    });
    document.head.appendChild(script);
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
    loadScript(
      'https://www.clarity.ms/tag/' + encodeURIComponent(CLARITY_PROJECT_ID),
      'fishcare-clarity'
    );
  }

  function enableAds() {
    if (document.documentElement.dataset.adsenseContent !== 'true') return;
    if (document.documentElement.dataset.adsenseApproved !== 'true') return;
    loadScript(
      'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_CLIENT,
      'fishcare-adsense',
      { crossorigin: 'anonymous' }
    );
  }

  function applyConsent(value) {
    var granted = value === 'accepted';
    window.gtag('consent', 'update', {
      ad_storage: granted ? 'granted' : 'denied',
      analytics_storage: granted ? 'granted' : 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    if (granted) {
      enableAnalytics();
      enableAds();
    }
  }

  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (error) {}
    applyConsent(value);
    var banner = document.getElementById('fishcare-consent');
    if (banner) banner.hidden = true;
  }

  function setupConsentBanner() {
    var saved = null;
    try { saved = localStorage.getItem(CONSENT_KEY); } catch (error) {}
    if (saved === 'accepted' || saved === 'rejected') {
      applyConsent(saved);
      return;
    }

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
    banner.querySelectorAll('[data-consent]').forEach(function (button) {
      button.addEventListener('click', function () { setConsent(button.dataset.consent); });
    });
  }

  function setupMobileNavigation() {
    document.querySelectorAll('.nb').forEach(function (nav, index) {
      var links = nav.querySelector('.nlinks, .nav');
      if (!links) return;
      if (!links.id) links.id = 'site-navigation-' + index;

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

      toggle.addEventListener('click', function () {
        var open = links.classList.toggle('open');
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
      });
    });
  }

  function setupGlobalNavigation() {
    if (/^\/(?:admin\/|__forms\.html$|yandex_[^/]+\.html$)/.test(window.location.pathname)) return;

    var navs = document.querySelectorAll('body > nav.nb, body > nav.site-nav');
    var nav = navs[0];

    if (!nav) {
      nav = document.createElement('nav');
      document.body.insertBefore(nav, document.body.firstChild);
    }

    navs.forEach(function (duplicate, index) {
      if (index > 0) duplicate.remove();
    });

    var path = window.location.pathname;
    var section = path === '/' ? 'home' :
      path.indexOf('/guides/') === 0 ? 'guides' :
      path.indexOf('/wiki/') === 0 || path.indexOf('/encyclopedia/') === 0 ? 'wiki' :
      path.indexOf('/tools/') === 0 ? 'tools' :
      path.indexOf('/about/') === 0 ? 'about' : '';

    nav.className = 'nb fishcare-global-nav';
    nav.id = 'fishcare-global-navigation';
    nav.setAttribute('aria-label', 'Main navigation');
    nav.innerHTML =
      '<a class="brand" href="/" aria-label="FishCare AI home">' +
      '<img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"></a>' +
      '<div class="nlinks" id="nlinks">' +
      '<a class="nl' + (section === 'home' ? ' act' : '') + '" href="/">Home</a>' +
      '<a class="nl' + (section === 'guides' ? ' act' : '') + '" href="/guides/">Guides</a>' +
      '<a class="nl' + (section === 'wiki' ? ' act' : '') + '" href="/wiki/">Encyclopedia</a>' +
      '<a class="nl' + (section === 'fish-health' ? ' act' : '') + '" href="/fish-health/">Fish Health</a>' +
      '<a class="nl" href="https://fish-identification-d558af.anysites.app/" style="color:#67e8f9">Fish Identify</a>' +
      '<a class="nl' + (section === 'tools' ? ' act' : '') + '" href="/tools/fish-compatibility-checker/">Tools</a>' +
      '<a class="nl' + (section === 'about' ? ' act' : '') + '" href="/about/">About</a>' +
      '</div>';
  }

  function addLegalLinks() {
    document.querySelectorAll('footer').forEach(function (footer) {
      if (footer.querySelector('.legal-links')) return;
      var links = document.createElement('nav');
      links.className = 'legal-links';
      links.setAttribute('aria-label', 'Legal and company information');
      links.innerHTML = '<a href="/about/">About</a><a href="/contact/">Contact</a>' +
        '<a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a>' +
        '<a href="/image-credits/">Image Credits</a>';
      footer.appendChild(links);
    });
  }

  function ensureContentSchema() {
    if (document.querySelector('script[type="application/ld+json"]')) return;
    if (!/^\/(guides|wiki)\//.test(window.location.pathname)) return;

    var canonical = document.querySelector('link[rel="canonical"]');
    var description = document.querySelector('meta[name="description"]');
    var headline = document.querySelector('h1');
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
    var script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(schema);
    document.head.appendChild(script);
  }

  document.addEventListener('DOMContentLoaded', function () {
    setupGlobalNavigation();
    setupMobileNavigation();
    addLegalLinks();
    ensureContentSchema();
    setupConsentBanner();
  });
})();
