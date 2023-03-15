kubectl label node w1-k8s gpupool=nvidia accelerator=tesla-a100 --overwrite=true
kubectl label node w2-k8s gpupool=nvidia accelerator=tesla-v100 --overwrite=true
kubectl label node w3-k8s diskint=nvme inmemory=redis --overwrite=true