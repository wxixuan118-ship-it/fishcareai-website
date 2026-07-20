(function () {
  'use strict';
  var form = document.querySelector('[data-vercel-contact]');
  if (!form) return;
  var statusBox = document.getElementById('contact-status');
  var status = new URLSearchParams(window.location.search).get('status');
  if (status && statusBox) {
    statusBox.hidden = false;
    statusBox.textContent = status === 'service-unavailable'
      ? 'The contact service is being configured. Please try again later.'
      : 'Your message could not be sent. Check the fields and try again.';
  }
  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    var button = form.querySelector('button[type="submit"]');
    if (button) { button.disabled = true; button.textContent = 'Sending…'; }
    if (statusBox) statusBox.hidden = true;
    try {
      var response = await fetch('/api/contact', {
        method: 'POST',
        headers: { Accept: 'application/json', 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()
      });
      if (!response.ok) throw new Error('submission-failed');
      window.location.assign('/thank-you/');
    } catch (error) {
      if (statusBox) { statusBox.hidden = false; statusBox.textContent = 'Your message could not be sent. Please try again later.'; }
      if (button) { button.disabled = false; button.textContent = 'Send message'; }
    }
  });
})();
