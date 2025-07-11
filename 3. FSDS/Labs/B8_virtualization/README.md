## Multi stage build
### Before

```bash
docker build -t before_msb -f mlflow/Dockerfile --build-arg MLFLOW_VERSION=2.3.2 mlflow && docker run -p 5000:5000 before_msb
```

### After

```bash
docker build -t after_msb -f mlflow/Dockerfile-multistage-build --build-arg MLFLOW_VERSION=2.3.2 mlflow && docker run -p 5000:5000 after_msb
```

## Docker Compose
- Up and running MLFlow application with Docker Compose
    
    ```shell
    docker compose -f mlflow-docker-compose.yaml up -d
    ```
- Similarly, you can do it for Trino
    
    ```shell
    docker compose -f trino-docker-compose.yaml up -d
    ```