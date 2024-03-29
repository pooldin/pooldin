var PI, campaign,
  __slice = [].slice,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

PI = window.PI = window.PI || {};

ko.extenders.money = function(target, opts) {
  if (opts == null) {
    opts = {};
  }
  return ko.computed({
    read: function() {
      var number;
      number = target();
      if (!((number != null) && !isNaN(number))) {
        return;
      }
      return accounting.formatMoney(number, opts);
    },
    write: function(value) {
      var current;
      current = target();
      if (value !== current) {
        return target(value);
      }
    }
  });
};

ko.extenders.number = function(target, opts) {
  if (opts == null) {
    opts = {};
  }
  return ko.computed({
    read: function() {
      var number;
      number = target();
      if (!((number != null) && !isNaN(number))) {
        return;
      }
      return accounting.formatMoney(number, opts);
    },
    write: function(value) {
      var current;
      current = target();
      if (value !== current) {
        return target(value);
      }
    }
  });
};

PI.Schema = (function() {

  function Schema(cls, mapping) {
    if (!jQuery.isFunction(cls)) {
      mapping = cls;
      cls = void 0;
    }
    this.model = cls;
    this.mapping = mapping != null ? mapping : {};
  }

  Schema.prototype.key = function(key, callback) {
    var _base, _ref;
    if (key && callback) {
      if ((_ref = (_base = this.mapping)[key]) == null) {
        _base[key] = {};
      }
      this.mapping[key].key = callback;
    }
    return this;
  };

  Schema.prototype.map = function(key, callback) {
    var _base, _ref;
    if (key && callback) {
      if ((_ref = (_base = this.mapping)[key]) == null) {
        _base[key] = {};
      }
      this.mapping[key].create = callback;
      this.mapping[key].update = callback;
    }
    return this;
  };

  Schema.prototype.mapMoment = function() {
    var key, keys, _i, _len, _results;
    keys = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    _results = [];
    for (_i = 0, _len = keys.length; _i < _len; _i++) {
      key = keys[_i];
      _results.push(this.map(key, function(context) {
        var m;
        m = moment(context.data);
        if (context.observable) {
          return m;
        }
        return ko.observable(m);
      }));
    }
    return _results;
  };

  Schema.prototype.update = function(key, callback) {
    var _base, _ref;
    if (key && callback) {
      if ((_ref = (_base = this.mapping)[key]) == null) {
        _base[key] = {};
      }
      this.mapping[key].update = callback;
    }
    return this;
  };

  Schema.prototype.addList = function() {
    var arg, args, key, _base, _i, _len, _ref;
    key = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
    if (!(args.length > 0)) {
      return this;
    }
    if ((_ref = (_base = this.mapping)[key]) == null) {
      _base[key] = [];
    }
    for (_i = 0, _len = args.length; _i < _len; _i++) {
      arg = args[_i];
      if (jQuery.isArray(arg)) {
        arg = arg.slice();
        arg.unshift(key);
        this.addList.apply(this, arg);
      } else {
        this.mapping[key].push(arg);
      }
    }
    if (this.mapping[key].length < 1) {
      delete this.mapping[key];
    }
    return this;
  };

  Schema.prototype.ignore = function() {
    var args;
    args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    args.unshift('ignore');
    this.addList.apply(this, args);
    return this;
  };

  Schema.prototype.include = function() {
    var args;
    args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    args.unshift('include');
    this.addList.apply(this, args);
    return this;
  };

  Schema.prototype.copy = function() {
    var args;
    args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    args.unshift('copy');
    this.addList.apply(this, args);
    return this;
  };

  Schema.prototype.load = function(data, viewModel) {
    if (!viewModel && this.model) {
      viewModel = this.model();
    }
    if (!viewModel) {
      return ko.mapping.fromJS(data, this.mapping);
    }
    ko.mapping.fromJS(data, this.mapping, viewModel);
    return viewModel;
  };

  Schema.prototype.dump = function(viewModel) {
    if (viewModel) {
      return ko.mapping.toJS(viewModel);
    }
  };

  return Schema;

})();

PI.schema = new PI.Schema();

PI.Model = (function() {

  Model.load = function(data) {
    return new this(data);
  };

  function Model(data) {
    var _ref;
    this.schema = (_ref = this.constructor.schema) != null ? _ref : PI.schema;
    this.schema.load(data, this);
  }

  Model.prototype.update = function(data) {
    this.schema.load(data, this);
    return this;
  };

  Model.prototype.dump = function() {
    return this.schema.dump(this);
  };

  Model.prototype.toJSON = function() {
    return ko.toJSON(this.schema.dump(this));
  };

  return Model;

})();

