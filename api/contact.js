const ALLOWED_TOPICS = new Set([
  'Fish care question', 'Guide correction', 'Source request', 'Topic suggestion',
  'Privacy request', 'Partnership', 'Technical issue'
]);

function redirect(response, location) {
  response.statusCode = 303;
  response.setHeader('Location', location);
  response.end();
}

function escapeHtml(value) {
  return String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
}

async function parseBody(request) {
  if (request.body && typeof request.body === 'object') return request.body;
  if (typeof request.body === 'string') return Object.fromEntries(new URLSearchParams(request.body));
  let raw = '';
  for await (const chunk of request) {
    raw += chunk;
    if (raw.length > 20000) throw new Error('payload-too-large');
  }
  return Object.fromEntries(new URLSearchParams(raw));
}

function sendError(request, response, status, code) {
  if ((request.headers.accept || '').includes('application/json')) {
    return response.status(status).json({ ok: false, error: code });
  }
  return redirect(response, `/contact/?status=${encodeURIComponent(code)}`);
}

export default async function handler(request, response) {
  response.setHeader('Cache-Control', 'no-store');
  response.setHeader('X-Robots-Tag', 'noindex, nofollow');
  if (request.method !== 'POST') {
    response.setHeader('Allow', 'POST');
    return sendError(request, response, 405, 'method-not-allowed');
  }
  if (Number(request.headers['content-length'] || 0) > 20000) {
    return sendError(request, response, 413, 'message-too-large');
  }

  const origin = request.headers.origin;
  if (origin) {
    let hostname = '';
    try { hostname = new URL(origin).hostname; } catch (error) {}
    const allowed = hostname === 'fishcareai.com' || hostname === 'www.fishcareai.com' || hostname.endsWith('.vercel.app');
    if (!allowed) return sendError(request, response, 403, 'invalid-origin');
  }

  let body;
  try { body = await parseBody(request); }
  catch (error) { return sendError(request, response, 400, 'invalid-request'); }

  if (String(body['bot-field'] || '').trim()) {
    return (request.headers.accept || '').includes('application/json')
      ? response.status(200).json({ ok: true }) : redirect(response, '/thank-you/');
  }

  const name = String(body.name || '').trim();
  const email = String(body.email || '').trim().toLowerCase();
  const topic = String(body.topic || '').trim();
  const message = String(body.message || '').trim();
  const source = String(body.source || 'contact-page').trim().slice(0, 80);
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (name.length < 2 || name.length > 100 || !emailPattern.test(email) || email.length > 254 ||
      !ALLOWED_TOPICS.has(topic) || message.length < 10 || message.length > 5000) {
    return sendError(request, response, 400, 'invalid-fields');
  }

  const apiKey = process.env.RESEND_API_KEY;
  const toEmail = process.env.CONTACT_TO_EMAIL;
  const fromEmail = process.env.CONTACT_FROM_EMAIL;
  if (!apiKey || !toEmail || !fromEmail) {
    console.error('Contact form environment variables are not configured.');
    return sendError(request, response, 503, 'service-unavailable');
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  let delivery;
  try {
    delivery = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: fromEmail, to: [toEmail], reply_to: email,
        subject: `[FishCare AI] ${topic}`,
        text: `Name: ${name}\nEmail: ${email}\nTopic: ${topic}\nSource: ${source}\n\n${message}`,
        html: `<h2>New FishCare AI contact message</h2><p><strong>Name:</strong> ${escapeHtml(name)}</p><p><strong>Email:</strong> ${escapeHtml(email)}</p><p><strong>Topic:</strong> ${escapeHtml(topic)}</p><p><strong>Source:</strong> ${escapeHtml(source)}</p><hr><p style="white-space:pre-wrap">${escapeHtml(message)}</p>`
      }),
      signal: controller.signal
    });
  } catch (error) {
    console.error('Resend request failed:', error.message);
    return sendError(request, response, 502, 'delivery-failed');
  } finally { clearTimeout(timeout); }

  if (!delivery.ok) {
    console.error('Resend rejected contact email:', delivery.status, await delivery.text());
    return sendError(request, response, 502, 'delivery-failed');
  }
  return (request.headers.accept || '').includes('application/json')
    ? response.status(200).json({ ok: true }) : redirect(response, '/thank-you/');
}
