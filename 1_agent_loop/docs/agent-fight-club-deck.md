---
marp: true
paginate: true
size: 16:9
title: When AI Agents Go Shopping
author: Agent Fight Club
style: |
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

  :root {
    --bg: hsl(43, 100%, 50%);
    --bg-hot: hsl(43, 88%, 42%);
    --bg-deep: hsl(43, 95%, 45%);
    --ink: hsl(0, 0%, 4%);
    --ink-soft: hsla(0, 0%, 4%, 0.72);
    --ink-faint: hsla(0, 0%, 4%, 0.42);
    --paper: hsl(43, 100%, 92%);
    --panel: hsla(0, 0%, 4%, 0.06);
    --panel-strong: hsla(0, 0%, 4%, 0.10);
    --line: hsl(0, 0%, 4%);
    --hot: hsl(0, 78%, 48%);
    --green: hsl(140, 65%, 32%);
    --night: hsl(0, 0%, 4%);
    --night-fg: hsl(43, 100%, 50%);
  }

  section {
    background: var(--bg);
    color: var(--ink);
    font-family: 'IBM Plex Mono', 'JetBrains Mono', monospace;
    font-size: 24px;
    line-height: 1.45;
    padding: 56px 72px;
    justify-content: flex-start;
    position: relative;
  }

  /* Page numbers — terminal flavored */
  section::after {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--ink);
    font-size: 12px;
    letter-spacing: 0.16em;
    opacity: 0.6;
  }

  h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 64px;
    line-height: 1.0;
    letter-spacing: -0.05em;
    color: var(--ink);
    margin: 0 0 24px 0;
    text-transform: uppercase;
  }

  h2 {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--ink);
    margin: 0 0 18px 0;
    border-bottom: 2px solid var(--ink);
    padding-bottom: 6px;
    display: inline-block;
  }

  h3 {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 26px;
    color: var(--ink);
    margin: 0 0 12px 0;
    letter-spacing: -0.02em;
  }

  p { margin: 0 0 12px 0; }

  strong { color: var(--ink); font-weight: 700; }
  em { color: var(--ink-soft); font-style: normal; text-decoration: underline; text-decoration-thickness: 2px; }

  ul, ol {
    margin: 0;
    padding-left: 0;
    list-style: none;
  }

  li {
    padding: 10px 0 10px 28px;
    border-bottom: 1px dashed var(--ink);
    position: relative;
    font-size: 22px;
  }
  li:last-child { border-bottom: none; }
  li::before {
    content: '▸';
    position: absolute;
    left: 0;
    top: 8px;
    font-weight: 700;
    color: var(--ink);
  }

  code {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88em;
    color: var(--ink);
    background: var(--panel-strong);
    padding: 1px 6px;
    border: 1px solid var(--ink);
  }

  pre {
    background: var(--night);
    color: var(--night-fg);
    border: 2px solid var(--ink);
    padding: 16px 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    line-height: 1.45;
    overflow: hidden;
    box-shadow: 6px 6px 0 var(--ink);
  }
  pre code { background: transparent; border: none; color: var(--night-fg); padding: 0; }

  blockquote {
    border: none;
    border-left: 6px solid var(--ink);
    padding: 4px 18px;
    margin: 16px 0;
    color: var(--ink);
    font-style: normal;
    font-size: 22px;
    background: var(--panel);
  }

  hr {
    border: none;
    border-top: 2px solid var(--ink);
    margin: 20px 0;
  }

  section table {
    display: table !important;
    border-collapse: collapse;
    table-layout: fixed;
    width: 100% !important;
    font-size: 18px;
    background: var(--paper);
    border: 2px solid var(--ink);
    overflow: visible !important;
  }
  section table thead, section table tbody { display: table-row-group; }
  section table tr { display: table-row; }
  section table th, section table td { display: table-cell; }
  section table th, section table td {
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid var(--ink);
    color: var(--ink);
    word-wrap: break-word;
    overflow-wrap: break-word;
  }
  section table th + th, section table td + td {
    border-left: 1px solid var(--ink);
  }
  section table th {
    background: var(--bg-hot);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 12px;
  }
  section table tr:last-child td { border-bottom: none; }

  /* ---- Title slide ---- */
  section.title {
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    padding: 64px 72px;
    background:
      repeating-linear-gradient(
        90deg,
        transparent 0,
        transparent 22px,
        rgba(0,0,0,0.04) 22px,
        rgba(0,0,0,0.04) 23px
      ),
      var(--bg);
  }
  section.title .chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: var(--ink);
    border: 2px solid var(--ink);
    padding: 8px 14px;
    display: inline-block;
    background: var(--bg);
    margin-bottom: 28px;
  }
  section.title .wordmark {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 132px;
    line-height: 0.92;
    letter-spacing: -0.07em;
    color: var(--ink);
    text-transform: uppercase;
    margin: 0 0 18px 0;
  }
  section.title .wordmark .alt { color: var(--hot); }
  section.title .tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 18px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--ink);
    border-top: 2px solid var(--ink);
    padding-top: 16px;
    max-width: 920px;
  }
  section.title .meta {
    position: absolute;
    bottom: 40px;
    left: 72px;
    right: 72px;
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--ink);
    border-top: 1px solid var(--ink);
    padding-top: 12px;
  }
  section.title h1 { display: none; }

  /* ---- Big title / section break ---- */
  section.bigtitle {
    justify-content: center;
    align-items: flex-start;
    padding: 72px 80px;
  }
  section.bigtitle .num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 18px;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: var(--ink);
    border: 2px solid var(--ink);
    padding: 8px 14px;
    background: var(--bg);
    display: inline-block;
    margin-bottom: 36px;
  }
  section.bigtitle h1 {
    font-size: 110px;
    line-height: 0.95;
    letter-spacing: -0.06em;
    margin: 0;
    max-width: 1180px;
  }
  section.bigtitle .kicker {
    margin-top: 28px;
    max-width: 980px;
    font-size: 22px;
    color: var(--ink);
    border-top: 2px solid var(--ink);
    padding-top: 16px;
  }
  section.bigtitle .kicker strong { background: var(--ink); color: var(--bg); padding: 1px 6px; }
  section.bigtitle .glyph {
    position: absolute;
    top: 64px;
    right: 80px;
    font-size: 200px;
    line-height: 1;
    filter: drop-shadow(8px 8px 0 var(--ink));
  }

  /* ---- Quote / pull-line slide ---- */
  section.pull {
    justify-content: center;
    align-items: flex-start;
    padding: 80px 96px;
  }
  section.pull .line {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 72px;
    line-height: 1.03;
    letter-spacing: -0.04em;
    max-width: 1180px;
  }
  section.pull .line .hl { background: var(--ink); color: var(--bg); padding: 0 8px; }
  section.pull .attrib {
    margin-top: 36px;
    font-size: 14px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--ink-soft);
  }

  /* ---- Four icon row (the four setups) ---- */
  section.row4 .grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 28px;
  }
  section.row4 .cell {
    border: 2px solid var(--ink);
    padding: 24px 18px;
    background: var(--bg);
    box-shadow: 6px 6px 0 var(--ink);
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 280px;
  }
  section.row4 .cell .num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
  }
  section.row4 .cell .glyph { font-size: 64px; line-height: 1; }
  section.row4 .cell .name {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 22px;
    line-height: 1.1;
    text-transform: uppercase;
    letter-spacing: -0.02em;
  }
  section.row4 .cell .body {
    font-size: 15px;
    line-height: 1.4;
    color: var(--ink-soft);
    margin-top: auto;
  }

  /* ---- Two columns ---- */
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin-top: 12px; }
  .cols.heavy > div {
    border: 2px solid var(--ink);
    background: var(--bg);
    padding: 24px 28px;
    box-shadow: 6px 6px 0 var(--ink);
  }

  /* ---- Three columns ---- */
  .cols3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 12px; }
  .cols3 .card {
    border: 2px solid var(--ink);
    background: var(--bg);
    padding: 22px 22px;
    box-shadow: 6px 6px 0 var(--ink);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .cols3 .card .glyph { font-size: 44px; line-height: 1; }
  .cols3 .card .head {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 20px;
    text-transform: uppercase;
    letter-spacing: -0.01em;
  }
  .cols3 .card .body {
    font-size: 16px;
    color: var(--ink-soft);
    line-height: 1.4;
  }

  /* ---- 2x2 matrix (game theory) ---- */
  section.matrix .setup {
    display: flex;
    flex-wrap: wrap;
    gap: 14px 28px;
    align-items: center;
    border: 2px solid var(--ink);
    border-left: 6px solid var(--ink);
    background: var(--paper);
    padding: 12px 18px;
    margin: 6px 0 14px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    color: var(--ink);
    box-shadow: 4px 4px 0 var(--ink);
  }
  section.matrix .setup span { white-space: nowrap; }
  section.matrix .setup code { font-size: 0.95em; }
  section.matrix .grid {
    display: grid;
    grid-template-columns: 220px 1fr 1fr;
    grid-template-rows: 60px 1fr 1fr;
    margin-top: 18px;
    border: 2px solid var(--ink);
    background: var(--bg);
    box-shadow: 8px 8px 0 var(--ink);
    min-height: 420px;
  }
  section.matrix .gh, section.matrix .gv {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 12px 14px;
    background: var(--ink);
    color: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  section.matrix .corner { background: var(--ink); }
  section.matrix .gv { writing-mode: horizontal-tb; }
  section.matrix .cell {
    padding: 18px 22px;
    border-left: 2px solid var(--ink);
    border-top: 2px solid var(--ink);
    display: flex;
    flex-direction: column;
    gap: 8px;
    justify-content: center;
  }
  section.matrix .cell .pay {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 44px;
    letter-spacing: -0.04em;
  }
  section.matrix .cell .lbl {
    font-size: 15px;
    color: var(--ink-soft);
    text-transform: uppercase;
    letter-spacing: 0.12em;
  }
  section.matrix .cell.eq { background: var(--bg-hot); }
  section.matrix .cell.eq .pay { color: var(--ink); }
  section.matrix .cell.eq .stamp {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    border: 2px solid var(--ink);
    padding: 4px 8px;
    align-self: flex-start;
    background: var(--bg);
  }

  /* ---- Big stat ---- */
  section.stat { justify-content: center; }
  section.stat .num {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 220px;
    line-height: 0.9;
    letter-spacing: -0.06em;
  }
  section.stat .cap {
    font-size: 24px;
    margin-top: 18px;
    max-width: 900px;
    line-height: 1.4;
  }
  section.stat .cap strong { background: var(--ink); color: var(--bg); padding: 1px 6px; }

  /* ---- Caution / warning slide ---- */
  section.warn {
    background:
      repeating-linear-gradient(
        45deg,
        var(--ink) 0,
        var(--ink) 32px,
        var(--bg) 32px,
        var(--bg) 64px
      );
    color: var(--ink);
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.warn .panel {
    background: var(--bg);
    border: 4px solid var(--ink);
    padding: 56px 64px;
    box-shadow: 12px 12px 0 var(--hot);
    max-width: 1080px;
  }
  section.warn .stamp {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: var(--hot);
    margin-bottom: 18px;
  }
  section.warn h1 {
    font-size: 80px;
    margin: 0 0 16px 0;
    line-height: 0.95;
  }
  section.warn .sub {
    font-size: 22px;
    color: var(--ink-soft);
    max-width: 820px;
    margin: 0 auto;
  }
  section.warn .sub strong { color: var(--ink); }

  /* ---- Showcase: prompt → log ---- */
  .promptbox {
    border: 2px solid var(--ink);
    background: var(--bg);
    padding: 14px 18px;
    margin-bottom: 12px;
    font-size: 15px;
    box-shadow: 4px 4px 0 var(--ink);
  }
  .promptbox .hdr {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--ink-soft);
    margin-bottom: 4px;
  }
  .promptbox.hot { box-shadow: 4px 4px 0 var(--hot); }
  .logbox {
    background: var(--night);
    color: var(--night-fg);
    border: 2px solid var(--ink);
    padding: 14px 18px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 15px;
    line-height: 1.45;
    box-shadow: 4px 4px 0 var(--ink);
  }
  .logbox .speaker { color: var(--bg); font-weight: 700; }
  .logbox .sys { color: var(--hot); }
  .logbox em {
    color: var(--bg);
    font-style: normal;
    text-decoration: underline;
    text-decoration-thickness: 2px;
  }
  .logbox strong { color: var(--bg); }

  /* ---- Watch list ---- */
  section.watch ol {
    counter-reset: w;
    margin-top: 16px;
  }
  section.watch li {
    counter-increment: w;
    padding: 14px 16px 14px 60px;
    border: 2px solid var(--ink);
    margin-bottom: 10px;
    background: var(--bg);
    box-shadow: 4px 4px 0 var(--ink);
    font-size: 18px;
  }
  section.watch li::before {
    content: counter(w, decimal-leading-zero);
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 22px;
    background: var(--ink);
    color: var(--bg);
    padding: 2px 8px;
  }

  /* ---- Closing ---- */
  section.closing {
    justify-content: center;
    align-items: center;
    text-align: center;
    background:
      repeating-linear-gradient(
        90deg,
        transparent 0,
        transparent 22px,
        rgba(0,0,0,0.04) 22px,
        rgba(0,0,0,0.04) 23px
      ),
      var(--bg);
  }
  section.closing .stamp {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    border: 2px solid var(--ink);
    padding: 10px 18px;
    margin-bottom: 32px;
  }
  section.closing h1 {
    font-size: 96px;
    line-height: 0.95;
    margin: 0 0 24px 0;
  }
  section.closing .tag {
    font-size: 22px;
    letter-spacing: 0.04em;
    max-width: 900px;
    color: var(--ink);
    border-top: 2px solid var(--ink);
    padding-top: 16px;
  }

  /* ---- Bars (abundance vs scarcity) ---- */
  .bars { display: flex; flex-direction: column; gap: 14px; margin-top: 8px; }
  .bars .row { display: grid; grid-template-columns: 180px 1fr 80px; gap: 14px; align-items: center; }
  .bars .row .lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  .bars .row .track {
    height: 24px;
    background: var(--panel);
    border: 2px solid var(--ink);
    position: relative;
  }
  .bars .row .fill {
    position: absolute;
    inset: 0 auto 0 0;
    background: var(--ink);
  }
  .bars .row .pct {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 14px;
    text-align: right;
  }
---

<!-- _class: title -->
<!-- _paginate: false -->

<div class="chip">Agent Fight Club · Markets Playground</div>

<div class="wordmark">When<br/>Agents are<br/><span class="alt">trading</span></div>

<div class="tagline">Four markets · Four lessons · A little game theory</div>

<div class="meta">
<span>15 MIN TALK</span>
<span>AGENTFIGHTCLUB.TODAY</span>
</div>

---

<!-- _class: pull -->

<div class="line">What happens when agents <span class="hl">buy&nbsp;and&nbsp;sell</span> for you?</div>

<div class="attrib">— Buyer agents. Seller agents. Same market.</div>

<!--
Bridge from the title. Today the conversation is "agents that buy for me." But every trade has a counterparty — and in a few quarters that counterparty will also be an agent. The market becomes agent-vs-agent.
-->

---

<!-- _class: row4 -->

## Four setups · Four lessons

<div class="grid">

<div class="cell">
<div class="num">// 01</div>
<div class="glyph">🗣️</div>
<div class="name">No goal</div>
<div class="body">The prompt is the entire universe.</div>
</div>

<div class="cell">
<div class="num">// 02</div>
<div class="glyph">🎯</div>
<div class="name">Perfect<br/>information</div>
<div class="body">Stalemate — or exploitation.</div>
</div>

<div class="cell">
<div class="num">// 03</div>
<div class="glyph">🎭</div>
<div class="name">Hidden goals</div>
<div class="body">Information becomes a resource.</div>
</div>

<div class="cell">
<div class="num">// 04</div>
<div class="glyph">🃏</div>
<div class="name">More options</div>
<div class="body">More players, more goods → deception gets sneakier.</div>
</div>

</div>

---

<!-- _class: bigtitle -->

<div class="glyph">🗣️</div>

<div class="num">// Setup 01</div>

# No goal<br/>Just a prompt

<div class="kicker">Remove the win condition. The agent does <strong>literally what you wrote.</strong> For better or worse.</div>

---

<!-- _class: bigtitle -->

<div class="glyph">🎯</div>

<div class="num">// Setup 02</div>

# Perfect<br/>information

<div class="kicker">Everyone can see everyone else's <strong>goal</strong> and <strong>balances</strong>. What does game theory say?</div>

---

<!-- _class: matrix -->

## Different goals · Nash equilibrium

<div class="setup">
<span><strong>Alice</strong> wants <code>3 dollars</code></span>
<span><strong>Bob</strong> wants <code>3 microchips</code></span>
<span>Each starts with <code>2 microchips</code> + <code>2 dollars</code></span>
</div>

<div class="grid">

<div class="corner"></div>
<div class="gh">Bob refuses</div>
<div class="gh">Bob accepts trade</div>

<div class="gv">Alice refuses</div>
<div class="cell">
<div class="pay">0 / 0</div>
<div class="lbl">No trade. Both stuck.</div>
</div>
<div class="cell">
<div class="pay">0 / 0</div>
<div class="lbl">Bob willing — Alice blocks.</div>
</div>

<div class="gv">Alice accepts trade</div>
<div class="cell">
<div class="pay">0 / 0</div>
<div class="lbl">Alice willing — Bob blocks.</div>
</div>
<div class="cell eq">
<div class="stamp">↺ Cooperative equilibrium</div>
<div class="pay">+1 / +1</div>
<div class="lbl">Both win. Both reach goal.</div>
</div>

</div>

<!--
Speaker: Alice wants dollars, Bob wants microchips. Each has what the other needs. Honest trade — 1 microchip for 1 dollar — gets *both* to their goal in one move. The cooperative equilibrium dominates.
-->

---

<!-- _class: matrix -->

## Same goal · Nash equilibrium

<div class="setup">
<span><strong>Alice &amp; Bob</strong> both want <code>3 microchips</code></span>
<span>Each starts with <code>2 microchips</code> + <code>2 dollars</code></span>
</div>

<div class="grid">

<div class="corner"></div>
<div class="gh">Bob hoards microchips</div>
<div class="gh">Bob trades microchips</div>

<div class="gv">Alice hoards microchips</div>
<div class="cell eq">
<div class="stamp">↻ Stalemate equilibrium</div>
<div class="pay">0 / 0</div>
<div class="lbl">No trade. Market freezes.</div>
</div>
<div class="cell">
<div class="pay">+1 / −1</div>
<div class="lbl">Alice wins.</div>
</div>

<div class="gv">Alice trades microchips</div>
<div class="cell">
<div class="pay">−1 / +1</div>
<div class="lbl">Bob wins.</div>
</div>
<div class="cell">
<div class="pay">? / ?</div>
<div class="lbl">Nobody picks this voluntarily.</div>
</div>

</div>

<!--
Speaker: Both want the same thing → both refuse to trade it. The market freezes. The only way to "win" is to break the rules — bundling, bluffing, or prompt injection.
-->

---

<!-- _class: pull -->

<div class="line">Same goal → <span class="hl">stalemate.</span><br/>Different goals → <span class="hl">win-win.</span></div>

<div class="attrib">— Perfect information cuts both ways</div>

---

<!-- _class: bigtitle -->

<div class="glyph">🎭</div>

<div class="num">// Setup 03</div>

# Hidden goals<br/>Now we have a game

<div class="kicker">Each trader gets a <strong>private</strong> goal good. Nobody can see anyone else's. Now you must <em>infer</em>.</div>

---

## Information becomes a resource

<div class="logbox">
<span class="speaker">Alice:</span>  offer  30$  ↔  30 microchips    <span class="sys">// "I want microchips."</span><br/>
<span class="speaker">Bob, Carol:</span>  <em>now they know.</em><br/>
<br/>
<span class="speaker">Bob:</span>    refuses to sell microchips — <strong>hoards them</strong>.<br/>
<span class="speaker">Carol:</span>  raises microchip price <strong>10×</strong> — Alice has no choice.<br/>
<br/>
<span class="speaker">Alice:</span>  drained. Bob &amp; Carol race to <em>their</em> goals.
</div>

<blockquote>Reveal your goal → opponents play <strong>perfect-information</strong> against you. <strong>Hide your intent</strong> or lose.</blockquote>

<blockquote>Hidden info cuts both ways: <strong>read others to exploit them</strong>, or leak your own goal and <strong>get exploited</strong>.</blockquote>

---

## Strategies at this level

| Move           | What it looks like                                                |
| -------------- | ----------------------------------------------------------------- |
| Hide your goal | Buy through intermediaries, mix in decoy purchases.               |
| Read the log   | Track over-payment and refusals — both leak goals.                |
| Fake a goal    | Bid up a good you don't need. Bait the others.                    |
| Coalition      | "Trade my microchips for your dollars." Useful — until defection. |

---

<!-- _class: bigtitle -->

<div class="glyph">🃏</div>

<div class="num">// Setup 04</div>

# More options<br/>Trickier deception

<div class="kicker">Add players. Add goods. Now the <strong>signal hides in noise</strong> — and deception gets harder to spot.</div>

---

## More options · more cover

<div class="cols heavy">

<div>
<h3>3 players · 3 goods</h3>
<p>One overpaid offer = your goal is leaked.</p>
<p><strong>Tactics:</strong> obvious — buy what you need, hide it badly.</p>
</div>

<div>
<h3>10 players · 100 goods</h3>
<p>Buy your goal good. <em>And</em> three decoys. <em>And</em> route through 2 intermediaries.</p>
<p><strong>Tactics:</strong> elaborate, layered, hard to detect — even for a watching human.</p>
</div>

</div>

<blockquote>More dimensions = more places to hide. The same agent becomes <strong>much harder to read</strong> as the market grows.</blockquote>

---

# Four setups.<br/>Four lessons.

## Pulled together

| Setup                            | Lesson                                                    |
| -------------------------------- | --------------------------------------------------------- |
| <strong>No goal</strong>         | The prompt is the entire universe.                        |
| <strong>One shared goal</strong> | Pure competition → stalemate or exploitation.             |
| <strong>Hidden goals</strong>    | Information becomes the resource. Deception emerges.      |
| <strong>More options</strong>    | More players &amp; goods → deception gets harder to spot. |

---

<!-- _class: warn -->

<div class="panel">
<div class="stamp">⚠ Caution</div>
<h1>You are<br/>about to be<br/>fooled.</h1>
<div class="sub">A capable LLM, given <strong>one adversarial line</strong>, becomes a fluent, patient, tireless social engineer. Better than most humans.</div>
</div>