PI.Page = (function() {

  Page.init = function(opts) {
    var page;
    page = PI.page = new this(opts);
    page.render();
    return page;
  };

  function Page(opts) {
    if (opts == null) {
      opts = {};
    }
  }

  Page.prototype.render = function() {
    ko.applyBindings(this);
    return this;
  };

  return Page;

})();

PI.Modal = (function() {

  function Modal() {
    this.submit = __bind(this.submit, this);

    this.cancel = __bind(this.cancel, this);

    this.open = __bind(this.open, this);

    this.toggle = __bind(this.toggle, this);
    this.visible = ko.observable(false);
    this.el = this.getElement();
    this.visible.subscribe(this.onVisible, this);
  }

  Modal.prototype.show = function() {
    return this.visible(true);
  };

  Modal.prototype.hide = function() {
    return this.visible(false);
  };

  Modal.prototype.toggle = function() {
    return this.visible(!this.visible());
  };

  Modal.prototype.open = function() {
    this.reset();
    return this.show();
  };

  Modal.prototype.cancel = function() {
    this.reset();
    return this.hide();
  };

  Modal.prototype.submit = function() {};

  Modal.prototype.reset = function() {};

  Modal.prototype.onVisible = function(visible) {
    if (visible) {
      this.el.modal('show');
    }
    if (!visible) {
      return this.el.modal('hide');
    }
  };

  return Modal;

})();

PI.UploadModal = (function(_super) {

  __extends(UploadModal, _super);

  function UploadModal() {
    return UploadModal.__super__.constructor.apply(this, arguments);
  }

  UploadModal.prototype.getElement = function() {
    return jQuery('#uploader').modal({
      show: false,
      backdrop: 'static',
      keyboard: true
    });
  };

  return UploadModal;

})(PI.Modal);

PI.UserProfile = (function(_super) {

  __extends(UserProfile, _super);

  function UserProfile(user, opts) {
    this.opts = opts != null ? opts : {};
    this.publicLabel = ko.observable('public');
    this.isPublic = ko.observable(true);
    this.profile = new PI.UserProfileForm(user);
  }

  UserProfile.prototype.setPublic = function() {
    var publicLabel;
    this.isPublic(!this.isPublic());
    if (this.isPublic()) {
      publicLabel = 'public';
    }
    if (!this.isPublic()) {
      publicLabel = 'private';
    }
    return this.publicLabel(publicLabel);
  };

  return UserProfile;

})(PI.Page);

PI.UserProfileForm = (function(_super) {

  __extends(UserProfileForm, _super);

  function UserProfileForm(user) {
    this.onError = __bind(this.onError, this);

    this.onSuccess = __bind(this.onSuccess, this);

    this.save = __bind(this.save, this);

    this.cancel = __bind(this.cancel, this);

    this.toggleEdit = __bind(this.toggleEdit, this);
    UserProfileForm.__super__.constructor.call(this, user);
    this.isEditing = ko.observable(false);
  }

  UserProfileForm.prototype.toggleEdit = function() {
    this.isEditing(!this.isEditing());
    if (this.isEditing) {
      return jQuery('.about-text').focus();
    }
  };

  UserProfileForm.prototype.cancel = function() {
    var text;
    text = this.about();
    jQuery('.about-text').text(text);
    return this.toggleEdit();
  };

  UserProfileForm.prototype.save = function() {
    var text, toSave;
    text = jQuery.trim(jQuery('.about-text').text());
    toSave = this.dump();
    toSave.about = text;
    jQuery.post("/user/" + (this.username()) + "/about", toSave, void 0, 'json').done(this.onSuccess).fail(this.onError);
    return this.toggleEdit();
  };

  UserProfileForm.prototype.onSuccess = function(data) {
    var opts;
    this.update(data);
    opts = {
      keyboard: true,
      backdrop: false
    };
    return jQuery('#user-update-success').modal(opts);
  };

  UserProfileForm.prototype.onError = function() {
    var opts;
    opts = {
      keyboard: true,
      backdrop: false
    };
    return jQuery('#user-update-error').modal(opts);
  };

  return UserProfileForm;

})(PI.Model);

campaign = new PI.Schema();

campaign.mapMoment('started', 'deadline');

