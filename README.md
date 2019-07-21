# mx_sim

Start Redis from docker:

`~$: sudo docker run --name=redis-devel --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest`

Add this repo to PYTHONPATH:

`~$: export PYTHONPATH="root_dir_to_mx_sim:$PYTHONPATH"`

Run async websocket price update server:

`~$: python -m mx_sim.pricing.price_update_server`

Run Celery workers:

`~$: celery -A mx_sim.mq.async_tasks worker --loglevel=info`

Run Flask frontend

`~$: cd mx_sim_dir_location`

`~/mx_sim_dir_location$: flask run`
