/*
 * App call-to-action, shared by the static site and the species app.
 *
 * Fish-health pages ship a free water-checker box as plain HTML ([data-app-cta]);
 * on an iPhone this script turns it into an App Store box.
 * Tool pages load this script with data-tool="<name>"; on an iPhone it adds an App
 * Store box after the tool's result. Other devices see nothing extra on tools.
 * Tank-size calculators are matched by path, so they need no data-tool attribute.
 *
 * Copy here must match the live app: iPhone only, a free rules-based emergency
 * preview, and everything else behind FishCare Plus. Check ../fishcare-ai-app/src
 * before changing what it promises.
 */
(function () {
  'use strict';

  var STORE_URL = 'https://apps.apple.com/app/fishcare-ai/id6793299571';
  // App Store Connect > App Analytics > Campaigns. Installs are only attributed once set.
  var PROVIDER_TOKEN = '';
  var PLUS_PRICE = 'FishCare Plus ($5.99/mo or $39.99/yr)';

  var FISH_HEALTH_COPY = {
    heading: '🐠 Fish in trouble right now?',
    body: 'The FishCare AI iPhone app starts with a free rules-based health check that shows the risk level, first steps and warning signs. The full report, care plans and records need ' + PLUS_PRICE + '.',
    button: 'Get the iPhone App →'
  };

  var WATER_COPY = {
    heading: '📱 Keep this reading on file',
    body: 'The FishCare AI iPhone app keeps each tank\'s water history, reads test strips from a photo and reminds you when to retest. These features need ' + PLUS_PRICE + '.',
    button: 'Get the iPhone App →'
  };

  var TOOLS = {
    'water-parameter-checker': { ready: '#calc-result[data-analyzed="true"]', copy: WATER_COPY },
    'betta-fish-water-parameters': { ready: '#betta-result[data-analyzed="true"]', copy: WATER_COPY },
    'fish-compatibility-checker': {
      ready: '#compat-results:not(:empty)',
      copy: {
        heading: '📱 Check new fish against your real tank',
        body: 'The FishCare AI iPhone app checks fish from its species guide against your tank size, water type and current residents. It needs ' + PLUS_PRICE + '.',
        button: 'Get the iPhone App →'
      }
    },
    'tank-size': {
      ready: '#result:not(:empty), #gr-result:not(:empty), #rf-result:not(:empty), #tg-result:not(:empty)',
      copy: {
        heading: '📱 Turn this tank plan into a routine',
        body: 'The FishCare AI iPhone app tracks your tanks with care plans, reminders and water records. It needs ' + PLUS_PRICE + '.',
        button: 'Get the iPhone App →'
      }
    },
    'aquarium-planner': {
      ready: '#planner-result .hs',
      resultRoot: '#planner-result',
      copy: {
        heading: '📱 Turn this plan into a routine',
        body: 'The FishCare AI iPhone app tracks your tanks with care plans, reminders and water records. It needs ' + PLUS_PRICE + '.',
        button: 'Get the iPhone App →'
      }
    }
  };

  var script = document.currentScript;
  var toolName = script && script.getAttribute('data-tool');
  if (!toolName && /^\/calculators\/[^/]+-tank-size\//.test(location.pathname)) toolName = 'tank-size';
  var isIphone = /iPhone/.test(navigator.userAgent);

  function storeLink(placement) {
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

  function instrument(box, link, placement, variant) {
    link.addEventListener('click', function () { track('app_cta_click', placement, variant); });
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
      if (isIphone) {
        var heading = box.querySelector('h3, h4');
        var body = box.querySelector('p');
        if (heading) heading.textContent = FISH_HEALTH_COPY.heading;
        if (body) body.textContent = FISH_HEALTH_COPY.body;
        link.textContent = FISH_HEALTH_COPY.button;
        link.href = storeLink(placement);
      }
      instrument(box, link, placement, isIphone ? 'app-store' : 'water-checker');
    });
  }

  function buildToolBox(name, copy) {
    var box = document.createElement('div');
    box.className = 'app-cta-tool';
    box.style.cssText = 'margin:16px 0;padding:18px 20px;border-radius:12px;background:linear-gradient(135deg,#0F3D5E,#2E9E7D);color:#fff;text-align:left';
    var heading = document.createElement('div');
    heading.style.cssText = 'font-weight:700;font-size:1rem;margin-bottom:6px;color:#fff';
    heading.textContent = copy.heading;
    var body = document.createElement('p');
    body.style.cssText = 'margin:0 0 12px;font-size:.86rem;line-height:1.5;color:rgba(255,255,255,.88)';
    body.textContent = copy.body;
    var link = document.createElement('a');
    link.href = storeLink('tool-' + name);
    link.textContent = copy.button;
    link.style.cssText = 'display:inline-block;padding:9px 16px;border-radius:8px;background:#fff;color:#0F3D5E;font-weight:700;font-size:.88rem;text-decoration:none';
    box.appendChild(heading);
    box.appendChild(body);
    box.appendChild(link);
    instrument(box, link, 'tool-' + name, 'app-store');
    return box;
  }

  function initToolBox() {
    var tool = TOOLS[toolName];
    if (!tool || !isIphone) return;
    var box = buildToolBox(toolName, tool.copy);

    function sync() {
      var ready = document.querySelector(tool.ready);
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
      attributeFilter: ['data-analyzed']
    });
    sync();
  }

  function init() {
    initStaticBoxes();
    if (toolName) initToolBox();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
