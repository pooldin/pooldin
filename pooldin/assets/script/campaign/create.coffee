class PI.CampaignCreate extends PI.Page

  constructor: (opts) ->
    @opts = opts ? {}
    @uploader = new PI.UploadModal()

    @campaignType = ko.observable()
    @campaignType.subscribe(@onCampaignType, this)

    @campaignContract = ko.observable(false)
    @amazonPurchase = ko.observable(false)
    @typeDependentVisible = ko.observable(false)

   onCampaignType: (type) ->
     visible = type in ['co-own', 'gift']
     @toggleTypeDependents(visible)

   toggleTypeDependents: (visible) ->
     @typeDependentVisible(visible)
     @campaignContract(visible) if not visible
