const SYNC_ENDPOINT_KEY = 'SYNC_ENDPOINT_URL';

/**
 * メニューを追加
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Garoon連携')
    .addItem('申請データ同期', 'triggerGaroonSync')
    .addToUi();
}

/**
 * Garoon→Sheets同期を呼び出す
 */
function triggerGaroonSync() {
  const ui = SpreadsheetApp.getUi();
  ui.showToast('Garoon同期を開始します...', '実行中', 5);

  const endpoint = getSyncEndpoint();
  const payload = {
    dryRun: false,
    limit: 500,
  };

  try {
    const response = UrlFetchApp.fetch(endpoint, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true,
    });

    const statusCode = response.getResponseCode();
    if (statusCode >= 200 && statusCode < 300) {
      const body = JSON.parse(response.getContentText());
      const message = `同期完了: ${body.recordCount}件 (更新: ${body.sheetUpdated})`;
      ui.alert('Garoon同期', message, ui.ButtonSet.OK);
      ui.showToast(message, '完了', 5);
    } else {
      handleError(`HTTP ${statusCode}: ${response.getContentText()}`);
    }
  } catch (error) {
    handleError(error.message);
  }
}

/**
 * エンドポイントURLをScript Propertiesから取得
 */
function getSyncEndpoint() {
  const props = PropertiesService.getScriptProperties();
  const endpoint = props.getProperty(SYNC_ENDPOINT_KEY);
  if (!endpoint) {
    throw new Error('Script PropertiesにSYNC_ENDPOINT_URLが設定されていません');
  }
  return endpoint;
}

/**
 * エラー処理
 */
function handleError(message) {
  const ui = SpreadsheetApp.getUi();
  ui.alert('Garoon同期エラー', message, ui.ButtonSet.OK);
  ui.showToast(message, 'エラー', 10);
}
