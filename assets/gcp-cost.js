/* learn-gcp-with-phoebe - BigQuery on-demand cost engine (GcpCost).
   Bytes follow BigQuery's documented LOGICAL sizes (INT64/FLOAT64/TIMESTAMP 8, STRING 2 + UTF-8
   bytes, NULL 0), measured per column on the real sample in gcp-sample.js and scaled to the full
   table's row count. Only referenced columns count; a partition filter keeps only the rows in the
   kept partitions; charges round up to the nearest MB with a 10 MB minimum per table and per query.
   CLUSTERING IS MODELLED: BigQuery's block layout is not public. Each day partition is sorted by the
   cluster column into fixed blocks of BLOCK rows, and the query reads every block its value touches.
   Python twin: materials/cost_ref.py (must agree to the byte). */
(function (root) {
  "use strict";
  var MB = 1048576, TIB = 1099511627776, BLOCK = 5000;

  function colTotal(S, name) {
    var c = null;
    for (var i = 0; i < S.columns.length; i++) if (S.columns[i].name === name) c = S.columns[i];
    if (!c) throw new Error("unknown column " + name);
    var t = 0;
    c.hist.forEach(function (h) { t += h[0] * h[1]; });
    return t; /* logical bytes of this column over all sample rows */
  }

  /* rows x (sum of column bytes over the sample) / sample rows, rounded half up, in integers */
  function scaled(S, cols, rows) {
    var a = 0;
    cols.forEach(function (c) { a += colTotal(S, c); });
    var n = S.sample_rows, num = rows * a;
    return Math.floor((2 * num + n) / (2 * n));
  }

  /* rows read by the modelled cluster layout when filtering cluster column = value, per day */
  function clusterRows(S, value) {
    var total = 0, blocks = 0, all = 0;
    S.jan2019.days.forEach(function (d) {
      var start = 0, dayRows = 0;
      d.areas.forEach(function (a) { dayRows += a[1]; });
      var nb = Math.ceil(dayRows / BLOCK);
      all += nb;
      d.areas.forEach(function (a) {
        var n = a[1];
        if (a[0] === value && n > 0) {
          var b0 = Math.floor(start / BLOCK), b1 = Math.floor((start + n - 1) / BLOCK);
          for (var b = b0; b <= b1; b++) { total += Math.min(BLOCK, dayRows - b * BLOCK); blocks += 1; }
        }
        start += n;
      });
    });
    return { rows: total, blocks: blocks, allBlocks: all };
  }

  function billed(bytes) {
    var mb = Math.ceil(bytes / MB);
    return Math.max(mb, 10) * MB; /* one table per query here, so the per-table and per-query minimums coincide */
  }

  function dollars(b, S) { return b / TIB * S.prices.on_demand_per_tib; }

  /* q = {cols:[...], partition:"none"|"jan2019", cluster:null|value} */
  function run(S, q) {
    var rows, note = "", blk = null;
    if (q.partition === "jan2019") {
      if (q.cluster !== null && q.cluster !== undefined) {
        blk = clusterRows(S, q.cluster);
        rows = blk.rows;
        note = "modelled cluster blocks";
      } else rows = S.jan2019.rows;
    } else rows = S.full_rows;
    var bytes = scaled(S, q.cols, rows), b = billed(bytes);
    return { rows: rows, bytes: bytes, billed: b, cost: dollars(b, S), blocks: blk, note: note };
  }

  var ALL = function (S) { return S.columns.map(function (c) { return c.name; }); };
  var NAMED = ["trip_start_timestamp", "pickup_community_area", "fare"];
  function ladder(S) {
    return [
      { id: "star", label: "SELECT * on the whole table", q: { cols: ALL(S), partition: "none", cluster: null } },
      { id: "named", label: "Three named columns, filter on the date, table not partitioned", q: { cols: NAMED, partition: "none", cluster: null } },
      { id: "part", label: "+ table partitioned by day, filter keeps January 2019", q: { cols: NAMED, partition: "jan2019", cluster: null } },
      { id: "clus", label: "+ clustered by pickup_community_area, filter = 56 (Midway)", q: { cols: NAMED, partition: "jan2019", cluster: 56 } }
    ].map(function (r) { var o = run(S, r.q); o.id = r.id; o.label = r.label; return o; });
  }

  /* monthly: on-demand for N queries a day vs a slot reservation billed for the hours set */
  function monthly(S, billedPerQuery, perDay, slots, hoursPerDay, edition) {
    var tib = billedPerQuery * perDay * 30 / TIB;
    var od = Math.max(0, tib - S.prices.free_tib_per_month) * S.prices.on_demand_per_tib;
    var cap = slots * hoursPerDay * 30 * S.prices.slot_hour[edition];
    return { tib: tib, onDemand: od, capacity: cap };
  }

  var api = { MB: MB, TIB: TIB, BLOCK: BLOCK, NAMED: NAMED, run: run, ladder: ladder, billed: billed,
              clusterRows: clusterRows, scaled: scaled, monthly: monthly, colTotal: colTotal };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.GcpCost = api;
})(this);
