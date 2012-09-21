class PI.CampaignCreate extends PI.Page

  constructor: (opts) ->
    @opts = opts ? {}
    @uploader = new PI.UploadModal()

    @campaignType = ko.observable()
    @campaignType.subscribe(@onCampaignType, this)

    @requiredAmount = ko.observable()

    @paymentAmountType = ko.observable()
    @paymentAmountType.subscribe(@onPaymentAmountType, this)

    @campaignContract = ko.observable(false)
    @amazonPurchase = ko.observable(false)

    @typeDependentVisible = ko.observable(false)
    @paymentTypeDependentVisible = ko.observable(false)

   onCampaignType: (type) ->
     visible = type in ['co-own', 'gift']
     @toggleTypeDependents(visible)

   onPaymentAmountType: (type) ->
     visible = type is 'specific'
     @togglePaymentTypeDependents(visible)

   toggleTypeDependents: (visible) ->
     @typeDependentVisible(visible)
     @campaignContract(visible) if not visible

   togglePaymentTypeDependents: (visible) ->
     @paymentTypeDependentVisible(visible)
     @requiredAmount(0)
