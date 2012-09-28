class PI.UserProfile extends PI.Page

  constructor: (user, opts) ->
    @opts = opts ? {}

    @publicLabel = ko.observable('public')
    @isPublic = ko.observable(true)
    @profile = new PI.UserProfileForm(user)

  setPublic: ->
    @isPublic(not @isPublic())
    publicLabel = 'public' if @isPublic()
    publicLabel = 'private' if not @isPublic()
    @publicLabel(publicLabel)

class PI.UserProfileForm extends PI.Model

  constructor: (user)->
    super user
    @isEditing = ko.observable(false)

  toggleEdit: =>
    @isEditing(not @isEditing())
    jQuery('.about-text').focus() if @isEditing

  cancel: =>
    text = @about()
    jQuery('.about-text')[0].textContent = text
    @toggleEdit()

  save: =>
    text = jQuery.trim(jQuery('.about-text')[0].textContent)

    toSave = @dump()
    toSave.about = text

    jQuery.post("/user/#{@username()}/about", toSave, undefined, 'json')
          .done(@onSuccess)
          .fail(@onError)

    @toggleEdit()

  onSuccess: (data) =>
    @update(data)
    # display success message
    opts =
      keyboard: true
      backdrop: false
    jQuery('#user-update-success').modal(opts)

  onError: =>
    # display error message
    opts =
      keyboard: true
      backdrop: false
    jQuery('#user-update-error').modal(opts)
