# Agent brief - shared by every fan-out page of learn-gcp-with-phoebe

You are writing static HTML session pages. No servers, no npm. **If your target file already
exists on disk, do not write it; report that and move to your next file.** Write each file, return
its path and one line of coverage. No HTML in your reply.

## Read first, in this order

1. The template page for YOUR track. Copy its structure, classes, SVG grammar and quiz markup
   EXACTLY, including how many options each question has (4):
   - Leader track (a1-a6, no code): `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/courses/a1-what-gcp-is-to-a-data-team.html`
   - Builder track (b1-b8, sandbox + laptop): `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/courses/b1-cloud-storage-layout-and-parquet.html` (the bench page `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/courses/b8-the-gcp-iam-and-cost-bench.html` holds the canon numbers in context)
2. The source map: every verified number, its evidence tier, per-session coverage, the seams. Use
   ONLY its numbers; never invent a statistic; if a fact is missing, teach the uncertainty.
   `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/materials/official-course-map.md`
   Deeper quotes with URLs: `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/materials/sources-gcp-docs.md`
3. Builder pages only: your build-along script(s) and REAL output, which you paste verbatim:
   `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/materials/buildalong/<script>` and
   `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/materials/buildalong/outputs/<script>.txt`.
   Show the code in 2-4 step boxes (split the script; keep it runnable when concatenated), then the
   output box labelled "(real output)". Never edit an output line; you may omit log lines (Beam's
   WARNING/INFO lines) if you say "log lines omitted". Timings vary by machine.
4. The stylesheet `:root` block for the palette tokens: `/Users/phoebe.fu/Documents/Claude_Work/github_repo/learn-gcp-with-phoebe/assets/style.css`

## Page skeleton (keep every component)

toolbar (crumb EXACTLY `<a href="../index.html">learn-gcp-with-phoebe</a> / Leader session N of 6`
or `/ Builder session N of 8`, #toggle-all, #zoom-toggle) · masthead (eyebrow "Learn GCP with Phoebe ·
Leader track · Session N of 6" or "... · Builder track · Session N of 8", h1 with one
`<span class="accent">`, .sub, .chip-row with the level chip 🟢 Foundations (sessions 1-2) / 🟡 Core
(3-4) / 🟠 Applied (5-7) / 🔴 Capstone (leader 6), two audience chips as in the template, time chip
"45 min", .agenda a1-a4) · main.wrap · section#intro (Part 0: kicker, .lede, .legend pills,
.callout.win "★ What you walk out with tonight.") · 3 Parts, each `section.section#part-N` with
section-kicker (klabel "Part N · covers ...", h2, `.tag.concept "N min live"`), a `.lede`, ONE
figure, `details.card` accordions (summary: `.mode.live` or `.mode.self`, title, `.mini`, `.caret ▶`),
at least one `.callout.example` with `span.ex-pill` "Real world" on the page · section#demo-1
Build-along (kicker `.tag.demo "★ 22 min · everyone builds"`, .lede, ONE figure, `.steps > .step`,
each with a `.prompt-box.good` carrying a `span.label`; leader pages: a paper exercise on Tidewater
with worked example boxes; builder pages: setup box pointing back to builder session 1's environment
(`pip install` with the pinned versions named in your outline), the split script, the real output,
and where something needs billing, a `.callout.tip` "On a billing-enabled project (optional)." whose
next sentence is EXACTLY "Shown, needs a billing-enabled project: the BigQuery sandbox covers
BigQuery only, and the $300 Free Trial asks for a card." (b2, b3, b7 use instead: "Runs in the
BigQuery sandbox: no card, no billing account." for sandbox SQL boxes, and label every sandbox output
"expected, your numbers will differ")) · section#exercise Homework (ol, 4 items) · section#quiz (3 x
`.quiz-q data-answer="0-based"`, `p.qtext`, 4 x `button.qopt` "A · ...", `p.qwhy`; one
`p.quiz-score` after the last; vary the correct letter) · section#official, h2 EXACTLY "What this
session teaches, and where it came from", `.covered > .covered-row` (pill solid ✓ / light ◐ + name +
note), then the `.mono` line EXACTLY "Every fact on this page, and its verification tier, is
recorded in the course's source map." · section.cheat#cheatsheet (h3 "Leader session N cheat sheet
<span>· pin this</span>" or "Builder session N cheat sheet ...", .grid-2 of six .cheat-item) ·
`.callout.next` with `.nx-pill` "Next session" · footer.pagefoot ·
`<script src="../assets/app.js?v=1"></script>`.

Head: the template's social meta block with this page's own title/description/url;
`<title>Leader session N · Title - learn gcp with phoebe</title>` (or Builder);
`<link rel="stylesheet" href="../assets/style.css?v=1">`. Nothing else external.

First `details.card` in the FIRST Part is `open`; no other. Sentence case headings. Warm
practitioner voice, concrete, never dry. Inside prompt-boxes escape `&` `<` `>`. 450 to 650 lines
is guidance about depth, never a target: never collapse whitespace, dissolve a list into a
paragraph, or drop a component to fit.

