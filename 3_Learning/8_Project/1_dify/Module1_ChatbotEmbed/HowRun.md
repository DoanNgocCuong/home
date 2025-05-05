# 1. Cách run với mặc định của dify: 
```bash
docker compose -f docker/docker-compose.yaml up
```
Cách run với image đã build sẵn
```bash
docker compose -f docker/docker-compose.yaml up --build
```

Tuy nhiên với việc run như trên thì sẽ không có api và web mới. 
- Cách 1: build image của api và web mới sau đó run `docker compose -f docker/docker-compose.yaml up`
- Cách 2: Truyền trực tiếp build (thay vì sử dụng image) vào `docker compose -f docker/docker-compose.yaml up`
```bash
image: langgenius/dify-api:0.9.2
```
thành 
```bash
build:
  context: ./api
  dockerfile: Dockerfile
```

# 3. Cách run 