PI.CampaignTarget = (function(_super) {

  __extends(CampaignTarget, _super);

  function CampaignTarget(data) {
    CampaignTarget.__super__.constructor.call(this, data);
    this.valueUI = ko.computed(this.getValueUI, this);
  }

  CampaignTarget.prototype.getValueUI = function() {
    var type, value;
    type = typeof this.type === "function" ? this.type() : void 0;
    value = typeof this.value === "function" ? this.value() : void 0;
    if (type === 'money') {
      return accounting.formatMoney(value, {
        precision: 0
      });
    }
    if (type === 'number') {
      value = accounting.formatNumber(value, {
        precision: 0
      });
      if (value != null) {
        return value + " Poold in";
      }
      return value;
    }
  };

  return CampaignTarget;

})(PI.Model);

PI.Campaign = (function(_super) {

  __extends(Campaign, _super);

  Campaign.schema = campaign;

  function Campaign(data) {
    var target;
    if (data == null) {
      data = {};
    }
    target = this.extractTarget(data);
    Campaign.__super__.constructor.call(this, data);
    this.days = ko.observable();
    this.hours = ko.observable();
    this.minutes = ko.observable();
    this.seconds = ko.observable();
    this.remaining = ko.observable();
    this.deadline.subscribe(this.refreshTimes, this);
    this.refreshTimes();
    if (target) {
      this.target = ko.observable(target);
    }
    if (!target) {
      this.target = ko.observable();
    }
    this.balanceUI = this.balance.extend({
      money: {
        precision: 0
      }
    });
    this.progress = ko.computed(this.getProgress, this);
    this.progressUI = this.progress.extend({
      number: {
        precision: 0,
        format: '%v%'
      }
    });
  }

  Campaign.prototype.extractTarget = function(data) {
    var has, target, _ref, _ref1;
    if (data == null) {
      data = {};
    }
    has = data.target === null;
    target = data.target;
    delete data.target;
    if (data.target_type) {
      if (target == null) {
        target = {};
      }
      if ((_ref = target.type) == null) {
        target.type = data.target_type;
      }
      delete data.target_type;
    }
    if (data.target_value) {
      if (target == null) {
        target = {};
      }
      if ((_ref1 = target.value) == null) {
        target.value = data.target_value;
      }
      delete data.target_value;
    }
    if (has && !target) {
      return null;
    }
    if (!target) {
      return void 0;
    }
    return PI.CampaignTarget.load(target);
  };

  Campaign.prototype.update = function(data) {
    var target;
    target = this.extractTarget(data);
    Campaign.__super__.update.call(this, data);
    if (target || target === null) {
      this.target(target);
    }
    return this;
  };

  Campaign.prototype.getProgress = function() {
    var field, type, value, _ref, _ref1;
    type = (_ref = this.target()) != null ? typeof _ref.type === "function" ? _ref.type() : void 0 : void 0;
    value = (_ref1 = this.target()) != null ? typeof _ref1.value === "function" ? _ref1.value() : void 0 : void 0;
    if (type === 'money') {
      field = this.balance();
    }
    if (type !== 'money') {
      field = this.participants();
    }
    if (!(field != null) || isNaN(field) || field < 0) {
      return 0;
    }
    if (!(value != null) || isNaN(value)) {
      return 0;
    }
    return Math.min((field / value) * 100, 100);
  };

  Campaign.prototype.refreshTimes = function(deadline) {
    var diff, duration;
    if (deadline == null) {
      deadline = this.deadline();
    }
    diff = deadline.diff();
    duration = moment.duration(diff);
    this.days(Math.round(duration.asDays()));
    this.hours(Math.round(duration.hours()));
    this.minutes(Math.round(duration.minutes()));
    this.seconds(Math.round(duration.seconds()));
    return this.remaining(Math.round(duration.asSeconds()));
  };

  return Campaign;

})(PI.Model);

PI.CampaignCreate = (function(_super) {

  __extends(CampaignCreate, _super);

  function CampaignCreate(opts) {
    this.opts = opts != null ? opts : {};
    this.uploader = new PI.UploadModal();
    this.campaignType = ko.observable();
    this.campaignType.subscribe(this.onCampaignType, this);
    this.requiredAmount = ko.observable();
    this.paymentAmountType = ko.observable();
    this.paymentAmountType.subscribe(this.onPaymentAmountType, this);
    this.campaignContract = ko.observable(false);
    this.amazonPurchase = ko.observable(false);
    this.typeDependentVisible = ko.observable(false);
    this.paymentTypeDependentVisible = ko.observable(false);
  }

  CampaignCreate.prototype.onCampaignType = function(type) {
    var visible;
    visible = type === 'co-own' || type === 'gift';
    return this.toggleTypeDependents(visible);
  };

  CampaignCreate.prototype.onPaymentAmountType = function(type) {
    var visible;
    visible = type === 'specific';
    return this.togglePaymentTypeDependents(visible);
  };

  CampaignCreate.prototype.toggleTypeDependents = function(visible) {
    this.typeDependentVisible(visible);
    if (!visible) {
      return this.campaignContract(visible);
    }
  };

  CampaignCreate.prototype.togglePaymentTypeDependents = function(visible) {
    this.paymentTypeDependentVisible(visible);
    return this.requiredAmount(0);
  };

  return CampaignCreate;

})(PI.Page);

