class PI.CampaignDetails extends PI.Page

  constructor: (campaign) ->
    @campaign = ko.observable(campaign)
    @progress = ko.computed(@getProgress, this)
    @progress.subscribe(@renderPie, this)

    @remaining = ko.computed(@getRemaining, this)
    @deadlineUI = ko.computed(@getDeadlineUI, this)
    @daysUI = ko.computed(@getDaysUI, this)
    @hoursUI = ko.computed(@getHoursUI, this)
    @minutesUI = ko.computed(@getMinutesUI, this)
    @secondsUI = ko.computed(@getSecondsUI, this)
    @remaining.subscribe(@onRefreshRemaining, this)
    @onRefreshRemaining(@remaining())

    @uploader = new PI.UploadModal()
    @manager = new PI.CampaignManager(@uploader)
    @promote = new PI.CampaignPromote()
    @disburse = new PI.CampaignDisburse()
    @payment = new PI.PaymentModal(this)

  getProgress: ->
    return @campaign().progress()

  getDeadlineUI: ->
    deadline = @campaign().deadline()
    month = deadline.format('MMM').toUpperCase()
    day = deadline.format('Do')
    year = deadline.format('YYYY')
    return "#{month} #{day} #{year}"

  getDaysUI: ->
    days = @campaign().days()
    return days + ' day' if days is 1
    return days + ' days'

  getHoursUI: ->
    hours = @campaign().hours()
    return hours + ' hour' if hours is 1
    return hours + ' hours'

  getMinutesUI: ->
    mins = @campaign().minutes()
    return mins + ' min' if mins is 1
    return mins + ' mins'

  getSecondsUI: ->
    secs = @remaining()
    return ':' + secs if secs > 9
    return ':0' + secs

  getRemaining: ->
    return @campaign().remaining()

  pieData: (total) ->
    total = 0 unless total and total > 0
    total = 100 if total > 100

    remaining = 100 - total

    rotation = 0

    if total < 100
      rotation = -180 * (remaining / 100) if total <= 50
      rotation = 180 * (total / 100) if total > 50

    colors = ['#739b9e', '#fff']
    colors.reverse() if total <= 50
    colors = ['#739b9e'] if total >= 100

    data = [100] if total >= 100
    data = [total, remaining] if total < 100

    return {
      total: total,
      remaining: remaining,
      rotation: rotation,
      data: data,
      colors: colors
    }

  render: ->
    super()
    @renderGraph('#pie-chart')
    return this

  renderGraph: (el, width, height, x, y, r) ->
    el = jQuery(el)
    width ?= 200
    height ?= 200
    x ?= 100
    y ?= 100
    r ?= 100
    return unless el and el.length > 0
    graph = Raphael(el[0], 200, 200)
    @renderPie(@progress(), graph, x, y, r)

  renderPie: (total, graph, x, y, r) ->
    graph ?= @graph
    return unless graph

    graph.clear()
    pie = @pieData(total)

    pieChart = graph.piechart(x, y, r, pie.data, {
      init: 0.1,
      colors: pie.colors
    })

    pieChart.rotate(pie.rotation) if pie.rotation

    graph.circle(x, y, r*0.98).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur()

    graph.circle(x, y, r*0.99).animate({
      stroke: "#aaa",
      "stroke-width": 1
    })

    graph.circle(x, y, r*0.70).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    })

    graph.circle(x, y, r*0.72).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur()

    graph.circle(x, y, r*0.70).animate({
      stroke: "#aaa",
      "stroke-width": 1,
      fill: "#fff"
    })

    return this

  delayRefresh: (ms) ->
    clearTimeout(@timeout) if @timeout

    delay = =>
      clearTimeout(@timeout) if @timeout
      @campaign().refreshTimes()

    @timeout = setTimeout(delay, ms)

  onRefreshRemaining: (remaining) ->
    return if remaining <= 0

    factor = 60
    factor = 1 if remaining < 61
    @delayRefresh(1000 * factor)
