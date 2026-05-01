# SecureShop — Workshop 3 DevSecOps
Plateforme e-commerce microservices.

## Lancer
docker compose up --build

## Health checks
curl http://localhost/api/users/health
curl http://localhost/api/products/health
curl http://localhost/api/orders/health
curl http://localhost/api/payments/health
curl http://localhost/api/notifications/health
curl http://localhost/api/inventory/health