PI.CampaignDetails = (function(_super) {

  __extends(CampaignDetails, _super);

  function CampaignDetails(campaign) {
    this.campaign = ko.observable(campaign);
    this.progress = ko.computed(this.getProgress, this);
    this.progress.subscribe(this.renderPie, this);
    this.remaining = ko.computed(this.getRemaining, this);
    this.deadlineUI = ko.computed(this.getDeadlineUI, this);
    this.daysUI = ko.computed(this.getDaysUI, this);
    this.hoursUI = ko.computed(this.getHoursUI, this);
    this.minutesUI = ko.computed(this.getMinutesUI, this);
    this.secondsUI = ko.computed(this.getSecondsUI, this);
    this.remaining.subscribe(this.onRefreshRemaining, this);
    this.onRefreshRemaining(this.remaining());
    this.uploader = new PI.UploadModal();
    this.manager = new PI.CampaignManager(this.uploader);
    this.promote = new PI.CampaignPromote();
    this.disburse = new PI.CampaignDisburse();
    this.payment = new PI.PaymentModal(this);
  }

  CampaignDetails.prototype.getProgress = function() {
    return this.campaign().progress();
  };

  CampaignDetails.prototype.getDeadlineUI = function() {
    var day, deadline, month, year;
    deadline = this.campaign().deadline();
    month = deadline.format('MMM').toUpperCase();
    day = deadline.format('Do');
    year = deadline.format('YYYY');
    return "" + month + " " + day + " " + year;
  };

  CampaignDetails.prototype.getDaysUI = function() {
    var days;
    days = this.campaign().days();
    if (days === 1) {
      return days + ' day';
    }
    return days + ' days';
  };

  CampaignDetails.prototype.getHoursUI = function() {
    var hours;
    hours = this.campaign().hours();
    if (hours === 1) {
      return hours + ' hour';
    }
    return hours + ' hours';
  };

  CampaignDetails.prototype.getMinutesUI = function() {
    var mins;
    mins = this.campaign().minutes();
    if (mins === 1) {
      return mins + ' min';
    }
    return mins + ' mins';
  };

  CampaignDetails.prototype.getSecondsUI = function() {
    var secs;
    secs = this.remaining();
    if (secs > 9) {
      return ':' + secs;
    }
    return ':0' + secs;
  };

  CampaignDetails.prototype.getRemaining = function() {
    return this.campaign().remaining();
  };

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

  CampaignDetails.prototype.render = function() {
    CampaignDetails.__super__.render.call(this);
    this.renderGraph('#pie-chart');
    return this;
  };

  CampaignDetails.prototype.renderGraph = function(el, width, height, x, y, r) {
    var graph;
    el = jQuery(el);
    if (width == null) {
      width = 200;
    }
    if (height == null) {
      height = 200;
    }
    if (x == null) {
      x = 100;
    }
    if (y == null) {
      y = 100;
    }
    if (r == null) {
      r = 100;
    }
    if (!(el && el.length > 0)) {
      return;
    }
    graph = Raphael(el[0], 200, 200);
    return this.renderPie(this.progress(), graph, x, y, r);
  };

  CampaignDetails.prototype.renderPie = function(total, graph, x, y, r) {
    var pie, pieChart;
    if (graph == null) {
      graph = this.graph;
    }
    if (!graph) {
      return;
    }
    graph.clear();
    pie = this.pieData(total);
    pieChart = graph.piechart(x, y, r, pie.data, {
      init: 0.1,
      colors: pie.colors
    });
    if (pie.rotation) {
      pieChart.rotate(pie.rotation);
    }
    graph.circle(x, y, r * 0.98).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur();
    graph.circle(x, y, r * 0.99).animate({
      stroke: "#aaa",
      "stroke-width": 1
    });
    graph.circle(x, y, r * 0.70).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    });
    graph.circle(x, y, r * 0.72).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur();
    graph.circle(x, y, r * 0.70).animate({
      stroke: "#aaa",
      "stroke-width": 1,
      fill: "#fff"
    });
    return this;
  };

  CampaignDetails.prototype.delayRefresh = function(ms) {
    var delay,
      _this = this;
    if (this.timeout) {
      clearTimeout(this.timeout);
    }
    delay = function() {
      if (_this.timeout) {
        clearTimeout(_this.timeout);
      }
      return _this.campaign().refreshTimes();
    };
    return this.timeout = setTimeout(delay, ms);
  };

  CampaignDetails.prototype.onRefreshRemaining = function(remaining) {
    var factor;
    if (remaining <= 0) {
      return;
    }
    factor = 60;
    if (remaining < 61) {
      factor = 1;
    }
    return this.delayRefresh(1000 * factor);
  };

  return CampaignDetails;

})(PI.Page);

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

