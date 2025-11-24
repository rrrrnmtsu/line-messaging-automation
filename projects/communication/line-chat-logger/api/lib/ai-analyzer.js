// AI分析モジュール（プロジェクト管理用）

/**
 * メッセージからタスクを抽出
 */
export function extractTasks(content) {
  const tasks = [];

  // タスク検出パターン
  const taskPatterns = [
    /(.+)を(作成|実装|確認|修正|テスト|デプロイ|レビュー)する/g,
    /(.+)を(やる|行う|進める)/g,
    /(.+)(してください|お願いします)/g,
    /TODO[:\s]*(.+)/gi,
    /\[?\s*タスク\s*\]?\s*[:\s]*(.+)/gi
  ];

  taskPatterns.forEach(pattern => {
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      const task = match[1] || match[0];
      if (task && task.length > 2 && task.length < 100) {
        tasks.push({
          content: task.trim(),
          detectedPattern: pattern.source
        });
      }
    }
  });

  return tasks;
}

/**
 * 進捗ステータス検出
 */
export function detectProgress(content) {
  const progressPatterns = {
    completed: ['完了', '終わった', '完成', 'done', '済み', 'finished'],
    in_progress: ['進行中', '作業中', '対応中', '進めています', 'やっています'],
    blocked: ['困っている', 'ブロック', '止まっている', '待ち', 'できない'],
    pending: ['未着手', 'これから', '予定']
  };

  const lowerContent = content.toLowerCase();

  for (const [status, keywords] of Object.entries(progressPatterns)) {
    if (keywords.some(keyword => lowerContent.includes(keyword))) {
      return {
        status,
        confidence: 0.8
      };
    }
  }

  return null;
}

/**
 * ボトルネック検出
 */
export function detectBottleneck(content) {
  const bottleneckKeywords = [
    '困っている', '問題', '課題', 'うまくいかない',
    'エラー', '動かない', '分からない', '詰まっている',
    '時間がかかる', '難しい', 'ブロック'
  ];

  const found = bottleneckKeywords.filter(keyword =>
    content.includes(keyword)
  );

  if (found.length > 0) {
    return {
      detected: true,
      keywords: found,
      severity: found.length >= 2 ? 'high' : 'medium'
    };
  }

  return { detected: false };
}

/**
 * リスク検出
 */
export function detectRisk(content) {
  const riskPatterns = {
    schedule: ['遅れ', '遅延', '間に合わない', '期限', 'deadline'],
    technical: ['バグ', 'エラー', '不具合', '障害', '問題発生'],
    resource: ['人手不足', 'リソース', '時間が足りない', '工数'],
    quality: ['品質', 'テスト失敗', 'レビュー指摘', '仕様違い']
  };

  const risks = [];

  for (const [category, keywords] of Object.entries(riskPatterns)) {
    const found = keywords.filter(keyword => content.includes(keyword));
    if (found.length > 0) {
      risks.push({
        category,
        keywords: found,
        severity: calculateRiskSeverity(content, found)
      });
    }
  }

  return risks;
}

/**
 * リスク深刻度計算
 */
function calculateRiskSeverity(content, keywords) {
  const highSeverityWords = ['緊急', '重大', '致命的', 'クリティカル', '即対応'];
  const hasHighSeverity = highSeverityWords.some(word => content.includes(word));

  if (hasHighSeverity || keywords.length >= 3) return 'high';
  if (keywords.length >= 2) return 'medium';
  return 'low';
}

/**
 * 優先度判定
 */
export function detectPriority(content) {
  const urgentKeywords = ['緊急', '至急', 'ASAP', '今すぐ', '急ぎ'];
  const importantKeywords = ['重要', '必須', 'critical', 'important', '優先'];

  const isUrgent = urgentKeywords.some(keyword => content.toLowerCase().includes(keyword.toLowerCase()));
  const isImportant = importantKeywords.some(keyword => content.toLowerCase().includes(keyword.toLowerCase()));

  if (isUrgent && isImportant) return 'critical';
  if (isUrgent) return 'high';
  if (isImportant) return 'medium';
  return 'low';
}

/**
 * 包括的分析
 */
export function analyzeMessage(messageData) {
  const content = messageData.content;

  const analysis = {
    messageId: messageData.messageId,
    timestamp: messageData.timestamp,
    userId: messageData.userId,
    userName: messageData.userName,
    sourceType: messageData.sourceType,
    groupId: messageData.groupId,
    groupName: messageData.groupName,

    // 分析結果
    tasks: extractTasks(content),
    progress: detectProgress(content),
    bottleneck: detectBottleneck(content),
    risks: detectRisk(content),
    priority: detectPriority(content),

    // メタ情報
    analyzedAt: new Date().toISOString(),
    hasActionItems: false
  };

  // アクションアイテム判定
  analysis.hasActionItems =
    analysis.tasks.length > 0 ||
    analysis.bottleneck.detected ||
    analysis.risks.length > 0;

  return analysis;
}

/**
 * プロジェクトサマリー生成
 */
export function generateProjectSummary(messages) {
  const allTasks = [];
  const allRisks = [];
  const bottlenecks = [];
  const progressByUser = {};

  messages.forEach(msg => {
    const analysis = analyzeMessage(msg);

    allTasks.push(...analysis.tasks);
    allRisks.push(...analysis.risks);

    if (analysis.bottleneck.detected) {
      bottlenecks.push({
        user: msg.userName,
        content: msg.content,
        severity: analysis.bottleneck.severity
      });
    }

    if (analysis.progress) {
      if (!progressByUser[msg.userName]) {
        progressByUser[msg.userName] = [];
      }
      progressByUser[msg.userName].push(analysis.progress.status);
    }
  });

  return {
    totalMessages: messages.length,
    totalTasks: allTasks.length,
    totalRisks: allRisks.length,
    totalBottlenecks: bottlenecks.length,
    risksByCategory: groupBy(allRisks, 'category'),
    bottlenecksBySeverity: groupBy(bottlenecks, 'severity'),
    progressByUser,
    generatedAt: new Date().toISOString()
  };
}

/**
 * ヘルパー関数: グループ化
 */
function groupBy(array, key) {
  return array.reduce((result, item) => {
    const group = item[key];
    if (!result[group]) result[group] = [];
    result[group].push(item);
    return result;
  }, {});
}
