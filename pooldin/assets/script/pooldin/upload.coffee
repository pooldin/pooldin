class PI.Uploader

  constructor: ->
    @visible = ko.observable(false)
    @el = jQuery('#uploader').modal({
      show: false,
      backdrop: 'static',
      keyboard: true
    })
    @visible.subscribe(@onVisible, this)

  show: ->
    @visible(true)

  hide: ->
    @visible(false)

  toggle: ->
    @visible(not @visible())

  open: =>
    @reset()
    @show()

  cancel: =>
    @reset()
    @hide()

  reset: ->

  submit: ->

  onVisible: (visible) ->
    @el.modal('show') if visible
    @el.modal('hide') unless visible