## Hard rules (a violation is rework)

- NEVER an em dash or en dash, anywhere (prose, code, aria-labels, comments). Hyphen only.
- No meta text: never "this course", "in this course", "the course teaches", "banned here". Say
  "these pages" or name the session. State the professional norm directly with its reason. The two
  exact estate phrases above are the only self-references.
- Attribution "by Phoebe Fu". Never "built with" a tool.
- Every number comes from the map (sections 3 and 4) or is labelled constructed or modelled. For
  sandbox examples print "expected, your numbers will differ"; never invent outputs as if run.
- Prices: say "us-central1, BigQuery pricing page, 3 November 2026" (or the product's pricing page)
  near a dollar figure, and that prices must be re-verified. Never quote a price not in the map.
- Things the map marks `R` or NOT FOUND (e.g. "no way to remove an inherited permission", scheduled
  query 5-minute minimum, BigQuery ML in the sandbox, US multi-region slot prices) must NOT be stated
  as Google's words. Teach them as derived or unknown and say so.
- Renames: first use on a page writes the current name with the old in brackets or vice versa:
  "Vertex AI (now Gemini Enterprise Agent Platform)", "Knowledge Catalog (formerly Dataplex)",
  "Managed Service for Apache Spark (formerly Dataproc)", "Cloud Run functions (formerly Cloud
  Functions)", Composer "evolving to become Managed Service for Apache Airflow".
- Contested or missing evidence: teach the disagreement; never resolve what the sources have not.
- Citations in the exact form of the map's appendix; anything marked `R` is "reported".
- NEVER "lottery" or "lotteries". NEVER the bullet "✗" in prose lists (only the existing
  `prompt-box bad` label pattern from the template is allowed).
- Default to the English word. No Chinese terms.
- Seams: link, never teach (map section 1). RBAC/ABAC and row/column security concepts belong to
  learn-data-access-control; warehouse modelling to learn-data-warehouse; lakehouse to
  learn-databricks; pipeline design to learn-data-engineering / learn-data-pipelines /
  learn-data-orchestration; streaming to learn-streaming-data; infrastructure as code to
  learn-terraform (link its session 4 for `google_storage_bucket`); Claude on Vertex to learn-claude
  session 68; AWS services to learn-aws.
- Titles, widget ids and class names must not collide with siblings: do not reuse "Who can touch
  what", "The bill you did not plan", "A data platform on one page", "The IAM and cost bench", "The
  policy bench", "Who can see what", "Cost and performance"; no new CSS classes (use only classes
  that exist in the template pages and style.css); no element ids beyond the section ids.
- Tidewater Grocers is constructed: say "constructed" on every page that uses it. Its hierarchy is
  fixed (map section 0): organization tidewater.example > folders data-platform, analytics, sandbox >
  projects tw-lake-prod (data-platform), tw-bi-prod (analytics), tw-lake-dev (sandbox) > datasets
  sales_raw, sales_curated, loyalty_pii; bucket tw-lake-prod-landing; people mei (analysts), raj
  (data-eng), ana (contractors), zoe (privacy-officers), sam (security), lin (loyalty lead), service
  account ingest-pipeline@tw-lake-prod.iam.gserviceaccount.com.

## Figure grammar (hand-drawn, every figure)

Palette, ONLY these hexes (no invented greys): ink #202124 · muted #5F6368 · accent #1A73E8 ·
deep #174EA6 · mid #4285F4 · soft #AECBFA · tint #E8F0FE · faint #DADCE0 · hairline #E8EAED ·
yellow #FBBC04 (fill only) · yellow ink #6B4A00 · yellow tint #FEF7E0 · `#FFFFFF` · universal reds
`#991B1B` `#FEF2F2` `#FCA5A5` only for a wrong-way panel. Text on a yellow fill is #202124, never
white; text on #174EA6 fills is #FFFFFF; NEVER #1A73E8 text on #E8F0FE (3.9:1): blue text is #174EA6.

- `<figure class="zoomable">` > `<svg viewBox="0 0 880 H" xmlns="http://www.w3.org/2000/svg" role="img"
  aria-label="the data, not the shape">` > `<defs>` + `<style>` + content, then
  `<figcaption>🔍 Click to zoom - takeaway</figcaption>`. Grow H, never W.
- Prefix unique per figure, used for every class and id: `<page><letter>` e.g. `a2a`, `a2b`, `b5c`
  (a, b, c for Parts 1-3, d for the build-along).
