# Installing

```sh
brew install k6
```

# Running tests

Because Erica is not accessible outside our cluster, it needs to be run inside the cluster. You could e.g. use this to create a pod & run some tests & delete the pod again:

```sh
kubectl --kubeconfig ~/.kube/otc-dev --namespace erica-staging run -i --rm --restart=Never --image=grafana/k6 load-test -- run - <test.js
```

# Visualizing results with Grafana

Attribution: Building on https://github.com/luketn/docker-k6-grafana-influxdb

```zsh
cd visualization/

# Start services
docker-compose up -d

# Install conversion script dependencies
pipenv install

# Run tests & process results:
(
  kubectl --kubeconfig ~/.kube/otc-dev --namespace erica-staging run -i --rm --restart=Never --image=grafana/k6 load-test -- run --quiet --out json=output - <../test.js &
  sleep 1
  kubectl --kubeconfig ~/.kube/otc-dev --namespace erica-staging wait --for=jsonpath='{.status.phase}'=Running pods/load-test
  kubectl --kubeconfig ~/.kube/otc-dev --namespace erica-staging exec load-test -- sh -c 'while [ ! -f output ]; do sleep 0.5; done; tail -n +0 -f output' | pipenv run python ./send_to_influx.py - influxdb://localhost:8086/k6
)
```

Access the dashboard at [http://localhost:3000/d/k6/k6-load-testing-results](http://localhost:3000/d/k6/k6-load-testing-results)

When you're finished, you can shut down the services and delete the data:

```sh
docker-compose down
```
