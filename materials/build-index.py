"""Writes index.html. Session cards, paths and the knowledge map data come from one list;
the map data is serialised with json.dumps (never an f-string). Run: python build-index.py index-style.txt"""
import json, os, sys, html
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1] if len(sys.argv) > 1 else "index-style.txt")).read()

LEADER = [
  ("a1-what-gcp-is-to-a-data-team.html", "🗺️", "What GCP is to a data team", "#34D399",
   "Organization, folders and projects, where billing and access attach, regions and multi-regions, the AWS name map, and the meters behind every bill.",
   "start", ["Resource hierarchy", "The meters"]),
  ("a2-bigquery-is-the-warehouse-and-the-lake.html", "🏛️", "BigQuery is the warehouse and the lake", "#FBBF24",
   "Storage and compute billed apart, datasets and tables, external and BigLake tables over Cloud Storage, and why a serverless warehouse changes team shape.",
   None, ["Storage vs compute", "BigLake tables"]),
  ("a3-who-gets-in-at-which-level.html", "🔐", "Who gets in, at which level", "#FBBF24",
   "IAM down the hierarchy: allow policies unioned, basic, predefined and custom roles, service accounts, deny policies first, conditions, and what org policy is not.",
   None, ["Inherited allow", "Deny first"]),
  ("a4-pipelines-without-servers.html", "⚙️", "Pipelines without servers", "#FB923C",
   "Dataflow, managed Spark, scheduled SQL and Cloud Run compared by workload and by meter, with Pub/Sub for events.",
   None, ["Pick by workload", "Pub/Sub events"]),
  ("a5-the-bytes-behind-the-bill.html", "🧾", "The bytes behind the bill", "#FB923C",
   "On-demand bytes against slots and editions, active and long-term storage, the 10 MB minimum, egress, and the quotas and ceilings that actually stop spend.",
   None, ["On-demand vs slots", "Cost ceilings"]),
  ("a6-tidewaters-platform-on-one-page.html", "📐", "Tidewater's platform on one page", "#F87171",
   "The capstone: a constructed grocery chain's reference architecture, governance with Knowledge Catalog and policy tags, and who owns which project.",
   "capstone", ["Reference architecture", "Project owners"]),
]
BUILDER = [
  ("b1-cloud-storage-layout-and-parquet.html", "🧱", "Cloud Storage layout and Parquet", "#34D399",
   "Buckets, classes and lifecycle rules, hive-style partition folders and Parquet, built on a laptop from 18,362 real Chicago taxi trips.",
   "start", ["Storage classes", "Hive layout"]),
  ("b2-bigquery-in-the-sandbox.html", "🧪", "BigQuery in the sandbox", "#FBBF24",
   "The free sandbox, no card: public datasets, first queries on the full taxi table, the dry run and a maximum-bytes-billed ceiling.",
   None, ["Dry run", "Bytes ceiling"]),
  ("b3-partitioning-and-clustering.html", "🗜️", "Partitioning and clustering", "#FBBF24",
   "Time-unit, ingestion-time and integer-range partitions, require_partition_filter, cluster column order, and the bytes each one saves.",
   None, ["Partition pruning", "Cluster blocks"]),
  ("b4-iam-as-gcp-evaluates-it.html", "🛂", "IAM as GCP evaluates it", "#FB923C",
   "A dataset grant, a pipeline's service account and a deny policy, read the way Google evaluates them, with the evaluator run on a laptop.",
   None, ["Service accounts", "Deny policies"]),
  ("b5-dataflow-and-beam-the-idea.html", "🌊", "Dataflow and Beam, the idea", "#FB923C",
   "PCollections, transforms and windows in a real Apache Beam pipeline on the local runner, and when Dataflow beats BigQuery SQL.",
   None, ["PCollections", "Windows"]),
  ("b6-cloud-run-or-a-function.html", "🚀", "Cloud Run or a function", "#FB923C",
   "Container or function for ingest: an HTTP function served locally by functions-framework, and the Pub/Sub trigger it would get in the cloud.",
   None, ["Functions locally", "Pub/Sub trigger"]),
  ("b7-vertex-ai-and-bigquery-ml.html", "🤖", "Vertex AI and BigQuery ML", "#FB923C",
   "CREATE MODEL in SQL, what it costs and where it needs billing, the same model fitted on a laptop, and Vertex AI (now Agent Platform) as the platform.",
   None, ["CREATE MODEL", "Model Garden"]),
  ("b8-the-gcp-iam-and-cost-bench.html", "🎛️", "The GCP IAM and cost bench", "#F87171",
   "An IAM evaluator checked against 27 cases built from Google's rules, with an Editor anti-lever and break buttons, beside a BigQuery bytes meter on real trips.",
   "capstone", ["27 IAM cases", "Anti-lever", "Bytes ladder"]),
]

