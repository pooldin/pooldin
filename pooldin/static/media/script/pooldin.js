var PI;

PI = window.PI = window.PI || {};

PI.CampaignDetails = (function() {

  function CampaignDetails() {}

  CampaignDetails.render = function() {
    var page;
    page = new this();
    page.render();
    return page;
  };

  CampaignDetails.prototype.render = function() {
    var chart, pie, total;
    this.el = jQuery('#pie-chart');
    this.graph = Raphael("pie-chart", 200, 200);
    total = 88;
    pie = this.pieData(total);
    chart = this.graph.piechart(100, 100, 100, pie.data, {
      init: 0.1,
      colors: pie.colors
    });
    if (pie.rotation) {
      chart.rotate(pie.rotation);
    }
    return this;
  };

  CampaignDetails.prototype.pieData = function(total) {
    var colors, data, remaining, rotation;
    if (total < 0) {
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

  return CampaignDetails;

})();
