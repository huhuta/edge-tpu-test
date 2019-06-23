helm upgrade --install edge-tpu-test ./k8s/helm/edge-tpu-test \
 -f k8s/values.yaml \
 --namespace default \
 --set volume.src="${PWD}"