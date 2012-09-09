class PI.ObservableDict

  constructor: (dict) ->
    @fields = {}
    @update(dict)

  get: (key) ->
    return unless @fields[key]
    return @getObservable()?()

  getObservable: (key) ->
    return unless @fields[key]
    return @fields[key]

  set: (key, value) ->
    @fields[key] = ko.observable(value) unless @fields[key]
    @fields[key](value)
    return this

  update: (dict) ->
    @set(key, value) for key, value of (dict ? {})
    return this

  remove: (key) ->
    delete @fields[key]
    return this

  setObservable: (key, value) ->
    @fields[key] = value
    return this

  subscribe: (key, handler, context) ->
    observable = @getObservable(key)
    observable = @set(key).getObservable(key) unless observable
    return observable.subscribe(key, handler, context)


PI.settings = new PI.ObservableDict({
  theme: {
    teal: '#739b9e',
    white: '#fff'
  }
})
