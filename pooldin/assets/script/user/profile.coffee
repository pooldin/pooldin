class PI.UserProfile extends PI.Page

  constructor: (user, opts) ->
    @opts = opts ? {}

    @publicLabel = ko.observable('public')
    @isPublic = ko.observable(true)

  setPublic: ->
    @isPublic(not @isPublic())
    publicLabel = 'public' if @isPublic()
    publicLabel = 'private' if not @isPublic()
    @publicLabel(publicLabel)