PI.PaymentModal = (function(_super) {

  __extends(PaymentModal, _super);

  function PaymentModal(page) {
    this.resetModal = __bind(this.resetModal, this);

    this.finishAndCreate = __bind(this.finishAndCreate, this);

    this.finish = __bind(this.finish, this);

    this.paymentCallback = __bind(this.paymentCallback, this);

    this.submitPayment = __bind(this.submitPayment, this);
    PaymentModal.__super__.constructor.call(this);
    this.page = page;
    this.loginPage = ko.observable(logInUser());
    this.formPage = ko.observable(!this.loginPage());
    this.processingPage = ko.observable(false);
    this.successPage = ko.observable(false);
    this.form = new PI.PaymentForm();
  }

  PaymentModal.prototype.getElement = function() {
    return jQuery('#payment').modal({
      show: false,
      backdrop: 'static',
      keyboard: true
    });
  };

  PaymentModal.prototype.open = function() {
    PaymentModal.__super__.open.call(this);
    if (this.page.renderedPaymentModal) {
      return;
    }
    this.page.renderGraph('#modal-pie-chart-login', 150, 150, 75, 75, 75);
    this.page.renderGraph('#modal-pie-chart-success', 150, 150, 75, 75, 75);
    this.page.renderGraph('#modal-pie-chart', 150, 150, 75, 75, 75);
    return this.page.renderedPaymentModal = true;
  };

  PaymentModal.prototype.submitPayment = function() {
    var el;
    if (!this.form.valid()) {
      this.displayErrors();
    }
    this.processingPage(true);
    el = jQuery('.processing-spinner')[0];
    this.spinner = this.buildSpinner();
    this.spinner.spin();
    el.appendChild(this.spinner.el);
    return setTimeout(this.paymentCallback, 2500);
  };

  PaymentModal.prototype.paymentCallback = function(data) {
    return this.paymentSuccess();
  };

  PaymentModal.prototype.paymentSuccess = function() {
    this.spinner.stop();
    this.processingPage(false);
    this.formPage(false);
    return this.successPage(true);
  };

  PaymentModal.prototype.displayErrors = function() {};

  PaymentModal.prototype.buildSpinner = function() {
    var opts;
    opts = {
      lines: 8,
      length: 7,
      width: 5,
      radius: 10,
      corners: 1,
      rotate: 0,
      color: "#FFF",
      speed: 1,
      trail: 60,
      shadow: false,
      hwaccel: false,
      className: "spinner"
    };
    return Spinner(opts);
  };

  PaymentModal.prototype.finish = function() {
    this.cancel();
    return setTimeout(this.resetModal, 1000);
  };

  PaymentModal.prototype.finishAndCreate = function() {
    var createCampaign;
    this.finish();
    createCampaign = function() {
      return window.location = '/campaign/new';
    };
    return setTimeout(createCampaign, 1000);
  };

  PaymentModal.prototype.resetModal = function() {
    this.form.paymentAmount("$0.00");
    this.successPage(false);
    return this.formPage(true);
  };

  return PaymentModal;

})(PI.Modal);

PI.PaymentForm = (function(_super) {

  __extends(PaymentForm, _super);

  function PaymentForm() {
    this.paymentAmount = ko.observable("$0.00");
    this.firstName = ko.observable();
    this.lastName = ko.observable();
    this.address = ko.observable();
    this.city = ko.observable();
    this.state = ko.observable();
    this.country = ko.observable();
    this.postalCode = ko.observable();
    this.ccNumber = ko.observable();
    this.ccvNumber = ko.observable();
    this.expirationMonth = ko.observable();
    this.expirationYear = ko.observable();
  }

  PaymentForm.prototype.valid = function() {
    return true;
  };

  return PaymentForm;

})(PI.Model);