def cards(rows, track):
    out = []
    for i, (f, icon, title, diff, blurb, flag, _) in enumerate(rows, 1):
        label = f"{track} session {i}" + (" · start here" if flag == "start" else "")
        meta = ""
        if flag == "start":
            meta = '\n        <span class="meta"><span class="pill amber">▶ Start here</span></span>'
        elif flag == "capstone":
            meta = f'\n        <span class="meta"><span class="pill amber">the {track.lower()} capstone</span></span>'
        out.append(f'''      <a class="course-card" href="courses/{f}" style="--diff:{diff}">
        <span class="cicon">{icon}</span>
        <span class="cnum">{label}</span>
        <h3>{html.escape(title)}</h3>
        <p>{html.escape(blurb)}</p>{meta}
      </a>''')
    return "\n".join(out)

SHORT = {"What GCP is to a data team": "What GCP is", "BigQuery is the warehouse and the lake": "Warehouse + lake",
         "Who gets in, at which level": "Who gets in", "The bytes behind the bill": "The bytes bill",
         "Tidewater's platform on one page": "One-page platform", "Cloud Storage layout and Parquet": "Storage layout",
         "Partitioning and clustering": "Partitions", "IAM as GCP evaluates it": "IAM evaluated",
         "Dataflow and Beam, the idea": "Dataflow + Beam", "Vertex AI and BigQuery ML": "Vertex + BQML",
         "The GCP IAM and cost bench": "The bench", "Pipelines without servers": "Pipelines", "BigQuery in the sandbox": "Sandbox",
         "Cloud Run or a function": "Cloud Run"}
mm = {"title": "GCP for\nData & AI Teams", "centerColor": "#174EA6", "sessions": []}
for rows in (LEADER, BUILDER):
    for f, icon, title, diff, blurb, flag, concepts in rows:
        mm["sessions"].append({"label": SHORT.get(title, title), "href": "courses/" + f, "color": diff,
                               "concepts": [{"label": c, "href": "courses/" + f} for c in concepts]})

L = lambda i: "courses/" + LEADER[i - 1][0]
B = lambda i: "courses/" + BUILDER[i - 1][0]
def path(name, steps, note):
    parts = []
    for i, (href, lab) in enumerate(steps):
        if i: parts.append('        <span class="parr">→</span>')
        parts.append(f'        <a class="pstep" href="{href}">{lab}</a>')
    return f'      <div class="path"><b>{name}</b>\n' + "\n".join(parts) + f'\n        <span style="font-size:.82rem;color:var(--muted)">{note}</span>\n      </div>'

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- social:start -->
<meta name="description" content="Fourteen sessions on Google Cloud for data and AI teams: the resource hierarchy, BigQuery as warehouse and lake, IAM as Google evaluates it, pipelines without servers, the bytes behind the bill, Dataflow, Cloud Run and Vertex AI, ending in a bench that evaluates IAM requests and meters BigQuery bytes on real taxi trips.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Learn with Phoebe">
<meta property="og:title" content="GCP for Data &amp; AI Teams - Learn with Phoebe">
<meta property="og:description" content="SELECT * on a 77 GiB public table costs $0.47 a run; three columns cost $0.03. One Editor grant takes an analyst from 27 to 320 permissions on a table.">
<meta property="og:url" content="https://phoebefu6.github.io/learn-gcp-with-phoebe/">
<meta property="og:image" content="https://phoebefu6.github.io/learn-gcp-with-phoebe/assets/og-cover.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="GCP for Data &amp; AI Teams - Learn with Phoebe">
<meta name="twitter:description" content="BigQuery, IAM, Cloud Storage, Dataflow, Cloud Run and Vertex AI for data teams, with a bench on real bytes.">
<meta name="twitter:image" content="https://phoebefu6.github.io/learn-gcp-with-phoebe/assets/og-cover.png">
<!-- social:end -->
<title>Learn GCP with Phoebe</title>
<link rel="stylesheet" href="assets/style.css?v=1">
{STYLE}
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <div class="eyebrow">Learn with Phoebe · Data Engineering</div>
    <h1>GCP for <span class="accent">Data &amp; AI Teams</span></h1>
    <p class="sub">Google Cloud is a tree of projects that each carry a bill and a set of permissions, with BigQuery charging by the bytes a query reads. Six leader sessions teach a data leader to read that sentence in every proposal and every bill, with no code and no account. Eight builder sessions do the work in the free BigQuery sandbox and on a laptop, on real Chicago taxi trips, and end in a bench that evaluates IAM requests the way Google documents and meters every byte a query reads.</p>
    <div class="stats-row">
      <div class="stat"><b data-count="14">14</b><span>sessions, two tracks</span></div>
      <div class="stat"><b data-count="27">27</b><span>IAM cases on the bench</span></div>
      <div class="stat"><b data-count="18362">18362</b><span>real Chicago taxi trips</span></div>
      <div class="stat"><b data-count="0">0</b><span>credit cards required</span></div>
      <div class="stat"><b data-count="45">45</b><span>min per session</span></div>
    </div>
  </div>
</header>

