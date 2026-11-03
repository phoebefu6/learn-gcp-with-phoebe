/* learn-gcp-with-phoebe - Google Cloud IAM evaluator (GcpIam), for the constructed Tidewater fixture.
   Documented order (read at source 2026-11-03): deny policies first ("IAM always checks relevant deny
   policies before checking relevant allow policies"), inherited from the organization, folder or
   project they attach to; then allow policies UNIONED from the resource up to the organization;
   anything else is not granted. Role permission lists come from the IAM roles reference pages
   (BigQuery, Cloud Storage), 2026-11-03. Legacy basic roles are MODELLED from their documented
   definitions (Viewer read-only, Editor adds state-changing actions, Owner adds managing roles).
   CEL subset only: resource.name.startsWith, request.time compared with timestamp(), resource.matchTag,
   !, &&, ||, parentheses; anything else throws rather than guessing.
   Python twin: materials/iam_eval.py (verdicts must be identical). */
(function (root) {
  "use strict";
  var FQDN = { bigquery: "bigquery.googleapis.com", storage: "storage.googleapis.com", resourcemanager: "cloudresourcemanager.googleapis.com" };
  var READ_VERBS = { get: 1, list: 1, getData: 1, getMetadata: 1, getIamPolicy: 1 };
  var BASIC = { "roles/viewer": 1, "roles/editor": 1, "roles/owner": 1 };
  var PUB = "principalSet://goog/public:all";

  function make(D) {
    var ROLES = {}, U = {}, UNIVERSE, NODES = {}, cache = {};
    Object.keys(D.roles).forEach(function (k) {
      if (k.charAt(0) === "_") return;
      ROLES[k] = {};
      D.roles[k].forEach(function (p) { ROLES[k][p] = 1; U[p] = 1; });
    });
    UNIVERSE = Object.keys(U).sort();
    D.fixture.nodes.forEach(function (n) { NODES[n.id] = n; });

    function verb(p) { var a = p.split("."); return a[a.length - 1]; }
    function rolePerms(role) {
      if (cache[role]) return cache[role];
      var s = {};
      if (ROLES[role]) s = ROLES[role];
      else if (role === "roles/viewer") UNIVERSE.forEach(function (p) { if (READ_VERBS[verb(p)]) s[p] = 1; });
      else if (role === "roles/editor") UNIVERSE.forEach(function (p) { if (verb(p) !== "setIamPolicy") s[p] = 1; });
      else if (role === "roles/owner") UNIVERSE.forEach(function (p) { s[p] = 1; });
      else throw new Error("unknown role " + role);
      cache[role] = s;
      return s;
    }

    /* ---- CEL subset ---- */
    var TOK = /^\s*(\|\||&&|<=|>=|<|>|!|\(|\)|,|\.|'[^']*'|[A-Za-z_][A-Za-z_0-9]*)/;
    function tokenize(s) {
      var out = [], rest = s.trim();
      while (rest.length) {
        var m = TOK.exec(rest);
        if (!m || !m[0].length) throw new Error("unsupported CEL near: " + rest.slice(0, 20));
        out.push(m[1]); rest = rest.slice(m[0].length).replace(/^\s+/, "");
      }
      return out;
    }
    function cel(expr, ctx) {
      var t = tokenize(expr), i = 0;
      function peek() { return i < t.length ? t[i] : null; }
      function take(x) { var v = peek(); if (x !== undefined && v !== x) throw new Error("unsupported CEL: expected " + x + " got " + v); i++; return v; }
      function str() { var v = take(); if (!v || v.charAt(0) !== "'") throw new Error("unsupported CEL: expected string"); return v.slice(1, -1); }
      function primary() {
        var x = peek();
        if (x === "!") { take(); return !primary(); }
        if (x === "(") { take(); var v = orr(); take(")"); return v; }
        if (x === "resource") {
          take(); take(".");
          var nm = take();
          if (nm === "name") { take("."); take("startsWith"); take("("); var p = str(); take(")"); return ctx.name.indexOf(p) === 0; }
          if (nm === "matchTag") { take("("); var k = str(); take(","); var val = str(); take(")"); return ctx.tags[k] === val; }
          throw new Error("unsupported CEL attribute resource." + nm);
        }
        if (x === "request") {
          take(); take("."); take("time");
          var op = take();
          if (["<", "<=", ">", ">="].indexOf(op) < 0) throw new Error("unsupported CEL operator " + op);
          take("timestamp"); take("("); var ts = str(); take(")");
          var a = ctx.time;
          return op === "<" ? a < ts : op === "<=" ? a <= ts : op === ">" ? a > ts : a >= ts;
        }
        throw new Error("unsupported CEL token " + x);
      }
      function andd() { var v = primary(); while (peek() === "&&") { take(); var w = primary(); v = v && w; } return v; }
      function orr() { var v = andd(); while (peek() === "||") { take(); var w = andd(); v = v || w; } return v; }
      var v = orr();
      if (peek() !== null) throw new Error("unsupported CEL trailing " + peek());
      return v;
    }

    function ancestors(id) { var out = []; while (id) { out.push(NODES[id]); id = NODES[id].parent; } return out; }
    function effTags(id) {
      var tags = {}, a = ancestors(id).reverse();
      a.forEach(function (n) { var t = n.tags || {}; Object.keys(t).forEach(function (k) { tags[k] = t[k]; }); });
      return tags;
    }
    function principalsOf(p) {
      var s = {}; s[p] = 1; s[PUB] = 1;
      Object.keys(D.fixture.groups).forEach(function (g) { if (D.fixture.groups[g].indexOf(p) >= 0) s[g] = 1; });
      return s;
    }
    function anyIn(set, list) { for (var i = 0; i < (list || []).length; i++) if (set[list[i]]) return true; return false; }
    function toFqdn(perm) { var i = perm.indexOf("."), svc = perm.slice(0, i); return (FQDN[svc] || svc + ".googleapis.com") + "/" + perm.slice(i + 1); }
    function matchesPerm(pf, pats) {
      var svc = pf.split("/")[0], rest = pf.slice(svc.length + 1), res = rest.split(".")[0];
      for (var i = 0; i < (pats || []).length; i++) {
        var p = pats[i];
        if (p === pf || p === svc + "/*.*" || p === svc + "/" + res + ".*") return true;
      }
      return false;
    }
    function checkBinding(b) {
      if (b.condition && BASIC[b.role]) return "You cannot use conditions when you grant legacy basic roles";
      return null;
    }

    /* mode: correct | allow-first | no-inherit */
    function evaluate(req, pol, mode) {
      pol = pol || D.fixture; mode = mode || "correct";
      var chain = ancestors(req.resource);
      if (mode === "no-inherit") chain = chain.slice(0, 1);
      var who = principalsOf(req.principal), trace = [];
      var ctx = { name: NODES[req.resource].name, tags: effTags(req.resource), time: req.time };

      function denyHit() {
        var pf = toFqdn(req.permission);
        for (var i = 0; i < chain.length; i++) {
          var rules = pol.deny[chain[i].id] || [];
          for (var j = 0; j < rules.length; j++) {
            var r = rules[j];
            if (!anyIn(who, r.deniedPrincipals)) continue;
            if (anyIn(who, r.exceptionPrincipals)) { trace.push("deny rule " + r.name + " at " + chain[i].label + ": principal is an exception"); continue; }
            if (!matchesPerm(pf, r.deniedPermissions)) continue;
            if (matchesPerm(pf, r.exceptionPermissions)) { trace.push("deny rule " + r.name + " at " + chain[i].label + ": permission is an exception"); continue; }
            if (r.denialCondition && !cel(r.denialCondition, ctx)) { trace.push("deny rule " + r.name + " at " + chain[i].label + ": denial condition false"); continue; }
            return { at: chain[i], rule: r };
          }
        }
        return null;
      }
      function allowHit() {
        for (var i = 0; i < chain.length; i++) {
          var bs = pol.allow[chain[i].id] || [];
          for (var j = 0; j < bs.length; j++) {
            var b = bs[j];
            if (!anyIn(who, b.members)) continue;
            if (!rolePerms(b.role)[req.permission]) continue;
            if (b.condition && !cel(b.condition, ctx)) { trace.push("binding " + b.role + " at " + chain[i].label + ": condition false"); continue; }
            return { at: chain[i], binding: b };
          }
        }
        return null;
      }
      var a;
      if (mode === "allow-first") {
        a = allowHit();
        if (a) return { verdict: "allow", step: "allow", at: a.at.id, where: a.at.label, role: a.binding.role, trace: trace };
      }
      var d = denyHit();
      if (d) return { verdict: "deny", step: "deny", at: d.at.id, where: d.at.label, rule: d.rule.name, trace: trace };
      a = allowHit();
      if (a) return { verdict: "allow", step: "allow", at: a.at.id, where: a.at.label, role: a.binding.role, trace: trace };
      return { verdict: "not-granted", step: "none", trace: trace };
    }

    function withAntilever() {
      var pol = JSON.parse(JSON.stringify(D.fixture));
      var al = D.fixture.antilever;
      (pol.allow[al.at] = pol.allow[al.at] || []).push({ role: "roles/editor", members: [al.member] });
      return pol;
    }
    function held(principal, resource, pol) {
      var n = 0;
      UNIVERSE.forEach(function (p) {
        if (evaluate({ principal: principal, permission: p, resource: resource, time: D.fixture.now }, pol).verdict === "allow") n++;
      });
      return n;
    }
    function caseVerdict(c, mode, pol) {
      if (c.kind === "binding") return checkBinding(c.binding) ? "refused" : "accepted";
      return evaluate(c.request, pol, mode).verdict;
    }
    function score(mode) {
      var ok = 0, fails = [];
      D.fixture.cases.forEach(function (c) { if (caseVerdict(c, mode) === c.expect) ok++; else fails.push(c.id); });
      return { ok: ok, fails: fails };
    }
    function run() {
      var cases = D.fixture.cases, al = D.fixture.antilever, pol = withAntilever();
      var target = cases.filter(function (c) { return c.id === al.case; })[0];
      var holds = cases.filter(function (c) { return c.id === al.holds; })[0];
      var allowedBefore = 0, allowedAfter = 0;
      cases.forEach(function (c) {
        if (c.kind === "binding") return;
        if (evaluate(c.request).verdict === "allow") allowedBefore++;
        if (evaluate(c.request, pol).verdict === "allow") allowedAfter++;
      });
      return {
        cases: cases.map(function (c) { return { id: c.id, expect: c.expect, got: caseVerdict(c, "correct") }; }),
        scores: { "correct": score("correct").ok, "allow-first": score("allow-first").ok, "no-inherit": score("no-inherit").ok },
        antilever: {
          "case": al.case, before: evaluate(target.request).verdict, after: evaluate(target.request, pol).verdict,
          held_before: held(al.member, al.count_on), held_after: held(al.member, al.count_on, pol),
          universe: UNIVERSE.length, allowed_cases_before: allowedBefore, allowed_cases_after: allowedAfter,
          still_denied: evaluate(holds.request, pol).verdict
        }
      };
    }
    return { evaluate: evaluate, withAntilever: withAntilever, held: held, score: score, run: run,
             caseVerdict: caseVerdict, checkBinding: checkBinding, universe: UNIVERSE, nodes: NODES, cel: cel };
  }

  var api = { make: make };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.GcpIam = api;
})(this);
