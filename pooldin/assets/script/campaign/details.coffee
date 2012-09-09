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

    el = jQuery('#pie-chart')
    return unless el and el.length > 0

    @el = el
    @graph = Raphael(@el[0], 200, 200)
    @renderPie(@progress())

    return this

  renderPie: (total) ->
    return unless @graph

    @graph.clear()
    pie = @pieData(total)

    @pie = @graph.piechart(100, 100, 100, pie.data, {
      init: 0.1,
      colors: pie.colors
    })

    @pie.rotate(pie.rotation) if pie.rotation

    @graph.circle(100, 100, 98).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur()

    @graph.circle(100, 100, 99).animate({
      stroke: "#aaa",
      "stroke-width": 1
    })

    @graph.circle(100, 100, 70).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    })

    @graph.circle(100, 100, 72).animate({
      stroke: "#747C7D",
      "stroke-width": 2
    }).blur()

    @graph.circle(100, 100, 70).animate({
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
