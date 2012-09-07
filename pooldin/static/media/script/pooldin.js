var PI;

PI = window.PI = window.PI || {};

PI.CampaignDetails = (function() {

  CampaignDetails.render = function(opts) {
    var page;
    page = new this(opts);
    page.render();
    ko.applyBindings(page);
    return page;
  };

  function CampaignDetails(opts) {
    if (opts == null) {
      opts = {};
    }
    this.total = ko.observable(opts.total);
    this.total.subscribe(this.render_pie, this);
  }

  CampaignDetails.prototype.pieData = function(total) {
    var colors, data, remaining, rotation;
    if (!(total && total > 0)) {
      total = 0;
    }
    if (total > 100) {
      total = 100;
    }
    remaining = 100 - total;
    rotation = 0;
    if (total < 100) {
      if (total <= 50) {
        rotation = -180 * (remaining / 100);
      }
      if (total > 50) {
        rotation = 180 * (total / 100);
      }
    }
    colors = ['#739b9e', '#fff'];
    if (total <= 50) {
      colors.reverse();
    }
    if (total >= 100) {
      colors = ['#739b9e'];
    }
    if (total >= 100) {
      data = [100];
    }
    if (total < 100) {
      data = [total, remaining];
    }
    return {
      total: total,
      remaining: remaining,
      rotation: rotation,
      data: data,
      colors: colors
    };
  };

  CampaignDetails.prototype.render = function(opts) {
    var el, total;
    if (opts == null) {
      opts = {};
    }
    el = opts.el || jQuery('#pie-chart');
    total = opts.total || this.total();
    if (!(el && el.length > 0)) {
      return;
    }
    this.el = el;
    this.graph = Raphael(this.el[0], 200, 200);
    this.render_pie(total);
    return this;
  };

  CampaignDetails.prototype.render_pie = function(total) {
    var pie;
    if (!this.graph) {
      return;
    }
    this.graph.clear();
    pie = this.pieData(total);
    this.pie = this.graph.piechart(100, 100, 100, pie.data, {
      init: 0.1,
      colors: pie.colors
    });
    if (pie.rotation) {
      this.pie.rotate(pie.rotation);
    }
    this.graph.circle(100, 100, 98).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur();
    this.graph.circle(100, 100, 99).animate({
      stroke: "#aaa",
      "stroke-width": 1
    });
    this.graph.circle(100, 100, 70).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    });
    this.graph.circle(100, 100, 72).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur();
    this.graph.circle(100, 100, 70).animate({
      stroke: "#aaa",
      "stroke-width": 1,
      fill: "#fff"
    });
    return this;
  };

  return CampaignDetails;

})();
