class PI.CampaignManager
  constructor: ->
    @tab = ko.observable()
    @tab.subscribe(@onTab, this)
    @navigate(location.hash)
    @visible = ko.observable(not not @tab())

    jQuery('.nav-tabs.manage a[data-toggle="tab"]').on 'shown', (e) =>
      @navigate(jQuery(e?.target).attr('href'))

  show: ->
    @visible(true)

  hide: ->
    @visible(false)

  toggle: ->
    @visible(not @visible())

  navigate: (tab) ->
    tab = (tab ? '').replace(/^#/g, '')
    @tab(tab) if tab in ['manage', 'promote', 'disburse']
    return this

  onTab: ->
    tab = @tab()
    return unless tab
    jQuery(".nav-tabs li a[href=##{tab}]").tab('show')

  cancel: ->
    @reset()
    @hide()

  reset: ->

  submit: ->
