/* Share / Cite module behaviour.
   Progressive enhancement only — the share links are real anchors that work
   without this file, and the citation text is complete in the static HTML.
   This adds: copy-to-clipboard buttons, and the "Accessed <date>" clause,
   which is deliberately absent from the markup so the crawled citation
   never carries a stale date. */
(function () {
  'use strict';

  // execCommand fallback — for insecure contexts and for browsers where the
  // async Clipboard API exists but rejects (permissions policy, no user
  // activation). Both cases have to be covered: a present-but-rejecting
  // clipboard would otherwise leave the button silently doing nothing.
  function legacyCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:absolute;left:-9999px;top:0';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try {
      ok = document.execCommand('copy');
    } catch (e) {
      ok = false;
    }
    document.body.removeChild(ta);
    return ok;
  }

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () {
        if (legacyCopy(text)) return;
        throw new Error('copy-unavailable');
      });
    }
    return legacyCopy(text) ? Promise.resolve() : Promise.reject(new Error('copy-unavailable'));
  }

  // Last resort: put the text under the user's cursor so ⌘C / Ctrl+C works.
  function selectText(el) {
    try {
      var r = document.createRange();
      r.selectNodeContents(el);
      var sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(r);
      return true;
    } catch (e) {
      return false;
    }
  }

  function flash(btn, message, ok) {
    var label = btn.querySelector('[data-sc-label]') || btn;
    if (btn.dataset.scBusy) return;
    btn.dataset.scBusy = '1';
    var original = label.textContent;
    label.textContent = message;
    if (ok) btn.classList.add('is-done');
    setTimeout(function () {
      label.textContent = original;
      btn.classList.remove('is-done');
      delete btn.dataset.scBusy;
    }, 1800);
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-sc-copy]');
    if (!btn) return;
    e.preventDefault();

    var sel = btn.getAttribute('data-sc-copy');
    var src = sel ? document.querySelector(sel) : null;
    var text = src ? src.textContent.trim() : '';
    if (!text) return;

    copy(text).then(
      function () { flash(btn, 'Copied', true); },
      function () {
        // Every clipboard route failed. Select the text so the reader can copy
        // it by hand, and say so — never leave the button looking inert.
        selectText(src);
        var manual = /Mac|iPhone|iPad/.test(navigator.platform) ? 'Press ⌘C' : 'Press Ctrl+C';
        flash(btn, manual, false);
      }
    );
  });

  // Append the access date to each citation at read time.
  var stamp = new Date().toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric'
  });
  document.querySelectorAll('[data-sc-accessed]').forEach(function (el) {
    if (el.textContent.trim()) return;
    el.textContent = ' Accessed ' + stamp + '.';
  });
})();
