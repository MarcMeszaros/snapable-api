snap_user:
  user: vagrant

celery:
  flower:
    broker: 'amqp://snap_api:snapable12345@192.168.56.102:5672/snap_api'

# only enable once "Hydrogen" is released
#rabbitmq:
#  plugins:
#    - rabbitmq_management