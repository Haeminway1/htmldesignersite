// DOMContentLoaded로 모든 엘리먼트가 준비된 뒤에만 코드 실행 + async로 'await' 사용 허용
document.addEventListener('DOMContentLoaded', async function () {
  // ====== Config ======
  // 배포 후 백엔드 URL로 교체하세요. 예: https://your-backend.onrender.com
  const API_BASE = window.location.hostname === 'localhost' 
      ? 'http://localhost:5000' 
      : 'https://htmldesignersite.onrender.com';

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
    let html = `
      <div class="mt-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-slate-700">첨부 파일 (${files.length}개)</span>
          <button onclick="event.stopPropagation(); event.preventDefault(); clearAllFiles()" class="text-xs text-red-600 hover:text-red-700 font-medium transition-colors">
            전체 제거
          </button>
        </div>
        <div class="space-y-2">
    `;
    Array.from(files).forEach((f, index) => {
      const fileName = f.name.length > 30 ? f.name.substring(0, 30) + '...' : f.name;
      html += `
        <div class="flex items-center justify-between px-4 py-3 bg-slate-50 rounded-xl border border-slate-200">
          <div class="flex items-center gap-3">
            <span class="text-lg">${getFileIcon(f.name)}</span>
            <span class="text-sm font-medium text-slate-900">${fileName}</span>
            <span class="text-xs text-slate-500">(${(f.size/1024/1024).toFixed(2)} MB)</span>
          </div>
          <button onclick="event.stopPropagation(); event.preventDefault(); removeFile(${index})" class="text-slate-400 hover:text-red-600 text-xl px-2 transition-colors" aria-label="파일 삭제">×</button>
        </div>
      `;
    });
    html += '</div></div>';
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

  // 전체 파일 제거 함수
  window.clearAllFiles = function() {
    fileInput.value = '';
    refreshFileList(null);
  };

  dropzone.addEventListener('click', (e) => {
    // 파일 리스트 영역 클릭 시에는 파일 선택창 열지 않음
    if (e.target.closest('#fileList')) {
      return;
    }
    fileInput.click();
  });
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
      // 기존 파일에 새 파일 추가 (대체가 아닌 추가)
      const dt = new DataTransfer();
      // 기존 파일들 먼저 추가
      if (fileInput.files) {
        Array.from(fileInput.files).forEach(file => dt.items.add(file));
      }
      // 새 파일들 추가
      Array.from(e.dataTransfer.files).forEach(file => dt.items.add(file));
      fileInput.files = dt.files;
      refreshFileList(fileInput.files);
    }
  });
  fileInput.addEventListener('change', (e) => {
    // 파일 선택 시에도 기존 파일에 추가
    if (e.target.files && e.target.files.length) {
      const dt = new DataTransfer();
      // 기존 파일들 먼저 추가
      const existingFiles = Array.from(fileInput.files || []);
      const newFiles = Array.from(e.target.files);
      // 중복 제거: 같은 이름의 파일은 새 파일로 대체
      const fileMap = new Map();
      existingFiles.forEach(f => fileMap.set(f.name, f));
      newFiles.forEach(f => fileMap.set(f.name, f));
      fileMap.forEach(file => dt.items.add(file));
      fileInput.files = dt.files;
      refreshFileList(fileInput.files);
    }
  });

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
        // PDF 생성 성공
        const pdfUrl = `${API_BASE}${j.pdf_url}`;
        
        // PDF 새 창에서 자동 열기
        window.open(pdfUrl, '_blank');
        
        statusEl.innerHTML = `
          <div class="space-y-4">
            <p class="text-lg font-semibold text-slate-900">✨ 생성 완료!</p>
            <div class="flex flex-wrap gap-3">
              <a class="btn-toss inline-flex items-center gap-2 px-5 py-3 bg-slate-900 text-white rounded-xl hover:bg-slate-800 font-semibold shadow-md transition-all" 
                 href="${pdfUrl}" 
                 target="_blank" 
                 rel="noopener">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                </svg>
                새 창에서 열기
              </a>
              <a class="btn-toss inline-flex items-center gap-2 px-5 py-3 bg-white text-slate-900 border-2 border-slate-900 rounded-xl hover:bg-slate-50 font-semibold transition-all" 
                 href="${pdfUrl}" 
                 download>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m.75 12l3 3m0 0l3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                </svg>
                PDF 다운로드
              </a>
            </div>
          </div>
        `;
      } else if (j && j.html) {
        // PDF 변환 실패, HTML만 제공
        const blob = new Blob([j.html], { type: 'text/html;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const filename = `handout_${new Date().toISOString().slice(0,10)}.html`;
        
        // HTML을 새 창에서 자동으로 열기
        const previewWindow = window.open(url, '_blank');
        if (previewWindow) {
          previewWindow.document.title = filename;
        }
        
        statusEl.innerHTML = `
          <div class="space-y-4">
            <p class="text-lg font-semibold text-slate-900">✨ 생성 완료!</p>
            <div class="flex flex-wrap gap-3">
              <a class="btn-toss inline-flex items-center gap-2 px-5 py-3 bg-slate-900 text-white rounded-xl hover:bg-slate-800 font-semibold shadow-md transition-all" 
                 href="${url}" 
                 target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                </svg>
                새 창에서 열기
              </a>
              <a class="btn-toss inline-flex items-center gap-2 px-5 py-3 bg-white text-slate-900 border-2 border-slate-900 rounded-xl hover:bg-slate-50 font-semibold transition-all" 
                 href="${url}" 
                 download="${filename}">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 0L7.5 4.5m.75 0l-.75.75M7.5 4.5v12m6-6l3 3m0 0l3-3m-3 3v-6" />
                </svg>
                HTML 다운로드
              </a>
              <button class="btn-toss inline-flex items-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 font-semibold shadow-md transition-all" 
                      onclick="window.print()">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0110.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0l.229 2.523a1.125 1.125 0 01-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0021 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 00-1.913-.247M6.34 18H5.25A2.25 2.25 0 013 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 011.913-.247m10.5 0a48.536 48.536 0 00-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5zm-3 0h.008v.008H15V10.5z" />
                </svg>
                PDF로 저장
              </button>
            </div>
            <p class="text-sm text-slate-600">
              💡 "PDF로 저장" 버튼을 눌러 브라우저에서 직접 PDF로 변환할 수 있습니다
            </p>
          </div>
        `;
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
    // 버튼 텍스트만 변경 (애니메이션 제거)
    if (isLoading){
      generateBtn.dataset.prev = generateBtn.textContent;
      generateBtn.textContent = '생성하기';
      loadingOverlay && loadingOverlay.classList.remove('hidden');
      dropzone.classList.add('pointer-events-none','opacity-60');
      promptEl.setAttribute('aria-busy','true');
    } else {
      if (generateBtn.dataset.prev){ 
        generateBtn.textContent = generateBtn.dataset.prev; 
      }
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

  // 프롬프트 초기값 제거 (placeholder만 표시)
  promptEl.value = "";
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
