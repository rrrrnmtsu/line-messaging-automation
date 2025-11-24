// Notion MCP のツール一覧を確認
import { exec } from 'child_process';

exec('claude mcp list --json', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  
  try {
    const data = JSON.parse(stdout);
    const notionServer = data.servers?.find(s => s.name === 'notion');
    if (notionServer) {
      console.log('Notion MCP Tools:');
      console.log(JSON.stringify(notionServer.tools || [], null, 2));
    } else {
      console.log('Notion MCP not found');
    }
  } catch (e) {
    console.log('Available MCP tools check - using mcp__notion__* pattern');
  }
});
