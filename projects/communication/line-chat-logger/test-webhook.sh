#!/bin/bash

# Webhook動作テスト用スクリプト

echo "=== Webhook動作テスト ==="
echo ""

# テストペイロード（LINE風のイベント）
PAYLOAD='{
  "events": [
    {
      "type": "message",
      "message": {
        "type": "text",
        "id": "test-message-001",
        "text": "これはテストメッセージです"
      },
      "timestamp": '$(date +%s000)',
      "source": {
        "type": "user",
        "userId": "U18750d5c193ea061814314f62f0a7bc0"
      },
      "replyToken": "test-reply-token"
    }
  ]
}'

# 署名生成
SECRET="cfa0ba820ef777f9ccbd9afc2282cdf2"
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" -binary | base64)

echo "Payload: $PAYLOAD"
echo ""
echo "Signature: $SIGNATURE"
echo ""
echo "Sending request to Vercel..."
echo ""

# リクエスト送信
curl -X POST https://line-message-logger.vercel.app/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: $SIGNATURE" \
  -d "$PAYLOAD" \
  -v

echo ""
echo ""
echo "=== ダッシュボード確認 ==="
sleep 2
curl https://line-message-logger.vercel.app/dashboard
