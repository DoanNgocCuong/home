
WEB: 

1. https://github.com/DoanNgocCuong/MiniProd_GradingVidMentorTeaching_StepUpE_T102024/blob/deploy1.3/ DOCKER COMPOSE của html css, python backend
2. [MiniProd_ContentEngFlow_IELTSStepUpE_T102024/deploy1.1/backend/app.py at main · DoanNgocCuong/MiniProd_ContentEngFlow_IELTSStepUpE_T102024](https://github.com/DoanNgocCuong/MiniProd_ContentEngFlow_IELTSStepUpE_T102024/blob/main/deploy1.1/backend/app.py)
DOCKER COMPOSE của backend python, react



Thông qua bridge 

```
version: '3'

  

services:

  backend:

    build:

      context: ./backend

      dockerfile: Dockerfile

    ports:

      - "25039:3001"

    environment:

      - FLASK_ENV=production

      - API_URL=http://103.253.20.13:5011

      - ALLOWED_ORIGINS=http://103.253.20.13:25040,http://103.253.20.13:5011

    healthcheck:

      test: ["CMD", "curl", "-f", "http://localhost:3001/health"]

      interval: 30s

      timeout: 10s

      retries: 3

    restart: always

  

  frontend:

    build:

      context: ./frontend

      dockerfile: Dockerfile

    ports:

      - "25040:5000"

    environment:

      - NODE_ENV=production

      - BACKEND_URL=http://103.253.20.13:25039

    depends_on:

      - backend

    restart: always

  

networks:

  app-network:

    driver: bridge
```

thì 1 bản `docker-compose -f docker-compose.prod.yml up --build` như này cũng chạy được ngon trên local