import jwt from 'jsonwebtoken';

const config = {
  botId: process.env.LINEWORKS_BOT_ID,
  botSecret: process.env.LINEWORKS_BOT_SECRET,
  privateKey: process.env.LINEWORKS_PRIVATE_KEY
};

/**
 * LINE WORKS Server API用のJWTトークンを生成
 */
export function generateJWT() {
  const iat = Math.floor(Date.now() / 1000);
  const exp = iat + (60 * 60); // 1時間有効

  const payload = {
    iss: config.botId,
    iat: iat,
    exp: exp
  };

  try {
    const token = jwt.sign(payload, config.privateKey, {
      algorithm: 'RS256'
    });

    return token;
  } catch (error) {
    console.error('JWT生成エラー:', error);
    throw error;
  }
}

/**
 * LINE WORKSアクセストークンを取得
 */
export async function getAccessToken() {
  const jwtToken = generateJWT();

  const response = await fetch('https://auth.worksmobile.com/oauth2/v2.0/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      assertion: jwtToken,
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      client_id: config.botId,
      client_secret: config.botSecret,
      scope: 'bot'
    })
  });

  if (!response.ok) {
    const error = await response.text();
    console.error('アクセストークン取得エラー:', error);
    throw new Error(`Failed to get access token: ${response.status}`);
  }

  const data = await response.json();
  return data.access_token;
}

// トークンキャッシュ（メモリベース）
let cachedToken = null;
let tokenExpiry = null;

/**
 * キャッシュ付きアクセストークン取得
 */
export async function getCachedAccessToken() {
  const now = Date.now();

  // キャッシュが有効な場合は返す
  if (cachedToken && tokenExpiry && now < tokenExpiry) {
    return cachedToken;
  }

  // 新しいトークンを取得
  cachedToken = await getAccessToken();
  tokenExpiry = now + (50 * 60 * 1000); // 50分後に期限切れ（実際は1時間だが余裕を持たせる）

  return cachedToken;
}
