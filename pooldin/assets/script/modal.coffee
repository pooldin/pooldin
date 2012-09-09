class PI.Modal

  constructor: ->
    @visible = ko.observable(false)
    @el = @getElement()
    @visible.subscribe(@onVisible, this)

  show: ->
    @visible(true)

  hide: ->
    @visible(false)

  toggle: =>
    @visible(not @visible())

  open: =>
    @reset()
    @show()

  cancel: =>
    @reset()
    @hide()

  submit: =>

  reset: ->

  onVisible: (visible) ->
    @el.modal('show') if visible
    @el.modal('hide') unless visible
