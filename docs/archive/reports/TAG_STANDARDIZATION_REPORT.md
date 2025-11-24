---
title: "Tag Standardization Report"
type: documentation
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "metadata/standardization"
  - "documentation/report"
---

# タグ標準化レポート

**実施日**: 2025-11-01 13:50
**対象**: /Users/remma/project

## 統計サマリー

- 総ファイル数: 126
- 更新対象: 14
- 変更不要: 111
- タグなし: 1
- フロントマターなし: 0
- エラー: 0

## 変更詳細

### projects/automation/dify-n8n-workflow/MOC - Project Overview.md

**変更前**:
```yaml
  - "moc"
  - "index"
  - "navigation"
```

**変更後**:
```yaml
  - "navigation/moc"
  - "navigation/index"
```

### projects/automation/dify-n8n-workflow/VAULT_OPTIMIZATION_REPORT.md

**変更前**:
```yaml
  - "optimization"
  - "vault-health"
  - "performance"
```

**変更後**:
```yaml
  - "metadata/optimization"
  - "metadata/vault-health"
  - "metadata/performance"
```

### projects/automation/dify-n8n-workflow/SESSION_5_BRANCH.md

**変更前**:
```yaml
  - "documentation/report"
  - "setup/general"
```

**変更後**:
```yaml
  - "documentation/report"
  - "setup/configuration"
```

### projects/automation/dify-n8n-workflow/STANDARDIZATION_SUMMARY.md

**変更前**:
```yaml
  - "metadata"
  - "documentation"
  - "standardization"
```

**変更後**:
```yaml
  - "metadata/standards"
  - "documentation/guide"
  - "metadata/standardization"
```

### projects/automation/dify-n8n-workflow/TAG_MIGRATION_REPORT.md

**変更前**:
```yaml
  - "sales-automation"
```

**変更後**:
```yaml
  - "workflow/sales-report"
```

### projects/automation/dify-n8n-workflow/gas-scripts/README.md

**変更前**:
```yaml
  - "documentation/readme"
  - "setup/general"
```

**変更後**:
```yaml
  - "documentation/readme"
  - "setup/configuration"
```

### projects/automation/dify-n8n-workflow/docs/telegram-bot-setup.md

**変更前**:
```yaml
  - "documentation/guide"
  - "integration/webhook"
  - "setup/docker"
  - "setup/general"
  - "setup/telegram"
  - "workflow/telegram"
```

**変更後**:
```yaml
  - "documentation/guide"
  - "integration/webhook"
  - "setup/docker"
  - "setup/configuration"
  - "setup/telegram"
  - "workflow/telegram"
```

### projects/automation/dify-n8n-workflow/n8n/SERPSTACK-API-SETUP.md

**変更前**:
```yaml
  - "documentation/guide"
  - "integration/api"
  - "integration/api/serpstack"
  - "setup/api/serpstack"
  - "setup/docker"
  - "workflow/seo"
```

**変更後**:
```yaml
  - "documentation/guide"
  - "integration/api"
  - "integration/api/serpstack"
  - "setup/docker"
  - "workflow/seo"
```

### projects/automation/dify-n8n-workflow/n8n/API-RESEARCH-REPORT.md

**変更前**:
```yaml
  - "documentation/report"
  - "integration/api"
  - "setup/api"
  - "workflow/seo"
```

**変更後**:
```yaml
  - "documentation/report"
  - "integration/api"
  - "workflow/seo"
```

### dify_note/unpublicnoteapi/README.md

**変更前**:
```yaml
  - "project/dify_note"
  - "documentation/readme"
  - "integration/api"
```

**変更後**:
```yaml
  - "project/dify-note"
  - "documentation/readme"
  - "integration/api"
```

### dify_note/unpublicnoteapi/sample_article.md

**変更前**:
```yaml
  - "project/dify_note"
  - "integration/api"
```

**変更後**:
```yaml
  - "project/dify-note"
  - "integration/api"
```

### suno_auto/CHANGELOG.md

**変更前**:
```yaml
  - "project/suno_auto"
  - "documentation/changelog"
```

**変更後**:
```yaml
  - "project/suno-auto"
  - "documentation/changelog"
```

### suno_auto/README.md

**変更前**:
```yaml
  - "project/suno_auto"
  - "documentation/readme"
```

**変更後**:
```yaml
  - "project/suno-auto"
  - "documentation/readme"
```

### suno_auto/WORKLOG.md

**変更前**:
```yaml
  - "project/suno_auto"
  - "documentation/changelog"
```

**変更後**:
```yaml
  - "project/suno-auto"
  - "documentation/changelog"
```

## 実行方法

変更を適用するには:
```bash
python3 /Users/remma/project/scripts/tag_standardizer.py
```

---

## 関連ドキュメント

- [[TAG_IMPLEMENTATION_COMPLETE]]

