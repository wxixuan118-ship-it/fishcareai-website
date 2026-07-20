(function () {
  'use strict';

  var CONSENT_KEY = 'fishcare-consent-v1';
  var ADSENSE_CLIENT = 'ca-pub-6697313643773879';

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

  document.addEventListener('DOMContentLoaded', function () {
    setupMobileNavigation();
    addLegalLinks();
    setupConsentBanner();
  });
})();
