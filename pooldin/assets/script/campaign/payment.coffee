class PI.PaymentModal extends PI.Modal

  constructor: (page) ->
    super()
    @page = page

    @login = ko.observable(logInUser())
    @form = ko.observable(not @login())
    @processing = ko.observable(false)
    @success = ko.observable(false)

  getElement: ->
    return jQuery('#payment').modal({
      show: false,
      backdrop: 'static',
      keyboard: true
    })

  open: ->
    super()
    @page.renderGraph('#modal-pie-chart-login', 150, 150, 75, 75, 75)
    @page.renderGraph('#modal-pie-chart', 150, 150, 75, 75, 75)
