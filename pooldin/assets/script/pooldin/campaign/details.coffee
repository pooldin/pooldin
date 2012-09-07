class PI.CampaignDetails

  @render: (opts) ->
    page = new this(opts)
    page.render()
    ko.applyBindings(page);
    return page

  constructor: (opts) ->
    opts ?= {}
    @total = ko.observable(opts.total)
    @total.subscribe(@render_pie, @)

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

  render: (opts) ->
    opts ?= {}
    el = opts.el or jQuery('#pie-chart')
    total = opts.total or @total()

    return unless el and el.length > 0

    @el = el
    @graph = Raphael(@el[0], 200, 200)
    @render_pie(total)

    return this

  render_pie: (total) ->
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
