#!/bin/bash

# Script de Teste CURL - Letícia Kyoko Bot
# Token: 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1

echo "🚀 Testando API Pushinpay com novo token da Letícia..."
echo "================================================"

# Configurações
TOKEN="42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1"
API_URL="https://api.pushinpay.com.br/api/pix/cashIn"

echo "📋 Token: $TOKEN"
echo "🔗 URL: $API_URL"
echo ""

# Teste 1: Pack Básico - R$ 9,90
echo "💕 Teste 1: Pack Básico - R$ 9,90"
echo "----------------------------------"
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 990
  }' \
  -w "\nStatus: %{http_code}\nTempo: %{time_total}s\n\n"

echo "💖 Teste 2: Pack Médio - R$ 15,90"
echo "----------------------------------"
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 1590
  }' \
  -w "\nStatus: %{http_code}\nTempo: %{time_total}s\n\n"

echo "🔥 Teste 3: Pack Completo - R$ 19,90"
echo "------------------------------------"
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 1990
  }' \
  -w "\nStatus: %{http_code}\nTempo: %{time_total}s\n\n"

echo "📹 Teste 4: Vídeochamada - R$ 49,90"
echo "-----------------------------------"
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 4990
  }' \
  -w "\nStatus: %{http_code}\nTempo: %{time_total}s\n\n"

echo "🌙 Teste 5: Programa - R$ 249,90"
echo "-------------------------------"
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 24990
  }' \
  -w "\nStatus: %{http_code}\nTempo: %{time_total}s\n\n"

echo "✅ Testes concluídos!"
echo "====================="
echo "📊 Resultados:"
echo "• Status 200/201 = Sucesso"
echo "• Status 400+ = Erro"
echo "• Tempo < 2s = Performance boa"
echo ""
echo "🔍 Verificar:"
echo "• Se todos retornaram status 200/201"
echo "• Se o QR Code foi gerado"
echo "• Se o ID do PIX foi retornado"
echo "• Se o tempo de resposta está bom"