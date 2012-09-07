class PI.CampaignDetails

  @render: ->
    page = new this()
    page.render()
    return page

  render: ->
    @el = jQuery('#pie-chart')
    @graph = Raphael("pie-chart", 200, 200)

    total = 88

    pie = @pieData(total)

    chart = @graph.piechart(100, 100, 100, pie.data, {
      init: 0.1,
      colors: pie.colors
    })

    chart.rotate(pie.rotation) if pie.rotation

    return this

  pieData: (total) ->
    total = 0 if total < 0
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
