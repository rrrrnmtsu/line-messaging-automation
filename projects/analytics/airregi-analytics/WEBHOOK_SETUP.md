---
title: "Airレジ Webhookサーバー セットアップガイド"
type: setup-guide
status: active
created: "2025-10-14"
updated: "2025-10-14"
tags:
  - "project/airregi-analytics"
  - "documentation/setup"
  - "setup/configuration"
  - "integration/webhook"
---

# Airレジ Webhookサーバー セットアップガイド

**作成日**: 2025年10月13日
**目的**: AirレジからのPush型データ受信に対応

---

## 📋 概要

このガイドでは、Airレジからデータを受信するためのWebhookサーバーのセットアップ方法を説明します。

### システム構成

```
Airレジ端末 → [精算完了] → Webhook送信 → 本Webhookサーバー
                                              ↓
                                    データ保存 (data/raw/)
                                              ↓
                                    分析処理 (既存機能活用)
```

---

## 🚀 Webhookサーバーの起動

### ローカル環境での起動

```bash
cd /Users/remma/airregi-analytics
source venv/bin/activate
python webhook_server.py
```

**起動メッセージ例**:
```
============================================================
Airレジ Webhookサーバー 起動
============================================================
APIキー: AKR3509874... (先頭10文字)
ポート: 5000
デバッグモード: True

利用可能なエンドポイント:
  GET  /health
  POST /webhook/airregi/transactions
  POST /webhook/airregi/settlements
  POST /webhook/airregi
============================================================
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

---

## 🌐 外部公開の方法

ローカルサーバーを外部に公開し、Airレジからアクセスできるようにします。

### オプション1: ngrok（開発・テスト用）

#### ngrokのインストール
```bash
# Homebrewでインストール
brew install ngrok
```

#### ngrokの起動
```bash
# 別のターミナルで実行
ngrok http 5000
```

#### 公開URL取得
ngrokの出力から以下のURLを確認:
```
Forwarding  https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:5000
```

このURL `https://xxxx-xx-xx-xx-xx.ngrok-free.app` を使用します。

### オプション2: 本番サーバー（VPS/クラウド）

#### 必要な環境
- VPS または クラウドサーバー (AWS EC2, GCP Compute Engine等)
- グローバルIPアドレス
- ドメイン (推奨)
- SSL/TLS証明書 (必須)

#### gunicornでの本番起動
```bash
# 本番環境用の起動
gunicorn -w 4 -b 0.0.0.0:5000 webhook_server:app
```

#### nginxリバースプロキシ設定例
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /webhook/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔧 Airレジ側の設定

### ステップ1: バックオフィスにログイン
1. Airレジアプリまたはブラウザからバックオフィスにアクセス
2. 管理者権限でログイン

### ステップ2: データ連携API設定
1. 「設定」メニューを選択
2. 「データ連携API」を選択
3. 「API利用を開始する」ボタンをクリック
4. 利用規約に同意

### ステップ3: Webhook URL登録

**登録するURL**:

開発環境（ngrok使用時）:
```
https://xxxx-xx-xx-xx-xx.ngrok-free.app/webhook/airregi
```

本番環境:
```
https://your-domain.com/webhook/airregi
```

**利用可能なエンドポイント**:
- `/webhook/airregi` - 汎用エンドポイント（推奨）
- `/webhook/airregi/transactions` - 取引データ専用
- `/webhook/airregi/settlements` - 精算データ専用

### ステップ4: テスト送信
1. Airレジ側で「テスト送信」機能を実行（もしあれば）
2. 実際の精算を行って確認

---

## 🧪 動作確認

### ヘルスチェック
```bash
curl http://localhost:5000/health
```

**期待されるレスポンス**:
```json
{
  "status": "ok",
  "service": "Airレジ Webhook Server",
  "version": "1.0.0"
}
```

### テストWebhookの送信

#### 取引データのテスト
```bash
curl -X POST http://localhost:5000/webhook/airregi/transactions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: AKR3509874320" \
  -H "X-API-Token: d8cc04d0833544e395eb7cbd48d23292" \
  -d '{
    "type": "transaction",
    "transaction_id": "TEST001",
    "timestamp": "2025-10-13T19:00:00+09:00",
    "data": {
      "amount": 1500,
      "items": []
    }
  }'
```

**期待されるレスポンス**:
```json
{
  "status": "success",
  "message": "Data processed successfully",
  "filename": "webhook_transaction_20251013_190000.json"
}
```

#### 受信データの確認
```bash
ls -la data/raw/webhook_*
```

---

## 📊 ログ確認

### リアルタイムログ監視
```bash
tail -f logs/WebhookServer_$(date +%Y%m%d).log
```

### ログの種類
- `WebhookServer_YYYYMMDD.log` - サーバー起動・リクエスト受信
- `WebhookHandler_YYYYMMDD.log` - データ処理ログ
- `WebhookAuth_YYYYMMDD.log` - 認証ログ

