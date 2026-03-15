θ60° 3d [ubuntu@mgc-dev2-3090:~/cuong_dn/LS_ai_automation/ … /webVisulizeDB_
ver2_fullstack]└4 <base> dev(+5/-5)* ± docker compose up --build -d 
WARN[0000] /home/ubuntu/cuong_dn/LS_ai_automation/utils_importDB/webVisulizeDB_ver2_fullstack/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
Compose can now delegate builds to bake for better performance.
 To do so, set COMPOSE_BAKE=true.
[+] Building 3.0s (14/14) FINISHED               docker-container:mybuilder
 => [ai-coach-api internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 969B                                   0.0s
 => [ai-coach-api internal] load metadata for docker.io/library/pytho  0.8s
 => [ai-coach-api internal] load .dockerignore                         0.0s
 => => transferring context: 2B                                        0.0s
 => [ai-coach-api 1/7] FROM docker.io/library/python:3.11-slim@sha256  0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:9e1912aab0a3  0.0s
 => [ai-coach-api internal] load build context                         0.0s
 => => transferring context: 4.58kB                                    0.0s
 => CACHED [ai-coach-api 2/7] WORKDIR /app                             0.0s
 => CACHED [ai-coach-api 3/7] RUN apt-get update && apt-get install -  0.0s
 => CACHED [ai-coach-api 4/7] COPY requirements.txt .                  0.0s
 => CACHED [ai-coach-api 5/7] RUN pip install --no-cache-dir -r requi  0.0s
 => [ai-coach-api 6/7] COPY app.py .                                   0.1s
 => [ai-coach-api 7/7] RUN useradd -m -u 1000 appuser && chown -R app  0.5s
 => [ai-coach-api] exporting to docker image format                    1.5s
 => => exporting layers                                                0.1s
 => => exporting manifest sha256:7c51e208fa352c58f23917470be2c4b83d67  0.0s
 => => exporting config sha256:6e66545cf50d1312b22b97247cbd1776c220ea  0.0s
 => => sending tarball                                                 1.4s
 => [ai-coach-api] importing to docker                                 0.2s
 => => loading layer c0091be9d879 1.62kB / 1.62kB                      0.2s
 => => loading layer b4290bd71a59 4.98kB / 4.98kB                      0.1s
 => [ai-coach-api] resolving provenance for metadata file              0.0s
[+] Running 2/2
 ✔ ai-coach-api                                           Built        0.0s 
 ✘ Network webvisulizedb_ver2_fullstack_ai-coach-network  Error        0.0s 
failed to create network webvisulizedb_ver2_fullstack_ai-coach-network: Error response from daemon: could not find an available, non-overlapping IPv4 address pool among the defaults to assign to the network
θ62° 3d [ubuntu@mgc-dev2-3090:~/cuong_dn/LS_ai_automation/ … /webVisulizeDB_
ver2_fullstack]└4 <base> dev(+13/-13)* ± 