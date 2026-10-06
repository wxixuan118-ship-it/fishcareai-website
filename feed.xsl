<?xml version="1.0" encoding="UTF-8"?>
<!-- Renders /feed.xml as a readable page when someone opens it in a browser.
     Feed readers ignore the stylesheet and read the raw RSS. -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title><xsl:value-of select="rss/channel/title"/> (RSS feed)</title>
<style>
  body{margin:0;background:#061827;color:#e6f4ff;font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
  main{max-width:760px;margin:0 auto;padding:32px 16px 64px}
  .note{background:#082B43;border:1px solid #0B6FA4;border-radius:12px;padding:14px 16px;font-size:.92rem;color:#9fc3dc}
  .note code{color:#25D7FF;word-break:break-all}
  h1{font-size:1.6rem;margin:24px 0 4px}
  article{padding:18px 0;border-bottom:1px solid #12324a}
  article a{color:#25D7FF;font-weight:700;font-size:1.08rem;text-decoration:none}
  article a:hover{text-decoration:underline}
  time{display:block;font-size:.82rem;color:#7fa6c2;margin:2px 0 6px}
  article p{margin:0;color:#c5dbea}
</style>
</head>
<body>
<main>
  <div class="note">This is the FishCare AI RSS feed. Paste <code>https://www.fishcareai.com/feed.xml</code> into Feedly, Inoreader or any feed reader to get new guides as they are published.</div>
  <h1><xsl:value-of select="rss/channel/title"/></h1>
  <p><xsl:value-of select="rss/channel/description"/><xsl:text> </xsl:text><a href="/" style="color:#25D7FF">Visit the site →</a></p>
  <xsl:for-each select="rss/channel/item">
    <article>
      <a href="{link}"><xsl:value-of select="title"/></a>
      <time><xsl:value-of select="substring(pubDate, 1, 16)"/></time>
      <p><xsl:value-of select="description"/></p>
    </article>
  </xsl:for-each>
</main>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
