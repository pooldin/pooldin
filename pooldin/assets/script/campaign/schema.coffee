campaign = new PI.Schema()
campaign.mapMoment('started', 'deadline')


class PI.CampaignTarget extends PI.Model
  constructor: (data) ->
    super(data)
    @valueUI = ko.computed(@getValueUI, this)

  getValueUI: ->
    type = @type?()
    value = @value?()

    if type is 'money'
      return accounting.formatMoney(value, precision: 0)

    if type is 'number'
      value = accounting.formatNumber(value, precision: 0)
      return value + " Poold in" if value?
      return value


class PI.Campaign extends PI.Model

  @schema: campaign

  constructor: (data) ->
    data ?= {}
    target = @extractTarget(data)
    super(data)

    @days = ko.observable()
    @hours = ko.observable()
    @minutes = ko.observable()
    @seconds = ko.observable()
    @remaining = ko.observable()
    @deadline.subscribe(@refreshTimes, this)
    @refreshTimes()

    @target = ko.observable(target) if target
    @target = ko.observable() unless target

    @balanceUI = @balance.extend(money: precision: 0)

    @progress = ko.computed(@getProgress, this)
    @progressUI = @progress.extend(number: precision: 0, format: '%v%')

  extractTarget: (data) ->
    data ?= {}

    has = data.target is null
    target = data.target
    delete data.target

    if data.target_type
      target ?= {}
      target.type ?= data.target_type
      delete data.target_type

    if data.target_value
      target ?= {}
      target.value ?= data.target_value
      delete data.target_value

    return null if has and not target
    return undefined unless target
    return PI.CampaignTarget.load(target)

  update: (data) ->
    target = @extractTarget(data)
    super(data)
    @target(target) if target or target is null
    return this

  getProgress: ->
    type = @target()?.type?()
    value = @target()?.value?()

    field = @balance() if type is 'money'
    field = @participants() unless type is 'money'

    return 0 if not field? or isNaN(field) or field < 0
    return 0 if not value? or isNaN(value)
    return Math.min((field / value) * 100, 100)

  refreshTimes: (deadline) ->
    deadline ?= @deadline()
    diff = deadline.diff()
    duration = moment.duration(diff)
    @days(Math.round(duration.asDays()))
    @hours(Math.round(duration.hours()))
    @minutes(Math.round(duration.minutes()))
    @seconds(Math.round(duration.seconds()))
    @remaining(Math.round(duration.asSeconds()))
