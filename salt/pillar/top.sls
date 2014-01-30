base:
  'roles:api':
    - match: grain
    - api

  'roles:worker-server':
    - match: grain
    - worker

  'roles:worker-node':
    - match: grain
    - worker
