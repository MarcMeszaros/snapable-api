base:
  'roles:api':
    - match: grain
    - api

  'roles:worker-server':
    - match: grain
    - worker

  'roles:worker':
    - match: grain
    - worker
