export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Handle message posting
    if (request.method === "POST") {
      const formData = await request.formData();
      const message = formData.get("msg");
      const language = formData.get("lang") || "javascript";

      if (message) {
        const id = Date.now().toString();
        const codeData = JSON.stringify({ 
          code: message, 
          language: language, 
          timestamp: new Date().toISOString() 
        });
        await env.CHAT_KV.put(id, codeData, { expirationTtl: 7200 }); // expire in 2h
      }
      return Response.redirect(url.origin, 303);
    }

    // Handle displaying code shares
    let list = await env.CHAT_KV.list();
    let messages = [];
    for (let key of list.keys) {
      let msg = await env.CHAT_KV.get(key.name);
      if (msg) {
        try {
          const parsed = JSON.parse(msg);
          messages.push({ id: key.name, ...parsed });
        } catch {
          // Handle legacy plain text messages
          messages.push({ 
            id: key.name, 
            code: msg, 
            language: "javascript", 
            timestamp: new Date().toISOString() 
          });
        }
      }
    }
    messages.sort((a, b) => b.id.localeCompare(a.id)); // Latest first

    // HTML escape function
    const escapeHtml = (text) => {
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    };

    // Build enhanced HTML
    let html = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Code Share Platform</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
      <style>
        * { box-sizing: border-box; }
        body { 
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
          margin: 0; 
          padding: 20px; 
          min-height: 100vh; 
          line-height: 1.6;
        }
        
        .container { 
          max-width: 1200px; 
          margin: 0 auto; 
          background: rgba(255,255,255,0.95); 
          border-radius: 20px; 
          box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
          backdrop-filter: blur(10px);
          overflow: hidden;
        }
        
        .header {
          background: linear-gradient(135deg, #2c3e50, #3498db);
          color: white;
          padding: 30px;
          text-align: center;
        }
        
        .header h1 {
          margin: 0;
          font-size: 2.5rem;
          font-weight: 300;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 15px;
        }
        
        .main-content {
          padding: 30px;
        }
        
        .submit-form {
          background: #f8f9fa;
          padding: 25px;
          border-radius: 15px;
          margin-bottom: 30px;
          border: 2px solid #e9ecef;
        }
        
        .form-group {
          margin-bottom: 20px;
        }
        
        .form-group label {
          display: block;
          margin-bottom: 8px;
          font-weight: 600;
          color: #2c3e50;
        }
        
        .form-row {
          display: flex;
          gap: 15px;
          align-items: end;
        }
        
        .form-row select {
          padding: 12px;
          border: 2px solid #ddd;
          border-radius: 8px;
          background: white;
          min-width: 150px;
        }
        
        .code-input {
          width: 100%;
          min-height: 150px;
          padding: 15px;
          border: 2px solid #ddd;
          border-radius: 8px;
          font-family: 'Courier New', Monaco, monospace;
          font-size: 14px;
          resize: vertical;
          transition: border-color 0.3s ease;
        }
        
        .code-input:focus {
          outline: none;
          border-color: #3498db;
          box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        
        .submit-btn {
          background: linear-gradient(135deg, #3498db, #2ecc71);
          color: white;
          border: none;
          padding: 12px 30px;
          border-radius: 25px;
          cursor: pointer;
          font-size: 16px;
          font-weight: 600;
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .submit-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        
        .code-item {
          background: white;
          border-radius: 12px;
          margin-bottom: 25px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.1);
          border: 1px solid #e9ecef;
          overflow: hidden;
          transition: transform 0.2s ease;
        }
        
        .code-item:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .code-header {
          background: linear-gradient(135deg, #34495e, #2c3e50);
          color: white;
          padding: 15px 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 10px;
        }
        
        .code-meta {
          display: flex;
          align-items: center;
          gap: 15px;
          flex-wrap: wrap;
        }
        
        .lang-badge {
          background: rgba(255,255,255,0.2);
          padding: 4px 12px;
          border-radius: 15px;
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
        }
        
        .timestamp {
          font-size: 12px;
          opacity: 0.8;
        }
        
        .code-actions {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }
        
        .action-btn {
          background: rgba(255,255,255,0.2);
          border: none;
          color: white;
          padding: 8px 12px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 12px;
          transition: background-color 0.2s ease;
          display: flex;
          align-items: center;
          gap: 5px;
        }
        
        .action-btn:hover {
          background: rgba(255,255,255,0.3);
        }
        
        .code-container {
          position: relative;
        }
        
        .code-frame {
          max-height: 300px;
          overflow: auto;
          margin: 0;
          border: none;
          background: #2d3748;
        }
        
        .code-frame.expanded {
          max-height: none;
        }
        
        .code-frame pre {
          margin: 0 !important;
          padding: 20px !important;
          background: transparent !important;
        }
        
        .code-frame code {
          font-family: 'Courier New', Monaco, monospace;
          font-size: 14px;
          line-height: 1.5;
        }
        
        .expand-overlay {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          height: 50px;
          background: linear-gradient(transparent, rgba(45, 55, 72, 0.9));
          display: flex;
          align-items: end;
          justify-content: center;
          padding-bottom: 10px;
        }
        
        .expand-btn {
          background: #3498db;
          color: white;
          border: none;
          padding: 6px 12px;
          border-radius: 15px;
          cursor: pointer;
          font-size: 12px;
          font-weight: 600;
        }
        
        .empty-state {
          text-align: center;
          padding: 60px 20px;
          color: #7f8c8d;
        }
        
        .empty-state svg {
          width: 80px;
          height: 80px;
          margin-bottom: 20px;
          opacity: 0.5;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
          body { padding: 10px; }
          .header h1 { font-size: 2rem; }
          .main-content { padding: 20px; }
          .submit-form { padding: 20px; }
          .form-row { flex-direction: column; align-items: stretch; }
          .code-header { flex-direction: column; align-items: stretch; text-align: center; }
          .code-meta, .code-actions { justify-content: center; }
          .code-frame pre { padding: 15px !important; }
          .code-frame code { font-size: 12px; }
        }
        
        @media (max-width: 480px) {
          .header { padding: 20px 15px; }
          .header h1 { font-size: 1.5rem; }
          .main-content { padding: 15px; }
          .submit-form { padding: 15px; }
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0L19.2 12l-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
            </svg>
            Code Share Platform
          </h1>
        </div>
        
        <div class="main-content">
          <div class="submit-form">
            <form method="POST">
              <div class="form-group">
                <label for="code">Share Your Code:</label>
                <textarea name="msg" id="code" class="code-input" placeholder="Paste your code here..." required></textarea>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="lang">Language:</label>
                  <select name="lang" id="lang">
                    <option value="javascript">JavaScript</option>
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="c">C</option>
                    <option value="csharp">C#</option>
                    <option value="php">PHP</option>
                    <option value="ruby">Ruby</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                    <option value="html">HTML</option>
                    <option value="css">CSS</option>
                    <option value="sql">SQL</option>
                    <option value="json">JSON</option>
                    <option value="xml">XML</option>
                    <option value="markdown">Markdown</option>
                    <option value="yaml">YAML</option>
                    <option value="bash">Bash</option>
                  </select>
                </div>
                <button type="submit" class="submit-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 5px;">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                  </svg>
                  Share Code
                </button>
              </div>
            </form>
          </div>
          
          <div id="messages">
            ${messages.length === 0 ? `
              <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0L19.2 12l-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
                </svg>
                <h3>No code shared yet</h3>
                <p>Be the first to share some code!</p>
              </div>
            ` : messages.map((m, index) => `
              <div class="code-item" data-id="${m.id}">
                <div class="code-header">
                  <div class="code-meta">
                    <span class="lang-badge">${escapeHtml(m.language)}</span>
                    <span class="timestamp">${new Date(m.timestamp).toLocaleString()}</span>
                  </div>
                  <div class="code-actions">
                    <button class="action-btn" onclick="copyCode('${m.id}')">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                      </svg>
                      Copy
                    </button>
                    <button class="action-btn" onclick="downloadCode('${m.id}', '${escapeHtml(m.language)}')">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/>
                      </svg>
                      Download
                    </button>
                  </div>
                </div>
                <div class="code-container">
                  <div class="code-frame" id="frame-${m.id}">
                    <pre><code class="language-${escapeHtml(m.language)}" id="code-${m.id}">${escapeHtml(m.code)}</code></pre>
                  </div>
                  ${m.code.split('\n').length > 10 ? `
                    <div class="expand-overlay" id="overlay-${m.id}">
                      <button class="expand-btn" onclick="toggleExpand('${m.id}')">Show More</button>
                    </div>
                  ` : ''}
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      </div>

      <script>
        // Auto-refresh every 30 seconds (increased from 5 seconds for better UX)
        let refreshInterval = setInterval(() => { 
          if (!document.hidden) location.reload(); 
        }, 30000);
        
        // Pause refresh when tab is not visible
        document.addEventListener('visibilitychange', () => {
          if (document.hidden) {
            clearInterval(refreshInterval);
          } else {
            refreshInterval = setInterval(() => { location.reload(); }, 30000);
          }
        });

        // Copy code to clipboard
        async function copyCode(id) {
          const codeElement = document.getElementById('code-' + id);
          const code = codeElement.textContent;
          
          try {
            await navigator.clipboard.writeText(code);
            showNotification('Code copied to clipboard!', 'success');
          } catch (err) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = code;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Code copied to clipboard!', 'success');
          }
        }

        // Download code as file
        function downloadCode(id, language) {
          const codeElement = document.getElementById('code-' + id);
          const code = codeElement.textContent;
          
          const extensions = {
            javascript: 'js', python: 'py', java: 'java', cpp: 'cpp', 
            c: 'c', csharp: 'cs', php: 'php', ruby: 'rb', go: 'go', 
            rust: 'rs', html: 'html', css: 'css', sql: 'sql', 
            json: 'json', xml: 'xml', markdown: 'md', yaml: 'yml', 
            bash: 'sh'
          };
          
          const extension = extensions[language] || 'txt';
          const filename = \`code-\${id}.\${extension}\`;
          
          const blob = new Blob([code], { type: 'text/plain' });
          const url = URL.createObjectURL(blob);
          
          const a = document.createElement('a');
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
          
          showNotification(\`Downloaded as \${filename}\`, 'success');
        }

        // Toggle expand/collapse code
        function toggleExpand(id) {
          const frame = document.getElementById('frame-' + id);
          const overlay = document.getElementById('overlay-' + id);
          const button = overlay.querySelector('.expand-btn');
          
          if (frame.classList.contains('expanded')) {
            frame.classList.remove('expanded');
            overlay.style.display = 'flex';
            button.textContent = 'Show More';
          } else {
            frame.classList.add('expanded');
            overlay.style.display = 'none';
            button.textContent = 'Show Less';
          }
        }

        // Show notification
        function showNotification(message, type = 'info') {
          const notification = document.createElement('div');
          notification.style.cssText = \`
            position: fixed; top: 20px; right: 20px; z-index: 1000;
            background: \${type === 'success' ? '#2ecc71' : '#3498db'};
            color: white; padding: 12px 20px; border-radius: 8px;
            font-weight: 600; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            animation: slideIn 0.3s ease-out;
          \`;
          notification.textContent = message;
          
          const style = document.createElement('style');
          style.textContent = \`
            @keyframes slideIn {
              from { transform: translateX(100%); opacity: 0; }
              to { transform: translateX(0); opacity: 1; }
            }
          \`;
          document.head.appendChild(style);
          
          document.body.appendChild(notification);
          
          setTimeout(() => {
            notification.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => notification.remove(), 300);
          }, 3000);
        }

        // Initialize syntax highlighting
        document.addEventListener('DOMContentLoaded', () => {
          if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
          }
        });
      </script>
    </body>
    </html>
    `;

    return new Response(html, { headers: { "Content-Type": "text/html" } });
  }
};
