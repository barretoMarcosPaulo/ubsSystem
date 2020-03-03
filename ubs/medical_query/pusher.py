import pusher

pusher_client = pusher.Pusher(
  app_id='957558',
  key='7c5598615bc9fbb306d2',
  secret='07bc8db23839a52a0597',
  cluster='us2',
  ssl=False
)

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})