---

## 🔐 セキュリティ設定

### 認証方式

現在の実装:
- HTTPヘッダー: `X-API-Key`, `X-API-Token`
- または JSONボディ内: `api_key`, `api_token`

**重要**: 実際のAirレジ仕様に合わせて `src/webhook/auth.py` を調整してください。

### ファイアウォール設定

本番環境では以下のポートのみ開放:
- 443 (HTTPS) - 必須
- 80 (HTTP) - HTTPSへのリダイレクト用

### レート制限（推奨）

nginx設定例:
```nginx
limit_req_zone $binary_remote_addr zone=webhook:10m rate=10r/s;

location /webhook/ {
    limit_req zone=webhook burst=20;
    proxy_pass http://127.0.0.1:5000;
}
```

---

## 🔄 データフロー

### 1. Webhook受信
```
Airレジ → POST /webhook/airregi → Webhookサーバー
```

### 2. 認証チェック
```
APIキー・トークン検証 → OK/NG
```

### 3. データ保存
```
data/raw/webhook_transaction_YYYYMMDD_HHMMSS.json
```

**保存形式**:
```json
{
  "received_at": "2025-10-13T19:00:00+09:00",
  "data_type": "transaction",
  "payload": {
    // Airレジから受信したデータ
  }
}
```

### 4. 分析処理（将来実装）
```
既存の分析エンジン → レポート生成
```

---

## ⚠️ トラブルシューティング

### Webhookが受信できない

#### チェックリスト:
- [ ] サーバーが起動しているか確認
  ```bash
  ps aux | grep webhook_server
  ```
- [ ] ファイアウォールでポート開放されているか
- [ ] ngrokが正常に動作しているか
- [ ] AirレジにURL正しく登録されているか
- [ ] HTTPSになっているか（本番環境）

### 認証エラー (401/403)

**原因**:
- APIキー・トークンが間違っている
- ヘッダー名が仕様と異なる

**対処**:
1. ログファイルで認証情報を確認
2. Airレジ側の仕様を確認
3. `src/webhook/auth.py` を調整

### データが保存されない

**確認事項**:
1. ディレクトリの書き込み権限
   ```bash
   ls -ld data/raw/
   ```
2. ディスク容量
   ```bash
   df -h
   ```
3. ログでエラー確認
   ```bash
   grep ERROR logs/WebhookHandler_*.log
   ```

---

## 📝 カスタマイズ

### データ処理のカスタマイズ

**ファイル**: `src/webhook/handler.py`

```python
def process_transaction_data(self, payload):
    # カスタム処理を追加
    # 例: 特定の条件で通知送信
    if payload.get('amount', 0) > 10000:
        send_alert_email()
```

### 認証方式のカスタマイズ

**ファイル**: `src/webhook/auth.py`

```python
def verify_airregi_auth(f):
    # 実際のAirレジ仕様に合わせて変更
    # 例: HMAC署名検証
    signature = request.headers.get('X-Signature')
    if not verify_signature(signature, request.data):
        return jsonify({"error": "Invalid signature"}), 403
```

---

## 🔜 次のステップ

### 1. Airレジ公式仕様の確認
- [ ] Webhook送信の正確なデータ形式を確認
- [ ] 認証方式の確認
- [ ] エラーハンドリング仕様の確認

### 2. 本番環境の準備
- [ ] VPS/クラウドサーバーの契約
- [ ] ドメインの取得
- [ ] SSL証明書の取得・設定
- [ ] 監視・アラート設定

### 3. 運用開始
- [ ] テストデータで動作確認
- [ ] 実データで検証
- [ ] 定常運用開始

---

## 📞 サポート

### Airレジサポート
- **FAQページ**: https://faq.airregi.jp/hc/ja/
- **サポートページ**: https://airregi.jp/jp/features/support/

### 技術的な問い合わせ推奨事項
```
件名: データ連携API - Webhook仕様について

以下の技術情報をご教示ください:
1. Webhookで送信されるデータ形式（JSON構造）
2. 認証方式の詳細（ヘッダー名、検証方法等）
3. エラー時のリトライ仕様
4. サンプルペイロード

開発環境情報:
- プログラミング言語: Python 3.13
- Webフレームワーク: Flask 3.1
```

---

## 📚 関連ドキュメント

- [API_ARCHITECTURE_UPDATE.md](API_ARCHITECTURE_UPDATE.md) - アーキテクチャ変更の詳細
- [USAGE.md](USAGE.md) - システム全体の使用方法
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - プロジェクト概要

---

**重要**: 本ドキュメントは推定ベースの実装です。実際の運用前に必ずAirレジの公式技術仕様を確認してください。

---

## 関連ドキュメント

- [[API_ARCHITECTURE_UPDATE]]
- [[API_SPECIFICATION]]
- [[GOOGLE_SHEETS_SETUP]]

