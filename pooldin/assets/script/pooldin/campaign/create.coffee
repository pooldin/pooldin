class PI.CampaignCreate

  @render: (opts) ->
    page = new this(opts)
    page.render()
    ko.applyBindings(page)
    return page

  constructor: (opts) ->
    opts ?= {}

    @uploader = new PI.Uploader()

  render: ->
