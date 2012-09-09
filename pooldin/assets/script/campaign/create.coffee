class PI.CampaignCreate extends PI.Page

  constructor: (opts) ->
    @opts = opts ? {}
    @uploader = new PI.Uploader()
