/* learn-gcp-with-phoebe - the IAM and cost bench (builder session 8)
   Needs: gcp-iam.js (GcpIam), gcp-iam-data.js (GCP_IAM_DATA), gcp-cost.js (GcpCost), gcp-sample.js (GCP_SAMPLE).
   Every verdict is computed by the evaluator in this page; every byte count comes from the real
   sample and BigQuery's documented data type sizes. Page API for verification:
   GCP_BENCH.setCase(n) (1-based case number), GCP_BENCH.setRung(id) (star | named | part | clus). */
(function () {
  "use strict";
  var I = window.GcpIam, D = window.GCP_IAM_DATA, C = window.GcpCost, S = window.GCP_SAMPLE;
  if (!I || !D || !C || !S) return;
  var E = I.make(D), F = D.fixture;
  var API = window.GCP_BENCH = { state: {} };

  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    for (var k in (attrs || {})) e.setAttribute(k, attrs[k]);
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function fmt(n, d) { return Number(n).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d }); }
  function who(p) { return p.split(":")[1]; }
  var WORD = { "allow": "Allowed", "deny": "Denied by a deny policy", "not-granted": "Not granted (no binding allows it)",
               "refused": "Binding refused", "accepted": "Binding accepted" };
  var RAIL = "Evaluation follows Google's documented IAM rules for these roles; real IAM has more roles, conditions and org policies. " +
             "Bytes follow BigQuery's documented sizes; clustering savings are modelled.";

  /* ---------------- IAM panel ---------------- */
  var iamRoot = document.getElementById("gcp-iam-bench");
  if (iamRoot) {
    var st = { anti: false, mode: "correct" };
    API.state.iam = st;
    var reqCases = F.cases.filter(function (c) { return c.kind !== "binding"; });
    var people = [], perms = [];
    F.cases.forEach(function (c) {
      if (!c.request) return;
      if (people.indexOf(c.request.principal) < 0) people.push(c.request.principal);
      if (perms.indexOf(c.request.permission) < 0) perms.push(c.request.permission);
    });
    perms.sort();
    iamRoot.innerHTML =
      '<div class="gcp-panel">' +
      '<div class="gcp-scope"><b>Scope, stated:</b> the constructed Tidewater hierarchy (organization, three folders, three projects, ' +
      'datasets, a bucket), allow policies with IAM Conditions, and deny policies with tag-based denial conditions. ' +
      'Role permission lists are Google\'s, for 8 predefined roles (retrieved ' + F.now.slice(0, 10) + '); the legacy basic roles are ' +
      '<b>modelled</b> from their documented definitions. Principal access boundaries, custom roles and org policy constraints are not modelled.</div>' +
      '<h4 class="gcp-h">1 · Ask as someone at Tidewater</h4>' +
      '<div class="gcp-row"><label class="gcp-wide">Case <select id="gcp-case"></select></label></div>' +
      '<div class="gcp-row"><label>Who <select id="gcp-who"></select></label>' +
      '<label>Permission <select id="gcp-perm"></select></label></div>' +
      '<div class="gcp-row"><label class="gcp-wide">On <select id="gcp-res"></select></label></div>' +
      '<div class="gcp-row"><label>Request time <input id="gcp-time" size="22"></label></div>' +
      '<div class="gcp-verdict" id="gcp-verdict"></div><ul class="gcp-trace" id="gcp-trace"></ul>' +
      '<div class="gcp-row"><button class="btn gcp-anti" id="gcp-anti" type="button">Anti-lever: grant roles/editor on tw-lake-prod to mei</button>' +
      '<span class="gcp-count" id="gcp-count"></span></div>' +
      '<details class="gcp-pol"><summary>The policies the evaluator reads (constructed)</summary><pre id="gcp-pol"></pre></details>' +
      '<h4 class="gcp-h">2 · The test table: ' + F.cases.length + ' cases built from Google\'s documented rules</h4>' +
      '<div class="gcp-row"><button class="btn gcp-break" id="gcp-flip" type="button">Break: evaluate allow before deny</button>' +
      '<button class="btn gcp-break" id="gcp-noinh" type="button">Break: ignore inheritance</button>' +
      '<span class="gcp-score" id="gcp-score"></span></div>' +
      '<div class="gcp-tablewrap"><table class="clean gcp-cases" id="gcp-cases"></table></div>' +
      '<p class="gcp-note">' + RAIL + '</p>' +
      '</div>';

    var selCase = document.getElementById("gcp-case"), selWho = document.getElementById("gcp-who"),
        selPerm = document.getElementById("gcp-perm"), selRes = document.getElementById("gcp-res"), inTime = document.getElementById("gcp-time");
    reqCases.forEach(function (c) {
      var q = c.request;
      selCase.appendChild(el("option", { value: c.id }, esc(c.id + " · " + who(q.principal).split("@")[0] + " · " + q.permission + " · " + E.nodes[q.resource].label)));
    });
    people.forEach(function (p) { selWho.appendChild(el("option", { value: p }, esc(who(p)))); });
    perms.forEach(function (p) { selPerm.appendChild(el("option", { value: p }, esc(p))); });
    F.nodes.forEach(function (n) { selRes.appendChild(el("option", { value: n.id }, esc(n.label))); });
    var polText = { allow: F.allow, deny: F.deny, groups: F.groups, tags: F.nodes.filter(function (n) { return n.tags; }).map(function (n) { return [n.label, n.tags]; }) };
    document.getElementById("gcp-pol").textContent = JSON.stringify(polText, null, 1);

    function pol() { return st.anti ? E.withAntilever() : null; }
    function request() { return { principal: selWho.value, permission: selPerm.value, resource: selRes.value, time: inTime.value.trim() || F.now }; }

    function explain(r, q) {
      var out = [];
      if (st.mode === "allow-first") out.push("BROKEN ORDER: allow policies read first.");
      if (r.verdict === "deny") {
        out.push("Step 1, deny policies: rule " + r.rule + " attached at " + r.where + " matched. Allow policies are never read.");
      } else {
        out.push("Step 1, deny policies: none applies" + (st.mode === "no-inherit" ? " (BROKEN: only the resource itself was read)" : " (organization, folder and project checked)") + ".");
        if (r.verdict === "allow") out.push("Step 2, allow policies: " + r.role + " bound at " + r.where + " includes " + q.permission + ".");
        else out.push("Step 2, allow policies: no binding on the resource or its ancestors grants " + q.permission + ".");
      }
      r.trace.forEach(function (t) { out.push("note: " + t); });
      return out;
    }

    function renderRequest() {
      var q = request(), r;
      try { r = E.evaluate(q, pol(), st.mode); }
      catch (err) { r = { verdict: "error", trace: [String(err.message)] }; }
      var v = document.getElementById("gcp-verdict");
      v.className = "gcp-verdict is-" + r.verdict;
      v.innerHTML = r.verdict === "error" ? "<b>Refused</b> <span>" + esc(r.trace[0]) + "</span>" :
        "<b>" + WORD[r.verdict] + "</b> <span>" + esc(who(q.principal)) + " · " + esc(q.permission) + "</span>";
      document.getElementById("gcp-trace").innerHTML = r.verdict === "error" ? "" : explain(r, q).map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("");
      var al = F.antilever, cnt = document.getElementById("gcp-count");
      var tgt = reqCases.filter(function (c) { return c.id === al.case; })[0];
      var b0 = E.held(al.member, al.count_on), b1 = E.held(al.member, al.count_on, E.withAntilever());
      var v0 = E.evaluate(tgt.request).verdict, v1 = E.evaluate(tgt.request, E.withAntilever()).verdict;
      cnt.innerHTML = st.anti
        ? "mei on sales_curated.orders: <b>" + b0 + " → " + b1 + "</b> of " + E.universe.length + " modelled permissions · " + al.case + " (read sales_raw): <b>" + WORD[v0].split(" (")[0] + " → " + WORD[v1].split(" (")[0] + "</b>"
        : "mei on sales_curated.orders: <b>" + b0 + "</b> of " + E.universe.length + " modelled permissions";
      API.state.verdict = r.verdict;
      API.state.held = st.anti ? b1 : b0;
    }

    function renderCases() {
      var res = E.score(st.mode), tb = document.getElementById("gcp-cases");
      var rows = "<tr><th>Case</th><th>Expected (from the docs)</th><th>Evaluator</th><th></th></tr>";
      F.cases.forEach(function (c) {
        var got = E.caseVerdict(c, st.mode), ok = got === c.expect;
        var title = c.kind === "binding" ? "bind " + c.binding.role + " with a condition"
          : who(c.request.principal).split("@")[0] + " · " + c.request.permission + " · " + E.nodes[c.request.resource].label + (c.request.time !== F.now ? " · at " + c.request.time.slice(0, 10) : "");
        rows += '<tr class="' + (ok ? "" : "gcp-fail") + '"><td><b>' + c.id + "</b> " + esc(title) + '<span class="gcp-doc">' + esc(c.doc) +
          "</span></td><td>" + WORD[c.expect].split(" (")[0] + "</td><td>" + WORD[got].split(" (")[0] + "</td><td>" + (ok ? "pass" : "<b>FAIL</b>") + "</td></tr>";
      });
      tb.innerHTML = rows;
      var sc = document.getElementById("gcp-score");
      sc.className = "gcp-score " + (res.fails.length ? "is-bad" : "is-good");
      sc.innerHTML = "<b>" + res.ok + " of " + F.cases.length + "</b> pass" + (res.fails.length ? " · <b>" + res.fails.length + " fail</b> (" + res.fails.join(", ") + "): the tests caught the broken logic" : "");
      API.state.score = res.ok;
    }

    /* n = the case number in the test table (c01 = 1 ... c27 = 27). Binding cases (c24, c25) show their verdict only. */
    function setCase(n) {
      var id = "c" + (n < 10 ? "0" : "") + n;
      var c = F.cases.filter(function (x) { return x.id === id; })[0];
      if (!c) return;
      if (c.kind === "binding") {
        var got = E.caseVerdict(c, st.mode), v = document.getElementById("gcp-verdict");
        v.className = "gcp-verdict is-" + (got === "refused" ? "deny" : "allow");
        v.innerHTML = "<b>" + WORD[got] + "</b> <span>" + esc(c.id + " · " + c.binding.role + " with a condition") + "</span>";
        document.getElementById("gcp-trace").innerHTML = "<li>" + esc(E.checkBinding(c.binding) || "Predefined roles accept IAM Conditions on supported resource types.") + "</li>";
        API.state.verdict = got;
        return;
      }
      selCase.value = c.id;
      selWho.value = c.request.principal; selPerm.value = c.request.permission; selRes.value = c.request.resource; inTime.value = c.request.time;
      renderRequest();
    }
    function applyMode(m) {
      st.mode = m;
      document.getElementById("gcp-flip").classList.toggle("is-on", st.mode === "allow-first");
      document.getElementById("gcp-noinh").classList.toggle("is-on", st.mode === "no-inherit");
      renderRequest(); renderCases();
    }
    function setMode(m) { applyMode(st.mode === m ? "correct" : m); }
    API.setCase = setCase;
    API.setAnti = function (on) { st.anti = !!on; document.getElementById("gcp-anti").classList.toggle("is-on", st.anti); renderRequest(); renderCases(); };
    API.setBreak = function (m) { applyMode(m || "correct"); };
    selCase.addEventListener("change", function () { setCase(Number(selCase.value.slice(1))); });
    [selWho, selPerm, selRes].forEach(function (s) { s.addEventListener("change", renderRequest); });
    inTime.addEventListener("input", renderRequest);
    document.getElementById("gcp-anti").addEventListener("click", function () { API.setAnti(!st.anti); });
    document.getElementById("gcp-flip").addEventListener("click", function () { setMode("allow-first"); });
    document.getElementById("gcp-noinh").addEventListener("click", function () { setMode("no-inherit"); });
    setCase(2); /* mei reads sales_raw: not granted, the anti-lever's target */
    renderCases();
  }

  /* ---------------- cost panel ---------------- */
  var costRoot = document.getElementById("gcp-cost-bench");
  if (costRoot) {
    var P = S.prices, L = C.ladder(S), GiB = 1073741824;
    var cst = { rung: "named" };
    API.state.cost = cst;
    var areas = [];
    S.jan2019.days[0].areas.forEach(function (a) { if (a[0] !== null) areas.push(a[0]); });
    costRoot.innerHTML =
      '<div class="gcp-panel">' +
      '<div class="gcp-stamp">Prices: BigQuery pricing page, <b>' + esc(P.region) + '</b>, retrieved <b>' + esc(P.retrieved) + '</b>: on-demand $' +
      fmt(P.on_demand_per_tib, 2) + ' per TiB, first ' + P.free_tib_per_month + ' TiB a month free, rounded up to the MB with a 10 MB minimum per table and per query. ' +
      '<b>Re-verify before delivery.</b></div>' +
      '<div class="gcp-scope">Table: <b>bigquery-public-data.chicago_taxi_trips.taxi_trips</b>, 23 columns. Bytes per column measured on <b>' +
      fmt(S.sample_rows, 0) + '</b> real trips (City of Chicago portal, Taxi Trips 2013-2023) and scaled to <b>' + fmt(S.full_rows, 0) +
      '</b> rows: scale factor <b>' + fmt(S.full_rows / S.sample_rows, 1) + '</b>. January 2019 partition counts are the portal\'s exact counts (' +
      fmt(S.jan2019.rows, 0) + ' trips). <span class="gcp-tag m">modelled</span> = the cluster rung: each day sorted by pickup_community_area into blocks of ' +
      fmt(C.BLOCK, 0) + ' rows; BigQuery\'s real block layout is not public and a dry run only gives an upper bound.</div>' +
      '<h4 class="gcp-h">1 · The ladder: one question, four ways to ask it</h4>' +
      '<div class="gcp-tablewrap"><table class="clean gcp-costs" id="gcp-ladder"></table></div>' +
      '<div class="gcp-row"><label><input type="checkbox" id="gcp-limit"> add LIMIT 10 to the selected rung</label></div>' +
      '<p class="gcp-note" id="gcp-sel"></p>' +
      '<h4 class="gcp-h">2 · Your own query on the same table</h4>' +
      '<div class="gcp-custom"><div class="gcp-cols" id="gcp-cols"></div>' +
      '<div class="gcp-row"><label>Table layout and filter <select id="gcp-part"><option value="none">not partitioned (any date filter reads every row)</option>' +
      '<option value="jan2019">partitioned by day, filter keeps January 2019</option></select></label>' +
      '<label>Cluster filter <select id="gcp-clus"><option value="">none</option></select></label></div>' +
      '<p class="gcp-note" id="gcp-own"></p></div>' +
      '<h4 class="gcp-h">3 · A month of it: on-demand or slots</h4>' +
      '<div class="gcp-row"><label>Runs a day <input id="gcp-qpd" type="number" min="0" step="1" value="200"></label>' +
      '<label>Slots <input id="gcp-slots" type="number" min="50" step="50" value="100"></label>' +
      '<label>Hours a day <input id="gcp-hrs" type="number" min="1" max="24" step="1" value="8"></label>' +
      '<label>Edition <select id="gcp-ed"></select></label></div>' +
      '<p class="gcp-note" id="gcp-month"></p>' +
      '<p class="gcp-note">' + RAIL + '</p>' +
      '<p class="gcp-note gcp-dim">This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, ' +
      'the official website of the City of Chicago. The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of ' +
      'the data provided at this site. The data provided at this site is subject to change at any time. It is understood that the data provided at this ' +
      'site is being used at one\'s own risk.</p>' +
      '</div>';

    var cols = document.getElementById("gcp-cols");
    S.columns.forEach(function (c) {
      cols.appendChild(el("label", {}, '<input type="checkbox" value="' + esc(c.name) + '"' + (C.NAMED.indexOf(c.name) >= 0 ? " checked" : "") + "> " + esc(c.name)));
    });
    var cl = document.getElementById("gcp-clus");
    areas.sort(function (a, b) { return a - b; }).forEach(function (a) { cl.appendChild(el("option", { value: a }, "pickup_community_area = " + a + (a === 56 ? " (Midway)" : a === 76 ? " (O'Hare)" : a === 8 ? " (Near North Side)" : ""))); });
    var ed = document.getElementById("gcp-ed");
    Object.keys(P.slot_hour).forEach(function (k) { ed.appendChild(el("option", { value: k }, esc(k + " $" + P.slot_hour[k] + " per slot-hour"))); });

    function cur() { return L.filter(function (r) { return r.id === cst.rung; })[0]; }
    function renderLadder() {
      var rows = "<tr><th>Rung</th><th>Rows read</th><th>Processed</th><th>Billed</th><th>On-demand, one run</th></tr>";
      L.forEach(function (r) {
        rows += '<tr class="' + (r.id === cst.rung ? "gcp-on" : "") + '" data-rung="' + r.id + '"><td><b>' + esc(r.label) + "</b>" +
          (r.blocks ? ' <span class="gcp-tag m">modelled</span><span class="gcp-doc">' + r.blocks.blocks + " of " + r.blocks.allBlocks + " blocks read</span>" : "") +
          "</td><td>" + fmt(r.rows, 0) + "</td><td>" + fmt(r.bytes / GiB, 4) + " GiB</td><td>" + fmt(r.billed / C.MB, 0) + " MB</td><td>$" + fmt(r.cost, 4) + "</td></tr>";
      });
      document.getElementById("gcp-ladder").innerHTML = rows;
      [].slice.call(document.querySelectorAll("#gcp-ladder tr[data-rung]")).forEach(function (tr) {
        tr.addEventListener("click", function () { API.setRung(tr.getAttribute("data-rung")); });
      });
      var r = cur(), star = L[0];
      document.getElementById("gcp-sel").innerHTML = "Selected: <b>" + esc(r.label) + "</b> reads <b>" + fmt(100 * r.bytes / star.bytes, 3) + "%</b> of SELECT *. " +
        (document.getElementById("gcp-limit").checked ? "With LIMIT 10 the bytes are <b>unchanged</b>: BigQuery charges for the columns read, \"even if you set an explicit LIMIT\". " : "") +
        (r.billed > r.bytes && r.bytes < 10 * C.MB ? "Billed is the <b>10 MB minimum</b>, more than the " + fmt(r.bytes / C.MB, 1) + " MB processed." : "");
      API.state.rungBytes = r.bytes; API.state.rungBilled = r.billed;
      renderMonth();
    }
    function renderOwn() {
      var picked = [].slice.call(cols.querySelectorAll("input:checked")).map(function (x) { return x.value; });
      if (!picked.length) { document.getElementById("gcp-own").innerHTML = "Pick at least one column."; return; }
      var part = document.getElementById("gcp-part").value, cv = cl.value;
      cl.disabled = part !== "jan2019";
      var r = C.run(S, { cols: picked, partition: part, cluster: part === "jan2019" && cv !== "" ? Number(cv) : null });
      document.getElementById("gcp-own").innerHTML = picked.length + " column" + (picked.length > 1 ? "s" : "") + ", " + fmt(r.rows, 0) + " rows read" +
        (r.blocks ? ' <span class="gcp-tag m">modelled</span> (' + r.blocks.blocks + " of " + r.blocks.allBlocks + " blocks)" : "") + ": <b>" + fmt(r.bytes / GiB, 4) +
        " GiB</b> processed, <b>" + fmt(r.billed / C.MB, 0) + " MB</b> billed, <b>$" + fmt(r.cost, 4) + "</b> a run.";
    }
    function renderMonth() {
      var r = cur(), qpd = Math.max(0, Number(document.getElementById("gcp-qpd").value) || 0);
      var slots = Math.max(50, Number(document.getElementById("gcp-slots").value) || 50), hrs = Math.min(24, Math.max(1, Number(document.getElementById("gcp-hrs").value) || 1));
      var m = C.monthly(S, r.billed, qpd, slots, hrs, ed.value);
      document.getElementById("gcp-month").innerHTML = "The selected rung, " + qpd + " runs a day for 30 days: <b>" + fmt(m.tib, 2) + " TiB</b> billed. On-demand after the free TiB: <b>$" +
        fmt(m.onDemand, 2) + "</b> a month. A " + slots + "-slot " + esc(ed.value) + " reservation billed " + hrs + " hours a day: <b>$" + fmt(m.capacity, 2) +
        "</b> a month <span class=\"gcp-tag m\">assumption</span> (real autoscaling bills slot-seconds used, in steps of 50 slots, one-minute minimum; whether 100 slots finish the work in time is not modelled).";
      API.state.month = m;
    }
    API.setRung = function (id) { if (L.some(function (r) { return r.id === id; })) { cst.rung = id; renderLadder(); } };
    API.ladder = L;
    document.getElementById("gcp-limit").addEventListener("change", renderLadder);
    cols.addEventListener("change", renderOwn);
    ["gcp-part", "gcp-clus"].forEach(function (id) { document.getElementById(id).addEventListener("change", renderOwn); });
    ["gcp-qpd", "gcp-slots", "gcp-hrs"].forEach(function (id) { document.getElementById(id).addEventListener("input", renderMonth); });
    ed.addEventListener("change", renderMonth);
    renderLadder(); renderOwn();
  }
})();