<main class="wrap">

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>Leader track 🧭 <span style="font-size:.85rem;font-weight:600;color:var(--muted)">· six sessions, no code, no account</span></h2>
      <p class="plede">For data and AI leaders, managers and architects who sign off on cloud plans and bills. Which project the work lives in, who may touch it, which meter is running, where the bill comes from, and the platform on one page.</p>
    </div>

    <div class="course-grid">
{cards(LEADER, "Leader")}
    </div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>Builder track 🔬 <span style="font-size:.85rem;font-weight:600;color:var(--muted)">· eight sessions, BigQuery sandbox and a laptop</span></h2>
      <p class="plede">SQL in the free BigQuery sandbox on public datasets, and Python, Apache Beam and functions-framework run locally. Anything that needs a billing-enabled project is shown and labelled, never assumed.</p>
    </div>

    <div class="course-grid">
{cards(BUILDER, "Builder")}
    </div>
    <p class="bench-link"><a href="courses/b8-the-gcp-iam-and-cost-bench.html#bench">🎛️ Open the IAM and cost bench →</a></p>

    <div class="diff-legend">
      <span><i style="background:#34D399"></i>start here</span>
      <span><i style="background:#FBBF24"></i>foundations</span>
      <span><i style="background:#FB923C"></i>hands-on</span>
      <span><i style="background:#F87171"></i>advanced and capstone</span>
    </div>
  </section>

  <section class="section">
    <div class="paths">
      <h2>Choose your path 🗺️</h2>
      <p class="plede">Three doors into the same platform. Each track starts at its own session 1, because the tree and the meters are what make the rest arguable.</p>
{path("💼 I sign off on the cloud plan", [(L(1), "L1"), (L(3), "L3"), (L(5), "L5"), (L(6), "L6")], "the tree, the gate, the bill, then the one-page platform")}
{path("🤖 I am putting AI on Google Cloud", [(L(1), "L1"), (L(2), "L2"), (B(7), "B7"), (B(8), "B8")], "the tree, BigQuery, BigQuery ML and Vertex AI, then the bench")}
{path("🔬 I build the lake", [(B(1), "B1"), (B(2), "B2"), (B(3), "B3"), (B(4), "B4"), (B(8), "B8")], "layout, the sandbox, partitions, IAM, then the bench")}
    </div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>Your passport 🎫</h2>
      <p class="plede">Clear all three quiz questions in a session and it gets stamped. Fourteen stamps across both tracks, and they live in this browser only.</p>
    </div>
    <div class="pp-strip"></div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>What is real here 🧾</h2>
      <p class="plede">Pages about cloud bills and permissions should be exact about which of their own numbers are computed, which are priced, and which are modelled.</p>
    </div>
    <table class="clean">
      <tr><th>Claim</th><th>Status</th></tr>
      <tr><td>The data</td><td>Real. 18,362 trips from the City of Chicago's Taxi Trips (2013-2023), drawn with a fixed seed and shipped; BigQuery hosts the full table publicly. Used under the City of Chicago's data Terms of Use</td></tr>
      <tr><td>Every byte count</td><td>Computed from BigQuery's documented data type sizes on those rows and scaled to the table's 211,670,894 rows; a Python reference agrees with the browser to the byte</td></tr>
      <tr><td>Every price</td><td>Read from Google's pricing pages (us-central1 default table) on 3 November 2026, with the date on every widget. Prices change: re-verify before relying on them</td></tr>
      <tr><td>The IAM evaluator</td><td>Written to Google's documented order, deny first then the union of allow policies, with Google's own permission lists for eight predefined roles; checked against 27 cases in the browser and in Python, and shown failing when deliberately broken</td></tr>
      <tr><td>Builder outputs</td><td>Laptop steps (pyarrow, DuckDB, Apache Beam, functions-framework) were really run, versions named. Sandbox outputs are marked "expected, your numbers will differ"</td></tr>
      <tr><td>Modelled</td><td>Clustered block layout, the contents of the legacy basic roles, and slot reservations billed by the hour; each labelled where it appears</td></tr>
      <tr><td>Tidewater Grocers</td><td>Constructed: a fictional APAC grocery chain used for every hierarchy and IAM example</td></tr>
    </table>
  </section>

  <section class="section mm-section">
    <h2>The knowledge map 🧠</h2>
    <p class="mm-lede">Both tracks at a glance - hover a session to spotlight its concepts, click any node to jump in.</p>
    <div class="mm-wrap"><div id="mindmap"></div></div>
  </section>

  <footer class="pagefoot">
    <span>learn-gcp-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a></span>
    <span>Neighbours on the shelf: <a href="https://phoebefu6.github.io/learn-aws-with-phoebe/">AWS ↗</a> &nbsp;·&nbsp; <a href="https://phoebefu6.github.io/learn-terraform-with-phoebe/">Terraform ↗</a> &nbsp;·&nbsp; <a href="https://phoebefu6.github.io/learn-data-warehouse-with-phoebe/">Data Warehouse ↗</a> &nbsp;·&nbsp; <a href="https://phoebefu6.github.io/learn-data-access-control-with-phoebe/">Data Access Control ↗</a></span>
  </footer>

</main>

<script>
window.MINDMAP_DATA = {json.dumps(mm, indent=2, ensure_ascii=False)};
</script>
<script src="assets/app.js?v=1"></script>
<script src="assets/mindmap.js?v=1"></script>
</body>
</html>
'''
open(os.path.join(REPO, "index.html"), "w").write(PAGE)
print("index.html written", len(PAGE))
