/*
 * App call-to-action, shared by the static site and the species app.
 *
 * What a visitor sees depends on the device:
 *   iPhone/iPad  App Store box
 *   Android      Google Play box once PLAY_LIVE is true; until then, nothing
 *   Desktop      the same box with a QR code to /app/ instead of a store button
 *
 * Fish-health pages ship a free water-checker box as plain HTML ([data-app-cta]);
 * on iOS (and Android once Play is live) this script turns it into a store box.
 * Desktop keeps the water checker there. Long fish-health pages also get a second
 * box before the FAQ (not on the 80 deep-rewrite test pages until the 11/23 check).
 * Tool pages load this script with data-tool="<name>"; a box is added after the
 * tool's result. Tank-size calculators, and tools whose slug is a key in TOOLS, are
 * matched by path, so they need no data-tool attribute.
 * Compatibility pages and care guides without a static box get a box from
 * placeAutoBox(); long guides get a second one near the top. Koi pond tools are
 * left out: the app has no pond tank type.
 *
 * Copy here must match the live app: a free rules-based emergency preview, and
 * everything else behind FishCare Plus. Check ../fishcare-ai-app/src before
 * changing what it promises.
 */
(function () {
  'use strict';

  var STORE_URL = 'https://apps.apple.com/app/fishcare-ai/id6793299571';
  var PLAY_URL = 'https://play.google.com/store/apps/details?id=com.fishcareai.app';
  // Flip to true once the Play listing stops returning 404 (also in site-compliance.js).
  var PLAY_LIVE = false;
  // App Store Connect > App Analytics > Campaigns. Installs are only attributed once set.
  var PROVIDER_TOKEN = '';
  var PLUS_PRICE = 'FishCare Plus ($5.99/mo or $39.99/yr)';

  // Deep-rewrite test pages (reports/fish-health-deep-test-2026-09-28.csv): keep
  // their layout unchanged until the 11/23 re-check.
  var FREEZE_UNTIL = Date.UTC(2026, 10, 24);
  var FROZEN_HEALTH = ['blood-parrot-cichlid-black-spots','blood-parrot-cichlid-white-spots','oscar-not-eating','betta-fish-curled-body','bristlenose-pleco-aggressive','common-pleco-jumping','common-pleco-floating','ember-tetra-pale-color','blood-parrot-cichlid-aggressive','neon-tetra-bloated','guppy-black-spots','neon-tetra-aggressive','blood-parrot-cichlid-hiding','common-pleco-aggressive','guppy-losing-color','dwarf-gourami-bloated','guppy-not-eating','ember-tetra-aggressive','flowerhorn-cichlid-not-eating','betta-imbellis-curled-body','ember-tetra-hiding','bristlenose-pleco-hiding','chili-rasbora-pale-color','common-pleco-pale-color','dwarf-gourami-aggressive','guppy-fin-rot','betta-fish-darting','kuhli-loach-jumping','molly-black-spots','cardinal-tetra-pale-color','oscar-pale-color','goldfish-losing-color','betta-fish-rapid-breathing','blood-parrot-cichlid-not-eating','kuhli-loach-pale-color','molly-hiding','flowerhorn-cichlid-jumping','molly-aggressive','rainbow-shark-hiding','bristlenose-pleco-black-spots','flowerhorn-cichlid-losing-color','common-pleco-hiding','goldfish-jumping','betta-fish-black-spots','koi-not-eating','weather-fish-floating','guppy-jumping','bristlenose-pleco-torn-fins','bristlenose-pleco-bloated','guppy-hiding','ember-tetra-losing-color','silver-arowana-not-eating','betta-fish-floating','molly-jumping','betta-fish-jumping','black-neon-tetra-pale-color','guppy-bloated','flowerhorn-cichlid-cloudy-eyes','cardinal-tetra-white-spots','black-neon-tetra-hiding','cardinal-tetra-losing-color','oscar-jumping','flowerhorn-cichlid-aggressive','blood-parrot-cichlid-swimming-sideways','blood-parrot-cichlid-losing-color','neon-tetra-hiding','guppy-curled-body','honey-gourami-bloated','bristlenose-pleco-pale-color','common-pleco-torn-fins','bristlenose-pleco-not-eating','common-pleco-not-eating','common-pleco-losing-color','guppy-rapid-breathing','silver-arowana-jumping','weather-fish-jumping','giant-gourami-bloated','dwarf-gourami-losing-color','oscar-white-spots','honey-gourami-hiding'];

  var ua = navigator.userAgent;
  var platform = /iPhone|iPod|iPad/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1) ? 'ios'
    : /Android/.test(ua) ? 'android'
    : /Mobi|Tablet/.test(ua) ? 'other' : 'desktop';
  // app-store | play | qr | null
  var target = platform === 'ios' ? 'app-store'
    : platform === 'android' ? (PLAY_LIVE ? 'play' : null)
    : platform === 'desktop' ? 'qr' : null;
  var APP = platform === 'ios' ? 'The FishCare AI app for iPhone and iPad'
    : platform === 'android' ? 'The FishCare AI Android app'
    : 'The FishCare AI app for ' + (PLAY_LIVE ? 'iPhone, iPad and Android' : 'iPhone and iPad');
  var BUTTON = target === 'play' ? 'Get it on Google Play →' : 'Get it on the App Store →';

  var FISH_HEALTH_COPY = {
    heading: '🐠 Fish in trouble right now?',
    body: APP + ' starts with a free rules-based health check that shows the risk level, first steps and warning signs. The full report, care plans and records need ' + PLUS_PRICE + '.'
  };

  var WATER_COPY = {
    heading: '📱 Keep this reading on file',
    body: APP + ' keeps each tank\'s water history, reads test strips from a photo and reminds you when to retest. These features need ' + PLUS_PRICE + '.'
  };

  var PLAN_COPY = {
    heading: '📱 Turn this tank plan into a routine',
    body: APP + ' tracks your tanks with care plans, reminders and water records. It needs ' + PLUS_PRICE + '.'
  };

  var COMPAT_COPY = {
    heading: '📱 Check new fish against your real tank',
    body: APP + ' checks fish from its species guide against your tank size, water type and current residents. It needs ' + PLUS_PRICE + '.'
  };

  var GUIDE_COPY = {
    heading: '📱 Keep your tank on schedule',
    body: APP + ' tracks your tanks with feeding and water-change reminders, care plans and water records. If a fish looks unwell, it starts with a free rules-based health check. Other features need ' + PLUS_PRICE + '.'
  };

  var FEEDING_COPY = {
    heading: '📱 Get feeding reminders',
    body: APP + ' sets feeding and water-change reminders and keeps care records for each tank. It needs ' + PLUS_PRICE + '.'
  };

  // changed: show the box once the result element differs from its initial
  // content and is visible, for tools whose result starts as a placeholder.
  var TOOLS = {
    'aquarium-equipment-calculator': { ready: '#equip-result:not(:empty)', copy: PLAN_COPY },
    'aquarium-heater-calculator': { ready: '#h-out', changed: true, copy: PLAN_COPY },
    'aquarium-size-calculator': { ready: '#vol-result', changed: true, copy: PLAN_COPY },
    'aquarium-substrate-calculator': { ready: '#sub-result:not(:empty)', copy: PLAN_COPY },
    'aquarium-weight-calculator': { ready: '#w-out', changed: true, copy: PLAN_COPY },
    'fish-feeding-calculator': { ready: '#feeding-result:not(:empty)', copy: FEEDING_COPY },
    'fish-tank-stocking-calculator': { ready: '#stock-result:not(:empty)', copy: COMPAT_COPY },
    'water-parameter-checker': { ready: '#calc-result[data-analyzed="true"]', copy: WATER_COPY },
    'betta-fish-water-parameters': { ready: '#betta-result[data-analyzed="true"]', copy: WATER_COPY },
    'fish-compatibility-checker': {
      ready: '#compat-results:not(:empty)',
      copy: COMPAT_COPY
    },
    'tank-size': {
      ready: '#result:not(:empty), #gr-result:not(:empty), #rf-result:not(:empty), #tg-result:not(:empty)',
      copy: PLAN_COPY
    },
    'aquarium-planner': {
      ready: '#planner-result .hs',
      resultRoot: '#planner-result',
      copy: {
        heading: '📱 Turn this plan into a routine',
        body: APP + ' tracks your tanks with care plans, reminders and water records. It needs ' + PLUS_PRICE + '.'
      }
    }
  };

  var script = document.currentScript;
  var toolName = script && script.getAttribute('data-tool');
  if (!toolName && /^\/calculators\/[^/]+-tank-size\//.test(location.pathname)) toolName = 'tank-size';
  if (!toolName) {
    var toolSlug = (location.pathname.match(/^\/tools\/([^/]+)\/?$/) || [])[1];
    if (toolSlug && Object.prototype.hasOwnProperty.call(TOOLS, toolSlug)) toolName = toolSlug;
  }
  if (/koi/.test(location.pathname)) toolName = null;

  function storeLink(placement) {
    if (target === 'play') {
      return PLAY_URL + '&referrer=' + encodeURIComponent('utm_source=fishcareai.com&utm_medium=web&utm_campaign=' + placement);
    }
    var params = 'ct=' + encodeURIComponent('web-' + placement).slice(0, 40) + '&mt=8';
    if (PROVIDER_TOKEN) params = 'pt=' + PROVIDER_TOKEN + '&' + params;
    return STORE_URL + '?' + params;
  }

  function track(name, placement, variant) {
    try {
      if (typeof window.gtag === 'function') {
        window.gtag('event', name, { placement: placement, variant: variant, page_path: location.pathname });
      }
    } catch (e) {}
  }

  function instrument(box, links, placement, variant) {
    Array.prototype.forEach.call(links, function (link) {
      link.addEventListener('click', function () { track('app_cta_click', placement, variant); });
    });
    if (!('IntersectionObserver' in window)) return;
    var observer = new IntersectionObserver(function (entries) {
      if (!entries.some(function (entry) { return entry.isIntersecting; })) return;
      observer.disconnect();
      track('app_cta_view', placement, variant);
    }, { threshold: 0.5 });
    observer.observe(box);
  }

  function initStaticBoxes() {
    var boxes = document.querySelectorAll('[data-app-cta]');
    Array.prototype.forEach.call(boxes, function (box) {
      var placement = box.getAttribute('data-app-cta');
      var link = box.querySelector('a');
      if (!link) return;
      var toStore = target === 'app-store' || target === 'play';
      if (toStore) {
        var heading = box.querySelector('h3, h4');
        var body = box.querySelector('p');
        if (heading) heading.textContent = FISH_HEALTH_COPY.heading;
        if (body) body.textContent = FISH_HEALTH_COPY.body;
        link.textContent = BUTTON;
        link.href = storeLink(placement);
      }
      instrument(box, [link], placement, toStore ? target : 'water-checker');
    });
  }

  function buildBox(placement, copy) {
    var box = document.createElement('div');
    box.className = 'app-cta-tool';
    box.setAttribute('data-app-cta-auto', placement);
    box.style.cssText = 'margin:16px 0;padding:18px 20px;border-radius:12px;background:linear-gradient(135deg,#0F3D5E,#2E9E7D);color:#fff;text-align:left;' +
      (target === 'qr' ? 'display:flex;flex-wrap:wrap;align-items:center;gap:16px' : '');
    var text = document.createElement('div');
    text.style.cssText = target === 'qr' ? 'flex:1 1 260px;min-width:0' : '';
    var heading = document.createElement('div');
    heading.style.cssText = 'font-weight:700;font-size:1rem;margin-bottom:6px;color:#fff';
    heading.textContent = copy.heading;
    var body = document.createElement('p');
    body.style.cssText = 'margin:0 0 12px;font-size:.86rem;line-height:1.5;color:rgba(255,255,255,.88)';
    body.textContent = copy.body;
    text.appendChild(heading);
    text.appendChild(body);
    box.appendChild(text);
    var link = document.createElement('a');
    var linkCss = 'display:inline-block;padding:9px 16px;border-radius:8px;background:#fff;color:#0F3D5E;font-weight:700;font-size:.88rem;text-decoration:none';
    if (target === 'qr') {
      link.href = '/app/?utm_source=web&utm_medium=' + encodeURIComponent(placement);
      link.textContent = 'See the app →';
      link.style.cssText = linkCss;
      text.appendChild(link);
      var qr = document.createElement('div');
      qr.style.cssText = 'flex:0 0 auto;text-align:center;font-size:.72rem;color:rgba(255,255,255,.8)';
      qr.innerHTML = '<img src="/assets/app-qr.svg" alt="QR code for the FishCare AI app page" width="104" height="104" loading="lazy" ' +
        'style="display:block;width:104px;height:104px;margin:0 auto 6px;padding:5px;border-radius:8px;background:#fff">Scan with your phone';
      box.appendChild(qr);
    } else {
      link.href = storeLink(placement);
      link.target = '_blank';
      link.rel = 'noopener';
      link.textContent = BUTTON;
      link.style.cssText = linkCss;
      text.appendChild(link);
    }
    instrument(box, [link], placement, target);
    return box;
  }

  function initToolBox() {
    var tool = TOOLS[toolName];
    if (!tool || !target) return;
    var box = buildBox('tool-' + toolName, tool.copy);
    var initial = tool.changed && document.querySelector(tool.ready);
    var initialHtml = initial ? initial.innerHTML : null;

    function sync() {
      var ready = document.querySelector(tool.ready);
      if (ready && tool.changed) {
        var html = ready.innerHTML;
        if (!html.trim() || html === initialHtml || ready.offsetParent === null) ready = null;
      }
      if (!ready) {
        if (box.parentNode) box.parentNode.removeChild(box);
        return;
      }
      var root = tool.resultRoot ? document.querySelector(tool.resultRoot) : ready;
      if (root && root.nextElementSibling !== box) root.insertAdjacentElement('afterend', box);
    }

    new MutationObserver(sync).observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['data-analyzed', 'class', 'style', 'hidden']
    });
    sync();
  }

  function topBlock(el, root) {
    while (el.parentElement && el.parentElement !== root) el = el.parentElement;
    return el;
  }

  function faqHeading(headings) {
    return Array.prototype.filter.call(headings, function (h) {
      return /faq|frequently asked/i.test(h.textContent);
    })[0];
  }

  function placeAutoBox() {
    if (!target || toolName || document.querySelector('[data-app-cta]')) return;
    var path = location.pathname;
    var kind = /^\/compatibility\/[^/]+\/?$/.test(path) ? 'compat'
      : /^\/guides\/.+/.test(path) ? 'guide-care' : null;
    if (!kind) return;
    var root = document.querySelector('article') || document.querySelector('main');
    if (!root) return;
    var headings = root.querySelectorAll('h2');
    if (!headings.length) return;
    if (kind === 'compat') {
      // After the first section, which holds the verdict.
      topBlock(headings[0], root).insertAdjacentElement('afterend', buildBox('compat', COMPAT_COPY));
      return;
    }
    var faq = faqHeading(headings);
    var faqBlock = faq && topBlock(faq, root);
    if (faqBlock) faqBlock.insertAdjacentElement('beforebegin', buildBox('guide-care', GUIDE_COPY));
    else root.appendChild(buildBox('guide-care', GUIDE_COPY));
    // Long care guides: a second box after the opening sections, so readers who
    // never reach the FAQ still see one.
    if (headings.length >= 10) {
      var early = topBlock(headings[3], root);
      if (early !== faqBlock && early.previousElementSibling && !early.previousElementSibling.hasAttribute('data-app-cta-auto')) {
        early.insertAdjacentElement('beforebegin', buildBox('guide-care-top', GUIDE_COPY));
      }
    }
  }

  // Fish-health symptom pages: a second box before the FAQ, after the treatment
  // and vet sections.
  function placeFishHealthEnd() {
    if (!target) return;
    var slug = (location.pathname.match(/^\/fish-health\/([^/]+)\/?$/) || [])[1];
    if (!slug || !document.querySelector('[data-app-cta]')) return;
    if (Date.now() < FREEZE_UNTIL && FROZEN_HEALTH.indexOf(slug) !== -1) return;
    var root = document.querySelector('article') || document.querySelector('main');
    if (!root || root.querySelector('[data-app-cta-auto="fish-health-end"]')) return;
    var faq = faqHeading(root.querySelectorAll('h2'));
    if (!faq) return;
    topBlock(faq, root).insertAdjacentElement('beforebegin', buildBox('fish-health-end', FISH_HEALTH_COPY));
  }

  function init() {
    initStaticBoxes();
    if (toolName) initToolBox();
    placeAutoBox();
    placeFishHealthEnd();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
