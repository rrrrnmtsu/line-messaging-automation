import { getCachedAccessToken } from './lib/auth.js';

export default async function handler(req, res) {
  try {
    console.log('Testing LINE WORKS authentication...');
    console.log('BOT_ID:', process.env.LINEWORKS_BOT_ID);
    console.log('BOT_SECRET exists:', !!process.env.LINEWORKS_BOT_SECRET);
    console.log('PRIVATE_KEY exists:', !!process.env.LINEWORKS_PRIVATE_KEY);

    const token = await getCachedAccessToken();

    res.status(200).json({
      success: true,
      message: 'Authentication successful',
      tokenPreview: token.substring(0, 20) + '...'
    });
  } catch (error) {
    console.error('Authentication failed:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      stack: error.stack
    });
  }
}
