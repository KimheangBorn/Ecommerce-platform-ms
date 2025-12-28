#!/bin/bash
set -e

BASE_URL="http://localhost:80"
EMAIL="testuser_$(date +%s)@example.com"
PASSWORD="password123"

echo "waiting for services..."
sleep 5

echo "1. Registering User..."
curl -s -f -X POST "$BASE_URL/api/users/register" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Test User\", \"email\": \"$EMAIL\", \"password\": \"$PASSWORD\", \"role\": \"customer\"}"
echo -e "\n[OK] User Registered"

echo "2. Logging In..."
LOGIN_RESP=$(curl -s -f -X POST "$BASE_URL/api/users/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

TOKEN=$(echo $LOGIN_RESP | grep -o '"accessToken":"[^"]*' | grep -o '[^"]*$')
echo "[OK] Login Successful. Token obtained."

echo "3. Creating Product..."
PROD_RESP=$(curl -s -f -X POST "$BASE_URL/api/products" \
  -H "Content-Type: application/json" \
  -d '{"sku": "TEST-SKU-'$(date +%s)'", "name": "Test Product", "description": "Desc", "price": 100.00, "category_id": 1}')
PROD_ID=$(echo $PROD_RESP | grep -o '"id":[^,]*' | awk -F: '{print $2}')
echo "[OK] Product Created. ID: $PROD_ID"

echo "4. Adding Inventory..."
curl -s -f -X POST "$BASE_URL/api/inventory/adjust" \
  -H "Content-Type: application/json" \
  -d "{\"product_id\": $PROD_ID, \"quantity\": 50}"
echo -e "\n[OK] Inventory Added"

echo "5. Creating Order..."
ORDER_RESP=$(curl -s -f -X POST "$BASE_URL/api/orders" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"userId\": 1, \"items\": [{\"productId\": $PROD_ID, \"quantity\": 1}]}")
ORDER_ID=$(echo $ORDER_RESP | grep -o '"orderNumber":"[^"]*' | awk -F'"' '{print $4}')
echo -e "\n[OK] Order Created. Order Number: $ORDER_ID"

echo "6. Processing Payment..."
curl -s -f -X POST "$BASE_URL/api/payments" \
  -H "Content-Type: application/json" \
  -H "idempotency-key: $(date +%s)" \
  -d "{\"order_id\": \"$ORDER_ID\", \"amount\": 100.00, \"payment_method\": \"credit_card\"}"
echo -e "\n[OK] Payment Processed"

echo -e "\n----------------------------------------"
echo "VERIFICATION SUCCESSFUL: Full flow verified."
echo "----------------------------------------"
