var PI,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

PI = window.PI = window.PI || {};

PI.Uploader = (function() {

  function Uploader() {
    this.cancel = __bind(this.cancel, this);

    this.open = __bind(this.open, this);
    this.visible = ko.observable(false);
    this.el = jQuery('#uploader').modal({
      show: false,
      backdrop: 'static',
      keyboard: true
    });
    this.visible.subscribe(this.onVisible, this);
  }

  Uploader.prototype.show = function() {
    return this.visible(true);
  };

  Uploader.prototype.hide = function() {
    return this.visible(false);
  };

  Uploader.prototype.toggle = function() {
    return this.visible(!this.visible());
  };

  Uploader.prototype.open = function() {
    this.reset();
    return this.show();
  };

  Uploader.prototype.cancel = function() {
    this.reset();
    return this.hide();
  };

  Uploader.prototype.reset = function() {};

  Uploader.prototype.submit = function() {};

  Uploader.prototype.onVisible = function(visible) {
    if (visible) {
      this.el.modal('show');
    }
    if (!visible) {
      return this.el.modal('hide');
    }
  };

  return Uploader;

})();

PI.CampaignCreate = (function() {

  CampaignCreate.render = function(opts) {
    var page;
    page = new this(opts);
    page.render();
    ko.applyBindings(page);
    return page;
  };

  function CampaignCreate(opts) {
    if (opts == null) {
      opts = {};
    }
    this.uploader = new PI.Uploader();
  }

  CampaignCreate.prototype.render = function() {};

  return CampaignCreate;

})();

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
    this.uploader = new PI.Uploader();
    this.manager = new PI.CampaignManager(this.uploader);
    this.promote = new PI.CampaignPromote();
    this.disburse = new PI.CampaignDisburse();
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

PI.CampaignManager = (function() {

  function CampaignManager(uploader) {
    var _this = this;
    this.uploader = uploader;
    this.tab = ko.observable();
    this.tab.subscribe(this.onTab, this);
    this.navigate(location.hash);
    this.visible = ko.observable(!!this.tab());
    jQuery('.nav-tabs.manage a[data-toggle="tab"]').on('shown', function(e) {
      return _this.navigate(jQuery(e != null ? e.target : void 0).attr('href'));
    });
  }

  CampaignManager.prototype.show = function() {
    return this.visible(true);
  };

  CampaignManager.prototype.hide = function() {
    return this.visible(false);
  };

  CampaignManager.prototype.toggle = function() {
    return this.visible(!this.visible());
  };

  CampaignManager.prototype.navigate = function(tab) {
    tab = (tab != null ? tab : '').replace(/^#/g, '');
    if (tab === 'manage' || tab === 'promote' || tab === 'disburse') {
      this.tab(tab);
    }
    return this;
  };

  CampaignManager.prototype.onTab = function() {
    var tab;
    tab = this.tab();
    if (!tab) {
      return;
    }
    return jQuery(".nav-tabs li a[href=#" + tab + "]").tab('show');
  };

  CampaignManager.prototype.cancel = function() {
    this.reset();
    return this.hide();
  };

  CampaignManager.prototype.reset = function() {};

  CampaignManager.prototype.submit = function() {};

  return CampaignManager;

})();

PI.CampaignPromote = (function() {

  function CampaignPromote() {}

  CampaignPromote.prototype.cancel = function() {
    this.reset();
    return this.hide();
  };

  CampaignPromote.prototype.reset = function() {};

  CampaignPromote.prototype.submit = function() {};

  return CampaignPromote;

})();

PI.CampaignDisburse = (function() {

  function CampaignDisburse() {}

  CampaignDisburse.prototype.cancel = function() {
    this.reset();
    return this.hide();
  };

  CampaignDisburse.prototype.reset = function() {};

  CampaignDisburse.prototype.submit = function() {};

  return CampaignDisburse;

})();
