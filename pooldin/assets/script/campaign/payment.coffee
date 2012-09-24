class PI.PaymentModal extends PI.Modal

  constructor: (page) ->
    super()
    @page = page

    @loginPage = ko.observable(logInUser())
    @formPage = ko.observable(not @loginPage())
    @processingPage = ko.observable(false)
    @successPage = ko.observable(false)

    @form = new PI.PaymentForm()

  getElement: ->
    return jQuery('#payment').modal({
      show: false,
      backdrop: 'static',
      keyboard: true
    })

  open: ->
    super()
    return if @page.renderedPaymentModal
    @page.renderGraph('#modal-pie-chart-login', 150, 150, 75, 75, 75)
    @page.renderGraph('#modal-pie-chart', 150, 150, 75, 75, 75)
    @page.renderedPaymentModal = true

   submitPayment: =>
     @displayErrors() if not @form.valid()
     @processingPage(true)
     el = jQuery('.processing-spinner')[0]
     @spinner = @buildSpinner()
     @spinner.spin()
     el.appendChild(@spinner.el)
     setTimeout(@paymentCallback, 2500)

   paymentCallback: (data) =>
     @paymentSuccess()

   paymentSuccess: ->
     @spinner.stop()
     @processingPage(false)
     @formPage(false)
     @successPage(true)

   displayErrors: ->
     return

   buildSpinner: ->
     opts =
       lines: 8
       length: 7
       width: 5
       radius: 10
       corners: 1
       rotate: 0
       color: "#FFF"
       speed: 1
       trail: 60
       shadow: false
       hwaccel: false
       className: "spinner"
     return Spinner(opts)

class PI.PaymentForm extends PI.Model

  constructor: ->
    @paymentAmount = ko.observable("$0.00")
    @firstName = ko.observable()
    @lastName = ko.observable()
    @address = ko.observable()
    @city = ko.observable()
    @state = ko.observable()
    @country = ko.observable()
    @postalCode = ko.observable()

    @ccNumber = ko.observable()
    @ccvNumber = ko.observable()
    @expirationMonth = ko.observable()
    @expirationYear = ko.observable()

  valid: ->
    return true
