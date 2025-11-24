---
title: "Airレジ API仕様（推定版）"
type: api-documentation
status: active
created: "2025-10-13"
updated: "2025-10-13"
tags:
  - "project/airregi-analytics"
  - "integration/api"
---

# Airレジ API仕様（推定版）

## 注意
このドキュメントは、公開されている情報と一般的なREST API設計パターンに基づく推定です。
**実際のAPI仕様は、Airレジの公式ドキュメントで必ず確認してください。**

## ベース情報

### ベースURL（推定）
```
https://api.airregi.jp/v1
```

### 認証方式
HTTPヘッダーによる認証:
```
X-API-Key: {APIキー}
X-API-Token: {APIトークン}
Content-Type: application/json
Accept: application/json
```

## エンドポイント（推定）

### 1. ヘルスチェック
```
GET /health
GET /status
GET /ping
```

レスポンス例:
```json
{
  "status": "ok",
  "timestamp": "2025-10-13T10:00:00Z"
}
```

### 2. 取引情報取得
```
GET /transactions
```

クエリパラメータ:
- `start_date`: 開始日（YYYY-MM-DD形式）
- `end_date`: 終了日（YYYY-MM-DD形式）
- `limit`: 取得件数上限（デフォルト: 100）
- `offset`: オフセット（ページネーション用）

レスポンス例:
```json
{
  "transactions": [
    {
      "transaction_id": "TXN20251013001",
      "transaction_datetime": "2025-10-13T14:30:00+09:00",
      "amount": 5800,
      "tax": 528,
      "payment_method": "現金",
      "items": [
        {
          "product_id": "P001",
          "product_name": "商品A",
          "quantity": 2,
          "unit_price": 1500,
          "subtotal": 3000
        }
      ],
      "customer_id": null,
      "staff_id": "S001",
      "store_id": "STORE001"
    }
  ],
  "total_count": 150,
  "page": 1,
  "per_page": 100
}
```

### 3. 売上サマリー取得
```
GET /sales/summary
```

クエリパラメータ:
- `start_date`: 開始日
- `end_date`: 終了日
- `group_by`: グルーピング基準（day, week, month）

レスポンス例:
```json
{
  "summary": {
    "total_sales": 1250000,
    "total_transactions": 320,
    "average_transaction": 3906,
    "total_tax": 113636,
    "daily_breakdown": [
      {
        "date": "2025-10-01",
        "sales": 42000,
        "transactions": 15
      }
    ]
  },
  "period": {
    "start_date": "2025-10-01",
    "end_date": "2025-10-31"
  }
}
```

### 4. 精算情報取得
```
GET /settlements
```

クエリパラメータ:
- `date`: 精算日（YYYY-MM-DD形式）
- `store_id`: 店舗ID（複数店舗の場合）

レスポンス例:
```json
{
  "settlement": {
    "settlement_id": "SET20251013001",
    "date": "2025-10-13",
    "cash_sales": 120000,
    "card_sales": 85000,
    "other_sales": 12000,
    "total_sales": 217000,
    "opening_cash": 50000,
    "closing_cash": 170000,
    "expected_cash": 170000,
    "difference": 0,
    "status": "completed"
  }
}
```

### 5. 入出金情報取得
```
GET /cash-flow
```

クエリパラメータ:
- `start_date`: 開始日
- `end_date`: 終了日
- `type`: タイプ（in: 入金, out: 出金, all: すべて）

レスポンス例:
```json
{
  "cash_flows": [
    {
      "id": "CF20251013001",
      "datetime": "2025-10-13T10:00:00+09:00",
      "type": "in",
      "amount": 100000,
      "category": "つり銭補充",
      "note": "営業開始前の準備金",
      "staff_id": "S001"
    }
  ]
}
```

### 6. 商品マスタ取得
```
GET /products
```

クエリパラメータ:
- `category_id`: カテゴリID
- `status`: ステータス（active, inactive, all）
- `limit`: 取得件数上限
- `offset`: オフセット

レスポンス例:
```json
{
  "products": [
    {
      "product_id": "P001",
      "product_name": "商品A",
      "category_id": "C001",
      "category_name": "カテゴリ1",
      "price": 1500,
      "tax_rate": 0.10,
      "sku": "SKU001",
      "status": "active"
    }
  ]
}
```

## エラーレスポンス

### 共通エラー形式
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": "詳細情報"
  }
}
```

### HTTPステータスコード
- `200 OK`: 成功
- `400 Bad Request`: リクエストパラメータエラー
- `401 Unauthorized`: 認証エラー
- `403 Forbidden`: アクセス権限なし
- `404 Not Found`: リソースが見つからない
- `429 Too Many Requests`: レート制限超過
- `500 Internal Server Error`: サーバーエラー

### レート制限
- リクエスト数: 不明（要確認）
- レート制限時のヘッダー:
  ```
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 999
  X-RateLimit-Reset: 1697184000
  Retry-After: 60
  ```

## データ取得制限

### 期間制限
- **過去2ヶ月分**のデータが取得可能
- それ以前のデータは取得不可

### ページネーション
- デフォルト: 100件/ページ
- 最大: 1000件/ページ（推定）

## 実装時の注意事項

### 1. エンドポイントの確認
実際のエンドポイントは以下で確認してください：
- Airレジ バックオフィス > データ連携API設定
- Airレジ公式サポートページ
- 技術サポートへの問い合わせ

### 2. 認証情報の管理
- APIキー・トークンは外部に漏らさない
- 定期的に更新する
- 環境変数で管理する

### 3. エラーハンドリング
- レート制限に対応する（リトライ機能）
- ネットワークエラーに対応する
- タイムアウト処理を実装する

### 4. ログ記録
- すべてのAPIリクエストをログに記録
- エラー時の詳細情報を保存
- 個人情報はログに含めない

## 次のステップ

1. **公式ドキュメントの確認**
   - Airレジのサポートページで正確なAPI仕様を確認
   - エンドポイントURLの確認
   - パラメータ仕様の確認

2. **接続テストの実施**
   ```bash
   python test_api.py
   ```

3. **エンドポイントの調整**
   - テスト結果に基づき `src/api/client.py` を修正
   - 正しいエンドポイントに更新

4. **本番運用**
   - データ取得の確認
   - 分析結果の確認
   - レポート生成の確認

## 参考情報

### Airレジ関連リンク
- Airレジ公式サイト: https://airregi.jp/
- サポートページ: https://faq.airregi.jp/
- バックオフィス: https://airregi.jp/backoffice/

### 技術サポート
API仕様の詳細については、Airレジのテクニカルサポートにお問い合わせください。

---

## 関連ドキュメント

- [[GOOGLE_SHEETS_SETUP]]

