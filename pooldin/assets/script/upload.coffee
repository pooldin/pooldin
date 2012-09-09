class PI.UploadModal extends PI.Modal

  getElement: ->
    return jQuery('#uploader').modal({
      show: false,
      backdrop: 'static',
      keyboard: true
    })
