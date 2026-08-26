/* Home By Five workbench: tab shell, content renderer, live economics model,
   and the evidence ledger loaded straight from research/source_ledger.csv. */
(function () {
  var ECON = null, LEDGER = null;
  var TABS = [
    ["verdict", "Verdict"], ["model", "Model"], ["anchors", "Anchors"],
    ["offers", "Offers"], ["guarantees", "Guarantees"], ["risks", "Risks"],
    ["market", "Market size"], ["evidence", "Evidence"], ["build", "Build"]
  ];

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function usd(v) { return "$" + Math.round(v).toLocaleString("en-US"); }

  /* ---------------------------------------------------------- content blocks */
  function renderBlocks(sec) {
    var h = '<div class="eyebrow">Home By Five</div><h1>' + sec.title + "</h1>";
    if (sec.lede) h += '<p class="lede">' + sec.lede + "</p>";
    sec.blocks.forEach(function (b) {
      if (b.t === "h") h += "<h2>" + b.v + "</h2>";
      else if (b.t === "p") h += "<p>" + b.v + "</p>";
      else if (b.t === "code") h += '<div class="panel tight"><pre class="mono" style="margin:0;'
        + 'white-space:pre;overflow-x:auto;color:var(--ink-2);font-size:12.5px">' + esc(b.v) + "</pre></div>";
      else if (b.t === "callout") {
        h += '<div class="callout ' + (b.cls || "") + '">';
        if (b.h) h += '<div class="h">' + b.h + "</div>";
        (b.p || []).forEach(function (p) { h += "<p>" + p + "</p>"; });
        h += "</div>";
      } else if (b.t === "stats") {
        h += '<div class="grid g4" style="margin:16px 0">';
        b.items.forEach(function (i) {
          h += '<div class="stat"><div class="k">' + i[0] + '</div><div class="v ' + (i[2] || "")
            + '">' + i[1] + '</div><div class="n">' + (i[3] || "") + "</div></div>";
        });
        h += "</div>";
      } else if (b.t === "list") {
        if (b.h) h += "<h3>" + b.h + "</h3>";
        h += '<ul class="clean">' + b.items.map(function (i) { return "<li>" + i + "</li>"; }).join("") + "</ul>";
      } else if (b.t === "kv") {
        h += '<div class="panel tight"><dl class="kv">'
          + b.items.map(function (i) { return "<dt>" + i[0] + "</dt><dd>" + i[1] + "</dd>"; }).join("")
          + "</dl></div>";
      } else if (b.t === "table") {
        h += '<div class="tablewrap"><table><thead><tr>'
          + b.head.map(function (x) { return "<th>" + x + "</th>"; }).join("")
          + "</tr></thead><tbody>"
          + b.rows.map(function (r) {
            return "<tr>" + r.map(function (c) { return "<td>" + c + "</td>"; }).join("") + "</tr>";
          }).join("")
          + "</tbody></table></div>";
      } else if (b.t === "qa") {
        h += '<div class="grid g2">';
        b.items.forEach(function (i, n) {
          h += '<div class="panel"><div class="eyebrow">Q' + (n + 1) + '</div>'
            + '<h3 style="margin-top:0">' + i[0] + "</h3><p>" + i[1] + "</p></div>";
        });
        h += "</div>";
      }
    });
    return h;
  }

  /* ------------------------------------------------------------ economics model */
  var M = { tier: "STANDARD", accounts: 40, price: 300, owner: null, expert: null, office: true };

  function companyLayer(nPods) {
    var f = { "Growth / Product Director (owner)": 1.0 };
    f["QA Lead"] = nPods <= 1 ? 0.5 : (nPods <= 3 ? 1.0 : 2.0);
    if (nPods >= 2) {
      f["Automation / Data Engineer"] = 1.0;
      f["Paid Media Specialist"] = 0.5;
      f["Account / Project Coordinator"] = Math.ceil(nPods / 3);
    }
    return f;
  }

  function compute() {
    var sal = {};
    ECON.roles.forEach(function (r) { sal[r.role] = r.employer_usd; });
    var oh = ECON.overheads_usd;
    var shape = ECON.pod_shapes[M.tier];
    var nPods = M.accounts / ECON.pod_size;
    var whole = Math.max(1, Math.ceil(nPods));

    var podLabour = 0, podSeats = 0;
    Object.keys(shape).forEach(function (r) { podLabour += sal[r] * shape[r] * nPods; podSeats += shape[r] * nPods; });

    var comp = companyLayer(whole), compLabour = 0, compSeats = 0;
    Object.keys(comp).forEach(function (r) {
      var rate = (r.indexOf("Director") >= 0 && M.owner !== null) ? M.owner : sal[r];
      compLabour += rate * comp[r];
      compSeats += comp[r];
    });

    var seats = podSeats + compSeats;
    var overhead = oh.workspace_per_seat_month * seats * (M.office ? 1 : 0)
      + oh.equipment_per_seat_month * seats
      + oh.recruiting_per_hire_amortised_month * seats
      + oh.software_base_month + oh.software_per_pod_month * nPods
      + oh.accounting_payroll_month + oh.connectivity_utilities_month;
    var expert = (M.expert === null ? ECON.expert_budget_per_pod_usd : M.expert) * nPods;
    var sub = podLabour + compLabour + overhead + expert;
    var total = sub * (1 + ECON.contingency);
    var mrr = M.price * M.accounts;

    return {
      seats: seats, podLabour: podLabour, compLabour: compLabour, overhead: overhead,
      expert: expert, contingency: sub * ECON.contingency, total: total,
      perAccount: total / M.accounts, mrr: mrr, arr: mrr * 12,
      gp: mrr - total, gm: mrr ? 100 * (mrr - total) / mrr : 0, pods: nPods
    };
  }

  function renderModel() {
    var h = '<div class="eyebrow">Home By Five</div><h1>Unit economics</h1>'
      + '<p class="lede">Live model. Salary inputs are gross-up calculations over North '
      + 'Macedonian statutory rates; overheads are Skopje market costs. Move the controls and '
      + 'watch where $300 sits against the cost line.</p>'
      + '<div class="grid" style="grid-template-columns:minmax(280px,340px) 1fr;align-items:start">'

      + '<div class="panel">'
      + '<div class="eyebrow">Controls</div>'
      + '<div class="field"><label>Service tier</label><div class="seg" id="tierseg"></div>'
      + '<p class="muted" id="tierdesc" style="margin:8px 0 0"></p></div>'
      + '<div class="field"><label>Book size <b id="accv"></b></label>'
      + '<input type="range" id="acc" min="20" max="400" step="10"></div>'
      + '<div class="field"><label>Price per unit / month <b id="prv"></b></label>'
      + '<input type="range" id="pr" min="150" max="800" step="10"></div>'
      + '<div class="field"><label>Owner draw / month <b id="owv"></b></label>'
      + '<input type="range" id="ow" min="1000" max="6000" step="100"></div>'
      + '<div class="field"><label>Expert budget per pod / month <b id="exv"></b></label>'
      + '<input type="range" id="ex" min="0" max="4000" step="100"></div>'
      + '<label class="toggle"><input type="checkbox" id="off" checked> Skopje office '
      + '(uncheck for remote-first)</label>'
      + '<p class="muted" style="margin-top:14px">One pod covers ' + ECON.pod_size
      + ' accounts. The company layer grows in steps, which is the only place operating '
      + 'leverage comes from.</p>'
      + "</div>"

      + '<div id="out"></div></div>';

    document.getElementById("view").innerHTML = h;

    var seg = document.getElementById("tierseg");
    Object.keys(ECON.pod_shapes).forEach(function (t) {
      var b = document.createElement("button");
      b.textContent = t;
      b.onclick = function () { M.tier = t; sync(); };
      seg.appendChild(b);
    });
    document.getElementById("acc").value = M.accounts;
    document.getElementById("pr").value = M.price;
    document.getElementById("ow").value = M.owner === null
      ? Math.round(ECON.roles[0].employer_usd) : M.owner;
    document.getElementById("ex").value = M.expert === null
      ? ECON.expert_budget_per_pod_usd : M.expert;
    document.getElementById("off").checked = M.office;

    ["acc", "pr", "ow", "ex"].forEach(function (id) {
      document.getElementById(id).oninput = function () {
        M.accounts = +document.getElementById("acc").value;
        M.price = +document.getElementById("pr").value;
        M.owner = +document.getElementById("ow").value;
        M.expert = +document.getElementById("ex").value;
        sync();
      };
    });
    document.getElementById("off").onchange = function () { M.office = this.checked; sync(); };
    sync();
  }

  function sync() {
    document.querySelectorAll("#tierseg button").forEach(function (b) {
      b.className = b.textContent === M.tier ? "on" : "";
    });
    var shape = ECON.pod_shapes[M.tier];
    document.getElementById("tierdesc").textContent =
      Object.keys(shape).map(function (r) {
        return (shape[r] === 1 ? "" : shape[r] + "x ") + r.replace(" / ", "/");
      }).join(", ") + " per " + ECON.pod_size + " units";

    document.getElementById("accv").textContent = M.accounts + " units";
    document.getElementById("prv").textContent = usd(M.price);
    document.getElementById("owv").textContent = usd(M.owner);
    document.getElementById("exv").textContent = usd(M.expert);

    var c = compute();
    var ok = c.gm >= 30, marginal = c.gm >= 0;
    var cls = ok ? "good" : (marginal ? "warn" : "bad");

    var costRows = [
      ["Pod delivery labour", c.podLabour, "Scales linearly with the book"],
      ["Company layer labour", c.compLabour, "Director, QA, automation, coordination"],
      ["Workspace, equipment, tooling, admin", c.overhead, "Skopje costs at " + c.seats.toFixed(1) + " seats"],
      ["Outside expert budget", c.expert, "Specialist audits translated into SOPs"],
      ["Contingency at " + Math.round(ECON.contingency * 100) + "%", c.contingency, "Turnover, sick cover, overrun"]
    ];

    document.getElementById("out").innerHTML =
      '<div class="grid g4" style="margin-bottom:14px">'
      + tile("MRR", usd(c.mrr), "", usd(c.arr) + " ARR")
      + tile("Delivery cost", usd(c.total), "", c.seats.toFixed(1) + " FTE across " + c.pods.toFixed(2) + " pods")
      + tile("Cost per unit", "$" + c.perAccount.toFixed(0), c.perAccount > M.price ? "bad" : "good",
             "Breakeven price per unit / month")
      + tile("Gross margin", c.gm.toFixed(1) + "%", cls, usd(c.gp) + " per month")
      + "</div>"

      + (marginal
        ? '<div class="callout ' + (ok ? "good" : "warn") + '"><div class="h">'
          + (ok ? "This configuration works" : "Above water, but thin")
          + "</div><p>" + (ok
            ? "A margin above 30 percent leaves room for sales cost, tax, churn and a second senior hire."
            : "A margin under 30 percent leaves nothing for sales cost, churn or the second senior "
              + "strategist you will need before the third pod. Treat this as break-even, not profit.")
          + "</p></div>"
        : '<div class="callout bad"><div class="h">This configuration loses money</div><p>'
          + "At " + usd(M.price) + " per unit against a cost of $" + c.perAccount.toFixed(0)
          + ", every unit sold loses $" + (c.perAccount - M.price).toFixed(0)
          + " a month. Raise the price to $" + Math.ceil(c.perAccount / 10) * 10
          + " to break even, or strip the tier.</p></div>")

      + '<div class="panel"><h3 style="margin-top:0">Where the money goes</h3>'
      + costRows.map(function (r) {
        var pct = 100 * r[1] / c.total;
        return '<div class="scorebar"><span class="lab">' + r[0] + "</span>"
          + '<span class="bar" title="' + r[2] + '"><i style="width:' + pct.toFixed(1) + '%"></i></span>'
          + '<span class="val">' + usd(r[1]) + "</span></div>";
      }).join("")
      + '<p class="muted" style="margin-top:12px">Assumptions: contributions '
      + Math.round(ECON.statutory.contribution_rate * 100) + "% of gross, "
      + Math.round(ECON.statutory.pit_rate * 100) + "% flat income tax, monthly personal "
      + "allowance MKD " + ECON.statutory.monthly_allowance_mkd.toLocaleString("en-US")
      + ", employer add-on " + Math.round(ECON.statutory.employer_addon * 100) + "%, admin buffer "
      + Math.round((ECON.statutory.admin_buffer - 1) * 100) + "%. FX at "
      + ECON.fx.eur_usd.toFixed(3) + " EUR/USD and " + ECON.fx.eur_mkd.toFixed(1)
      + " EUR/MKD, captured " + ECON.fx.captured + ".</p></div>"

      + '<div class="panel"><h3 style="margin-top:0">Breakeven price per unit, by tier and book size</h3>'
      + breakevenTable() + "</div>"

      + '<div class="panel"><h3 style="margin-top:0">Scaling path</h3>' + scalePath() + "</div>";
  }

  function breakevenTable() {
    var sizes = [40, 80, 120, 150, 200, 300];
    var tiers = Object.keys(ECON.pod_shapes);
    var save = { tier: M.tier, accounts: M.accounts };
    var h = '<div class="tablewrap"><table><thead><tr><th>Book</th>'
      + tiers.map(function (t) { return '<th class="num">' + t + "</th>"; }).join("")
      + "</tr></thead><tbody>";
    sizes.forEach(function (s) {
      h += '<tr><td class="mono">' + s + " units</td>";
      tiers.forEach(function (t) {
        M.tier = t; M.accounts = s;
        var v = compute().perAccount;
        var col = v <= M.price ? "var(--good)" : (v <= M.price * 1.3 ? "var(--warn)" : "var(--bad)");
        h += '<td class="num" style="color:' + col + '">$' + v.toFixed(0) + "</td>";
      });
      h += "</tr>";
    });
    M.tier = save.tier; M.accounts = save.accounts;
    return h + "</tbody></table></div><p class=\"muted\" style=\"margin-top:10px\">Green means "
      + "the current price of " + usd(M.price) + " clears cost. Red means it does not.</p>";
  }

  function scalePath() {
    var save = { accounts: M.accounts, tier: M.tier };
    var steps = [
      ["$10k MRR", "One pod, owner doing senior delivery, no automation engineer yet. The "
        + "riskiest phase: everything depends on one person staying healthy."],
      ["$30k MRR", "Two pods. Automation engineer hired, QA lead full time. The owner should be "
        + "out of day-to-day execution here or the ceiling arrives early."],
      ["$50k MRR", "Three pods, coordinator layer, second senior strategist. This is the first "
        + "point the company survives the owner taking two weeks off."],
      ["$100k MRR", "Second anchor vertical signed. Owner entirely on product, pricing and "
        + "expert acquisition. Single-client concentration must be under 50 percent by here."]
    ];
    var h = '<div class="grid g2">';
    steps.forEach(function (s, i) {
      var target = [10000, 30000, 50000, 100000][i];
      M.tier = "STANDARD"; M.accounts = Math.round(target / M.price / 10) * 10;
      var c = compute();
      h += '<div class="panel tight" style="background:var(--panel-2)">'
        + '<div class="eyebrow">' + s[0] + "</div>"
        + '<div class="mono" style="font-size:13px;margin-bottom:6px">'
        + M.accounts + " units at " + usd(M.price) + " &middot; " + c.seats.toFixed(1) + " FTE &middot; "
        + '<span style="color:' + (c.gm >= 30 ? "var(--good)" : c.gm >= 0 ? "var(--warn)" : "var(--bad)")
        + '">' + c.gm.toFixed(0) + "% margin</span></div>"
        + '<p class="muted" style="margin:0">' + s[1] + "</p></div>";
    });
    M.accounts = save.accounts; M.tier = save.tier;
    return h + "</div>";
  }

  function tile(k, v, cls, n) {
    return '<div class="stat"><div class="k">' + k + '</div><div class="v ' + (cls || "")
      + '">' + v + '</div><div class="n">' + (n || "") + "</div></div>";
  }

  /* -------------------------------------------------------------- evidence tab */
  function parseCSV(text) {
    var rows = [], row = [], cell = "", q = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (q) {
        if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
        else if (c === '"') q = false;
        else cell += c;
      } else if (c === '"') q = true;
      else if (c === ",") { row.push(cell); cell = ""; }
      else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
      else if (c !== "\r") cell += c;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    var head = rows.shift();
    return rows.filter(function (r) { return r.length > 1; }).map(function (r) {
      var o = {}; head.forEach(function (h, i) { o[h] = r[i] || ""; }); return o;
    });
  }

  function classBadge(v) {
    var s = v.toUpperCase();
    if (s.indexOf("MODEL") === 0) return "model";
    if (s.indexOf("STRONG") === 0) return "inference";
    if (s.indexOf("FACT") === 0) return "fact";
    return "";
  }

  function renderEvidence() {
    var h = '<div class="eyebrow">Home By Five</div><h1>Evidence ledger</h1>'
      + '<p class="lede">Every externally sourced claim in this study, with its class, its '
      + 'confidence and the reason sources disagree where they do. Loaded live from '
      + '<code>research/source_ledger.csv</code>.</p>'
      + '<div class="ctrlrow"><input type="text" id="eq" placeholder="Filter claims" style="min-width:240px">'
      + '<select id="ec"><option value="">All classes</option><option>FACT</option>'
      + '<option>STRONG INFERENCE</option><option>MODEL</option></select>'
      + '<select id="es"><option value="">All subjects</option></select>'
      + '<span class="muted" id="ecount"></span>'
      + '<a class="badge" href="research/source_ledger.csv" download>Download CSV</a></div>'
      + '<div id="etable"></div>';
    document.getElementById("view").innerHTML = h;

    var subjects = [];
    LEDGER.forEach(function (r) { if (subjects.indexOf(r.subject) < 0) subjects.push(r.subject); });
    var es = document.getElementById("es");
    subjects.forEach(function (s) {
      var o = document.createElement("option"); o.textContent = s; es.appendChild(o);
    });

    function draw() {
      var q = document.getElementById("eq").value.toLowerCase();
      var cf = document.getElementById("ec").value;
      var sf = es.value;
      var list = LEDGER.filter(function (r) {
        if (q && (r.claim + r.value + r.source_name + r.conflict_note).toLowerCase().indexOf(q) < 0) return false;
        if (cf && r.evidence_class.toUpperCase().indexOf(cf) !== 0) return false;
        if (sf && r.subject !== sf) return false;
        return true;
      });
      document.getElementById("ecount").textContent = list.length + " of " + LEDGER.length + " claims";
      document.getElementById("etable").innerHTML =
        '<div class="tablewrap"><table><thead><tr><th>ID</th><th>Subject</th><th>Claim</th>'
        + "<th>Value</th><th>Class</th><th>Conf.</th><th>Source</th><th>Why sources differ</th>"
        + "</tr></thead><tbody>"
        + list.map(function (r) {
          return '<tr><td class="mono">' + r.id + "</td><td>" + r.subject + "</td><td>"
            + esc(r.claim) + '</td><td class="mono" style="font-size:12px">' + esc(r.value)
            + '</td><td><span class="badge ' + classBadge(r.evidence_class) + '">'
            + r.evidence_class + '</span></td><td><span class="badge '
            + (r.confidence === "Low" ? "low" : "") + '">' + r.confidence + "</span></td><td>"
            + (r.source_url && r.source_url.indexOf("http") === 0
              ? '<a href="' + r.source_url + '" rel="noopener">' + esc(r.source_name) + "</a>"
              : esc(r.source_name))
            + '</td><td style="color:var(--ink-3);font-size:12px">' + esc(r.conflict_note)
            + "</td></tr>";
        }).join("")
        + "</tbody></table></div>";
    }
    ["eq", "ec", "es"].forEach(function (id) {
      document.getElementById(id).oninput = draw;
      document.getElementById(id).onchange = draw;
    });
    draw();
  }

  /* ------------------------------------------------------------------- routing */
  function show(key) {
    location.hash = key;
    document.querySelectorAll("#tabs .tab").forEach(function (b) {
      b.className = "tab" + (b.dataset.k === key ? " active" : "");
    });
    if (key === "model") { ECON ? renderModel() : loading(); }
    else if (key === "evidence") { LEDGER ? renderEvidence() : loading(); }
    else document.getElementById("view").innerHTML = renderBlocks(window.HB5[key]);
    window.scrollTo(0, 0);
  }
  function loading() {
    document.getElementById("view").innerHTML = '<div class="panel"><p class="muted">Loading data…</p></div>';
  }

  var tabs = document.getElementById("tabs");
  TABS.forEach(function (t) {
    var b = document.createElement("button");
    b.className = "tab"; b.dataset.k = t[0]; b.textContent = t[1];
    b.onclick = function () { show(t[0]); };
    tabs.appendChild(b);
  });

  var start = (location.hash || "#verdict").slice(1);
  if (!window.HB5[start] && start !== "model" && start !== "evidence") start = "verdict";
  show(start);

  fetch("app/data/economics.json").then(function (r) { return r.json(); }).then(function (d) {
    ECON = d;
    if (location.hash === "#model") renderModel();
  });
  fetch("research/source_ledger.csv").then(function (r) { return r.text(); }).then(function (t) {
    LEDGER = parseCSV(t);
    if (location.hash === "#evidence") renderEvidence();
  });
})();
