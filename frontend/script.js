// DOMContentLoaded로 모든 엘리먼트가 준비된 뒤에만 코드 실행 + async로 'await' 사용 허용
document.addEventListener('DOMContentLoaded', async function () {
  // ====== Config ======
  // 배포 후 백엔드 URL로 교체하세요. 예: https://your-backend.onrender.com
  const API_BASE = window.location.hostname === 'localhost' 
      ? 'http://localhost:5000' 
      : 'https://your-backend.onrender.com';

  // ====== Elements ======
  const promptEl   = document.getElementById('prompt');
  const generateBtn= document.getElementById('generateBtn');
  const dropzone   = document.getElementById('dropzone');
  const fileInput  = document.getElementById('fileInput');
  const fileList   = document.getElementById('fileList');
  const spinner    = document.getElementById('spinner');
  const statusEl   = document.getElementById('status');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const yearEl     = document.getElementById('year');

  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ====== Guard: 필수 요소 점검 ======
  const required = [
    ['prompt', promptEl], ['generateBtn', generateBtn], ['dropzone', dropzone],
    ['fileInput', fileInput], ['fileList', fileList], ['status', statusEl]
  ];
  let guardsOk = true;
  required.forEach(([k, el]) => { 
    const ok = !!el; 
    if(!ok) {
      console.error(`Element #${k} not found`);
      guardsOk = false;
    }
  });
  if (!guardsOk) {
    statusEl && (statusEl.textContent = '초기화 오류: 필수 요소를 찾지 못했습니다.');
    return; // 더 진행하지 않음
  }

  // ====== Textarea auto-grow (with cap) ======
  function autoGrow(el) {
    el.style.height = 'auto';
    const max = 256; // px
    const newH = Math.min(el.scrollHeight, max);
    el.style.height = newH + 'px';
    el.style.overflowY = (el.scrollHeight > max) ? 'auto' : 'hidden';
  }
  promptEl.addEventListener('input', () => autoGrow(promptEl));
  autoGrow(promptEl); // 초기 적용

  // ====== Dropzone interactions ======
  function refreshFileList(files) {
    if (!files || files.length === 0) { 
      fileList.innerHTML = ''; 
      return; 
    }
    let html = '<div class="mt-3 space-y-2">';
    Array.from(files).forEach((f, index) => {
      const fileName = f.name.length > 30 ? f.name.substring(0, 30) + '...' : f.name;
      html += `
        <div class="flex items-center justify-between px-3 py-2 bg-slate-100 dark:bg-slate-800 rounded-lg">
          <div class="flex items-center gap-2">
            <span class="text-sm">${getFileIcon(f.name)}</span>
            <span class="text-sm font-medium">${fileName}</span>
            <span class="text-xs text-slate-400">(${(f.size/1024/1024).toFixed(2)} MB)</span>
          </div>
          <button onclick="removeFile(${index})" class="text-slate-400 hover:text-red-500 text-sm">×</button>
        </div>
      `;
    });
    html += '</div>';
    fileList.innerHTML = html;
  }

  function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
      'pdf': '📄', 'doc': '📝', 'docx': '📝', 'xls': '📊', 'xlsx': '📊',
      'ppt': '📽️', 'pptx': '📽️', 'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 
      'gif': '🖼️', 'txt': '📃', 'md': '📃', 'json': '⚙️', 'xml': '⚙️',
      'html': '🌐', 'htm': '🌐', 'zip': '📦', 'epub': '📚'
    };
    return icons[ext] || '📄';
  }

  // 파일 제거 함수를 전역으로 노출
  window.removeFile = function(index) {
    const dt = new DataTransfer();
    Array.from(fileInput.files).forEach((file, i) => {
      if (i !== index) dt.items.add(file);
    });
    fileInput.files = dt.files;
    refreshFileList(fileInput.files);
  };

  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('dragover', (e) => { 
    e.preventDefault(); 
    dropzone.classList.add('ring-2','ring-slate-400'); 
  });
  dropzone.addEventListener('dragleave', () => 
    dropzone.classList.remove('ring-2','ring-slate-400')
  );
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('ring-2','ring-slate-400');
    if (e.dataTransfer.files && e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      refreshFileList(fileInput.files);
    }
  });
  fileInput.addEventListener('change', () => refreshFileList(fileInput.files));

  // ====== Generate handler ======
  async function generate() {
    const prompt = (promptEl.value || '').trim();
    if (!prompt && (!fileInput.files || fileInput.files.length === 0)) {
      statusEl.textContent = '프롬프트 또는 파일 중 하나는 입력해야 합니다.';
      return;
    }

    // === Loading ON ===
    setLoading(true);
    statusEl.textContent = '생성 중… 잠시만 기다려 주세요';

    try {
      const fd = new FormData();
      fd.append('prompt', prompt);
      if (fileInput.files && fileInput.files.length) {
        Array.from(fileInput.files).forEach((f) => fd.append('files', f));
      }

      const res = await fetch(`${API_BASE}/api/convert`, { method: 'POST', body: fd });
      const j = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(j.error || `서버 오류 (${res.status})`);
      }
      if (j && j.pdf_url) {
        statusEl.innerHTML = `완료! <a class="text-blue-600 underline" href="${API_BASE}${j.pdf_url}" target="_blank" rel="noopener">PDF 다운로드</a>`;
      } else if (j && j.html) {
        // PDF 변환이 실패한 경우 HTML만 제공
        statusEl.innerHTML = `HTML 생성 완료! (PDF 변환 불가)`;
      } else {
        statusEl.textContent = 'PDF 링크를 받지 못했습니다.';
      }
    } catch (err) {
      statusEl.textContent = err.message || '오류가 발생했습니다.';
    } finally {
      // === Loading OFF ===
      setLoading(false);
    }
  }

  function setLoading(isLoading){
    generateBtn.disabled = !!isLoading;
    // 버튼 텍스트/모션
    if (isLoading){
      generateBtn.dataset.prev = generateBtn.textContent;
      generateBtn.textContent = '생성 중';
      if (!generateBtn.querySelector('.dots')){
        const s = document.createElement('span'); 
        s.className='dots'; 
        s.textContent='';
        generateBtn.appendChild(s);
      }
      loadingOverlay && loadingOverlay.classList.remove('hidden');
      dropzone.classList.add('pointer-events-none','opacity-60');
      promptEl.setAttribute('aria-busy','true');
    } else {
      if (generateBtn.dataset.prev){ 
        generateBtn.textContent = generateBtn.dataset.prev; 
      }
      const d = generateBtn.querySelector('.dots'); 
      if (d) d.remove();
      loadingOverlay && loadingOverlay.classList.add('hidden');
      dropzone.classList.remove('pointer-events-none','opacity-60');
      promptEl.removeAttribute('aria-busy');
    }
  }

  generateBtn.addEventListener('click', generate);
  
  // Enter+Ctrl/Cmd = 전송 단축키 (채팅 UX 유사)
  promptEl.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      generate();
    }
  });

  // 기본 프롬프트 설정
  promptEl.value = "해당 파일을 기반으로 영어 단어장을 새롭게 디자인해줘.";
  autoGrow(promptEl);

  // API 서버 상태 체크
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    if (response.ok) {
      console.log('✅ 서버 연결 정상');
    } else {
      console.warn('⚠️ 서버 응답 이상');
    }
  } catch (error) {
    console.error('❌ 서버 연결 실패:', error);
    statusEl.textContent = 'AI 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.';
  }
});
