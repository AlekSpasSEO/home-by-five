/* Network Performance Dashboard, MaidThis */
(function () {
  var D = null, sortKey = "opportunity_score", sortDir = -1, selected = null;

  var fmt = {
    n: function (v) { return v === null || v === undefined || v === "" ? "–" : Number(v).toLocaleString("en-US"); },
    d1: function (v) { return v === null || v === undefined || v === "" ? "–" : Number(v).toFixed(1); },
    usd: function (v) { return v === null || v === undefined || v === "" ? "–" : "$" + Number(v).toFixed(2); },
    usd0: function (v) { return v === null || v === undefined || v === "" ? "–" : "$" + Math.round(v).toLocaleString("en-US"); }
  };

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  function visible() {
    var q = document.getElementById("q").value.trim().toLowerCase();
    var sf = document.getElementById("statusf").value;
    var gf = document.getElementById("stagef").value;
    return D.markets.filter(function (m) {
      if (q && (m.market + " " + m.city + " " + m.state).toLowerCase().indexOf(q) < 0) return false;
      if (sf === "OPERATING" && m.maps_rank_general === null) return false;
      if (sf === "NOT VISIBLE" && m.maps_rank_general !== null) return false;
      if (gf && m.status !== gf) return false;
      return true;
    });
  }

  function kpis() {
    var m = D.markets;
    var operating = m.filter(function (x) { return x.maps_rank_general !== null; });
    var absent = m.length - operating.length;
    var demand = m.reduce(function (a, x) { return a + (x.total_msv || 0); }, 0);
    var cpcs = m.filter(function (x) { return x.weighted_cpc_usd; }).map(function (x) { return x.weighted_cpc_usd; });
    var avgCpc = cpcs.reduce(function (a, b) { return a + b; }, 0) / (cpcs.length || 1);
    var revs = operating.filter(function (x) { return x.gbp_reviews; }).map(function (x) { return x.gbp_reviews; });
    revs.sort(function (a, b) { return a - b; });
    var medRev = revs.length ? revs[Math.floor(revs.length / 2)] : 0;
    var top3 = operating.filter(function (x) { return x.maps_rank_general <= 3; }).length;

    var tiles = [
      ["Market pages tracked", m.length, "", "URL segments on maidthis.com found in the search index"],
      ["GBP confirmed in pack", operating.length, "accent", "MaidThis profile visible in the top 20 Maps results"],
      ["Not visible in pack", absent, absent > operating.length ? "bad" : "warn", "Page exists, no MaidThis profile found. Each one is a question, not a verdict"],
      ["Top 3 on Maps", top3, top3 >= 10 ? "good" : "warn", "For the head term house cleaning service"],
      ["Network search demand", fmt.n(demand) + "/mo", "", "Ten tracked keywords across all markets, Google Ads volume"],
      ["Mean weighted CPC", "$" + avgCpc.toFixed(2), "", "Average of each market's volume-weighted CPC"],
      ["Median GBP reviews", fmt.n(medRev), "", "Across markets where a MaidThis profile was found"],
      ["Modelled paid CPL", "$" + (avgCpc / 0.10).toFixed(0), "warn", "MODEL: weighted CPC at an assumed 10% click-to-lead rate"]
    ];
    var box = document.getElementById("kpis");
    box.innerHTML = "";
    tiles.forEach(function (t) {
      var s = el("div", "stat");
      s.appendChild(el("div", "k", t[0]));
      s.appendChild(el("div", "v " + (t[2] || ""), typeof t[1] === "number" ? fmt.n(t[1]) : t[1]));
      s.appendChild(el("div", "n", t[3]));
      box.appendChild(s);
    });
  }

  function rows() {
    var list = visible().slice().sort(function (a, b) {
      var x = a[sortKey], y = b[sortKey];
      if (x === null || x === undefined) x = sortDir === 1 ? Infinity : -Infinity;
      if (y === null || y === undefined) y = sortDir === 1 ? Infinity : -Infinity;
      if (typeof x === "string") return sortDir * x.localeCompare(y);
      return sortDir * (x - y);
    });
    var tb = document.getElementById("rows");
    tb.innerHTML = "";
    list.forEach(function (m) {
      var tr = el("tr", "clickable" + (selected === m.slug ? " selected" : ""));
      tr.onclick = function () { selected = m.slug; render(); document.getElementById("detail").scrollIntoView({ behavior: "smooth", block: "start" }); };
      var cells = [
        ["", m.market + (m.market_type === "corporate" ? ' <span class="badge">corp</span>' : "")],
        ["", m.state],
        ["", '<span class="badge ' + m.status.toLowerCase() + '">' + m.status + "</span>"],
        ["num", fmt.d1(m.opportunity_score)],
        ["num", fmt.n(m.total_msv)],
        ["num", fmt.d1(m.str_share_pct)],
        ["num", fmt.usd(m.weighted_cpc_usd)],
        ["num", fmt.usd(m.model_cpl_usd)],
        ["num", m.maps_rank_general === null ? '<span style="color:var(--bad)">none</span>' : m.maps_rank_general],
        ["num", m.maps_rank_str === null ? '<span style="color:var(--ink-3)">none</span>' : m.maps_rank_str],
        ["num", fmt.n(m.gbp_reviews)],
        ["num", fmt.n(m.pack_median_reviews)],
        ["num", fmt.n(m.strong_competitors_20)]
      ];
      cells.forEach(function (c) { tr.appendChild(el("td", c[0], c[1])); });
      tb.appendChild(tr);
    });
    document.getElementById("count").textContent = list.length + " of " + D.markets.length + " markets";
  }

  function detail() {
    var box = document.getElementById("detail");
    if (!selected) {
      box.innerHTML = '<div class="panel tight"><p class="muted" style="margin:0">'
        + "Select a market above to see its keyword table, Maps pack and score breakdown."
        + "</p></div>";
      return;
    }
    var m = D.markets.filter(function (x) { return x.slug === selected; })[0];
    var kws = D.keywords[selected] || [];
    var comps = D.competitors[selected] || [];

    var parts = [
      ["Demand", m.score_demand, "Log-scaled total monthly search volume, so a huge city cannot dominate on size alone"],
      ["Commercial value", m.score_commercial_value, "Volume-weighted CPC, a proxy for what a customer is worth locally"],
      ["Short-term-rental wedge", m.score_str_wedge, "Share of demand that is Airbnb and vacation-rental cleaning, where MaidThis is differentiated"],
      ["Competitive headroom", m.score_competitive_headroom, "Inverse of the median review count of the top 5 Maps competitors"],
      ["Visibility gap", m.score_visibility_gap, "How far MaidThis is from where it should already be ranking"],
      ["Review deficit", m.score_review_deficit, "MaidThis review count against the strongest profile in the pack"]
    ];

    var h = '<div class="panel"><div class="eyebrow">Market detail</div>'
      + '<h2 style="margin-top:0">' + m.market + ", " + m.state
      + ' <span class="badge ' + m.status.toLowerCase() + '">' + m.status + "</span></h2>"
      + '<div class="grid g4" style="margin:14px 0 18px">'
      + tile("Opportunity score", fmt.d1(m.opportunity_score), "accent", "0 to 100, weights below")
      + tile("Maps rank", m.maps_rank_general === null ? "not in top 20" : "#" + m.maps_rank_general, m.maps_rank_general === null ? "bad" : (m.maps_rank_general <= 3 ? "good" : "warn"), "house cleaning service")
      + tile("GBP rating", m.gbp_rating ? m.gbp_rating + " ★" : "–", "", fmt.n(m.gbp_reviews) + " reviews")
      + tile("Organic rank", m.organic_rank_city_term ? "#" + m.organic_rank_city_term : "not in top 20", m.organic_rank_city_term ? "" : "warn", "house cleaning services " + m.city.toLowerCase())
      + "</div>"

      + '<div class="grid g2">'
      + '<div><h3 style="margin-top:0">Score breakdown</h3>'
      + parts.map(function (p) {
        return '<div class="scorebar" title="' + p[2] + '"><span class="lab">' + p[0]
          + '</span><span class="bar"><i style="width:' + p[1] + '%"></i></span>'
          + '<span class="val">' + fmt.d1(p[1]) + "</span></div>";
      }).join("")
      + '<div class="grid g2" style="margin-top:12px">'
      + tile("Potential", fmt.d1(m.score_potential), "", "demand x (0.60 + 0.25 commercial + 0.15 STR)")
      + tile("Headroom", fmt.d1(m.score_headroom), "", "0.40 competitive + 0.45 visibility + 0.15 review")
      + "</div>"
      + '<p class="muted" style="margin-top:10px">Opportunity = potential x headroom, so a market '
      + "with almost no search demand cannot score highly just because MaidThis is invisible in it, "
      + "and a market already won scores low too. Uncaptured demand here: "
      + fmt.n(m.uncaptured_msv) + " searches a month.</p></div>"

      + '<div><h3 style="margin-top:0">Search demand</h3><div class="tablewrap"><table>'
      + "<thead><tr><th>Keyword</th><th class=num>Vol/mo</th><th class=num>CPC</th><th>Comp.</th></tr></thead><tbody>"
      + kws.sort(function (a, b) { return (b.volume || 0) - (a.volume || 0); }).map(function (k) {
        return "<tr><td>" + k.keyword + '</td><td class="num">' + fmt.n(k.volume)
          + '</td><td class="num">' + fmt.usd(k.cpc) + "</td><td>" + (k.competition || "–") + "</td></tr>";
      }).join("")
      + "</tbody></table></div></div></div>"

      + '<h3>Google Maps pack, house cleaning service</h3><div class="tablewrap"><table>'
      + "<thead><tr><th class=num>#</th><th>Business</th><th class=num>Rating</th><th class=num>Reviews</th><th>Category</th></tr></thead><tbody>"
      + comps.map(function (c) {
        return '<tr' + (c.is_maidthis ? ' class="selected"' : "") + '><td class="num">' + c.rank
          + "</td><td>" + (c.is_maidthis ? "<b>" + c.name + "</b>" : c.name)
          + '</td><td class="num">' + (c.rating || "–") + '</td><td class="num">' + fmt.n(c.reviews)
          + "</td><td>" + (c.category || "–") + "</td></tr>";
      }).join("")
      + "</tbody></table></div>"
      + '<p class="muted" style="margin-top:10px">Consumer page: <a href="https://maidthis.com/'
      + m.slug + '/">maidthis.com/' + m.slug + "/</a>. SERP features present on the organic result: "
      + (m.serp_item_types || "none recorded") + ".</p>"
      + "</div>";
    box.innerHTML = h;
  }

  function tile(k, v, cls, n) {
    return '<div class="stat"><div class="k">' + k + '</div><div class="v ' + (cls || "") + '">'
      + v + '</div><div class="n">' + (n || "") + "</div></div>";
  }

  function render() { kpis(); rows(); detail(); }

  fetch("../app/data/markets.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (d) {
    D = d;
    document.querySelectorAll("th.sortable").forEach(function (th) {
      th.onclick = function () {
        var k = th.dataset.k;
        if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = -1; }
        document.querySelectorAll("th.sortable").forEach(function (o) {
          o.innerHTML = o.innerHTML.replace(/\s*<span class="arrow">.*<\/span>/, "");
        });
        th.innerHTML += ' <span class="arrow">' + (sortDir === 1 ? "▲" : "▼") + "</span>";
        rows();
      };
    });
    ["q", "statusf", "stagef"].forEach(function (id) {
      document.getElementById(id).oninput = function () { rows(); };
      document.getElementById(id).onchange = function () { rows(); };
    });
    render();
  }).catch(function (e) {
    document.getElementById("rows").innerHTML =
      '<tr><td colspan="13">Could not load app/data/markets.json (' + e + ")</td></tr>";
  });
})();