- `<defs>` holds with prefix P: a wobble filter `id="PSk"` (`feTurbulence type="fractalNoise"
  baseFrequency="0.02" numOctaves="2" seed="<int>"` + `feDisplacementMap scale="2.4"
  xChannelSelector="R" yChannelSelector="G"`, `x="-3%" y="-3%" width="106%" height="106%"`), a hachure
  pattern `id="PHc"` (7x7 userSpaceOnUse, rotate(-38), one #1A73E8 line, opacity .5), an open
  arrowhead `id="PAr"` (path `M1 1 L9 5 L1 9`, fill none, ink stroke 1.6). ALL shapes sit inside ONE
  `<g filter="url(#PSk)" fill="none" stroke="#202124" stroke-width="2" stroke-linecap="round"
  stroke-linejoin="round">`; rects carry a tiny rotation (-4 to 4 degrees for hand-placed items,
  under 1 for panels). Fills: white, tint, the hachure for "the pile" or "the data", and yellow ONLY
  for the one thing the figure is about. Text classes: `.PH` 800 12px ink heading · `.PL` 600 12px
  ink label · `.PS` 400 11px muted · `.PB` 800 11px yellow-ink #6B4A00 (on white or tint only) ·
  `.PV` 800 16-20px deep value · `.PW` 800 12px white on a deep fill · `.PA` 700 11px deep axis
  caption · `.PN` 400 12px muted note. Do not override a class's fill with an inline style.
- ALL `<text>` outside the filtered group, sans stack, never below 10.5px.
- Lines and arrows must not pass through text (the gate flags "line-through-text"): route arrows
  around labels or stop them at box edges. Painted rects must not overlap each other unless one fully
  contains the other (a highlight inside a panel is fine; two siblings overlapping is a defect).
- Fit: max chars ≈ (box width - 20) / 7 at 12px, 6.4px/char at 11px; full-width note under 110
  chars; 40px between neighbouring point labels; bottom note 22px below the last row, H clears it by
  8px. Text must stay inside the box it labels. When in doubt, shorten.
- Floor: one figure per Part plus one in the build-along. Draw the MECHANISM (a policy flowing down
  a tree, a query reading three columns of 23, a partition being pruned, a window grouping events, a
  request waking a function), never a metaphor literally, never decoration.

## Voice and honesty

Every Part gets a real-world story. Composites say "constructed" in the callout or the coverage row.
Google facts are quoted from the map with their page names. Short quotes only (under 30 words each).

## Cross-links (absolute URLs)

- learn-aws: https://phoebefu6.github.io/learn-aws-with-phoebe/
- learn-terraform session 4: https://phoebefu6.github.io/learn-terraform-with-phoebe/courses/04-modules-and-versions.html
- learn-data-warehouse: https://phoebefu6.github.io/learn-data-warehouse-with-phoebe/
- learn-databricks: https://phoebefu6.github.io/learn-databricks-with-phoebe/
- learn-data-access-control: https://phoebefu6.github.io/learn-data-access-control-with-phoebe/
- learn-data-engineering: https://phoebefu6.github.io/learn-data-engineering-with-phoebe/
- learn-data-pipelines: https://phoebefu6.github.io/learn-data-pipelines-with-phoebe/
- learn-data-orchestration: https://phoebefu6.github.io/learn-data-orchestration-with-phoebe/
- learn-streaming-data: https://phoebefu6.github.io/learn-streaming-data-with-phoebe/
- learn-claude session 68: https://phoebefu6.github.io/learn-claude-with-phoebe/courses/68-bedrock-vertex.html
- Hub: https://phoebefu6.github.io/learn-with-phoebe/

## Footer chain(s) and session titles

Footer left: "Leader session N of 6 · learn-gcp-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a>" (Builder: "Builder session N of 8 · ...").
Footer right: "<a href="prev.html">← Prev: Title</a> &nbsp;·&nbsp; <a href="next.html">Next: Title →</a>"; leader 6 ends "← Prev ... &nbsp;·&nbsp; <a href="../index.html">Course home</a>".

Leader chain: a1-what-gcp-is-to-a-data-team.html "What GCP is to a data team" →
a2-bigquery-is-the-warehouse-and-the-lake.html "BigQuery is the warehouse and the lake" →
a3-who-gets-in-at-which-level.html "Who gets in, at which level" → a4-pipelines-without-servers.html
"Pipelines without servers" → a5-the-bytes-behind-the-bill.html "The bytes behind the bill" →
a6-tidewaters-platform-on-one-page.html "Tidewater's platform on one page".
Builder chain: b1-cloud-storage-layout-and-parquet.html "Cloud Storage layout and Parquet" →
b2-bigquery-in-the-sandbox.html "BigQuery in the sandbox" → b3-partitioning-and-clustering.html
"Partitioning and clustering" → b4-iam-as-gcp-evaluates-it.html "IAM as GCP evaluates it" →
b5-dataflow-and-beam-the-idea.html "Dataflow and Beam, the idea" → b6-cloud-run-or-a-function.html
"Cloud Run or a function" → b7-vertex-ai-and-bigquery-ml.html "Vertex AI and BigQuery ML" →
b8-the-gcp-iam-and-cost-bench.html "The GCP IAM and cost bench".

## Before you report

For each page: grep it for "—", "–", "this course", "lottery"; count `<details` vs `</details>`,
`<section` vs `</section>`, `<figure` vs `</figure>`, `<svg` vs `</svg>`, `<text` vs `</text>`; and
check no `#1A73E8` appears as a text `fill` in your figure `<style>`. Fix before reporting.
