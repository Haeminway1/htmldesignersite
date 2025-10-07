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
  const resultModal = document.getElementById('resultModal');
  const modalPreviewBtn = document.getElementById('modalPreviewBtn');
  const modalPdfBtn = document.getElementById('modalPdfBtn');
  const modalHtmlBtn = document.getElementById('modalHtmlBtn');
  const modalEditBtn = document.getElementById('modalEditBtn');
  const modalCloseBtn = document.getElementById('modalCloseBtn');

  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // 현재 생성된 결과 저장
  let currentResult = {
    html: '',
    url: '',
    type: '', // 'pdf' or 'html'
    filename: '',
    originalPrompt: ''
  };

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
            <span class="text-sm font-medium text-slate-900">${fileName}</span>
            <span class="text-xs text-slate-500">(${(f.size/1024/1024).toFixed(2)} MB)</span>
          </div>
          <button onclick="event.stopPropagation(); event.preventDefault(); removeFile(${index})" class="text-slate-400 hover:text-red-600 text-xl px-2 transition-colors" aria-label="파일 삭제">×</button>
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

  // ====== Result Modal Functions ======
  function showResultModal(html, url, type, filename = '') {
    currentResult = {
      html: html,
      url: url,
      type: type,
      filename: filename || `handout_${new Date().toISOString().slice(0,10)}.${type === 'pdf' ? 'pdf' : 'html'}`,
      originalPrompt: promptEl.value
    };

    // PDF 버튼 표시/숨김
    if (type === 'pdf') {
      modalPdfBtn.classList.remove('hidden');
    } else {
      modalPdfBtn.classList.add('hidden');
    }

    resultModal.classList.remove('hidden');
    resultModal.classList.add('flex');
    document.body.style.overflow = 'hidden';
  }

  function hideResultModal() {
    resultModal.classList.add('hidden');
    resultModal.classList.remove('flex');
    document.body.style.overflow = '';
  }

  // 모달 버튼 이벤트
  modalPreviewBtn.addEventListener('click', () => {
    if (currentResult.type === 'pdf') {
      window.open(currentResult.url, '_blank');
    } else {
      window.open(currentResult.url, '_blank');
    }
  });

  modalPdfBtn.addEventListener('click', () => {
    const a = document.createElement('a');
    a.href = currentResult.url;
    a.download = currentResult.filename;
    a.click();
  });

  modalHtmlBtn.addEventListener('click', () => {
    const blob = new Blob([currentResult.html], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = currentResult.filename.replace('.pdf', '.html');
    a.click();
    URL.revokeObjectURL(url);
  });

  modalEditBtn.addEventListener('click', () => {
    // 프롬프트를 .md 파일로 추가
    const promptBlob = new Blob([currentResult.originalPrompt], { type: 'text/markdown;charset=utf-8' });
    const promptFile = new File([promptBlob], 'prompt.md', { type: 'text/markdown' });

    // 결과물을 .html 파일로 추가
    const htmlBlob = new Blob([currentResult.html], { type: 'text/html;charset=utf-8' });
    const htmlFile = new File([htmlBlob], 'result.html', { type: 'text/html' });

    // DataTransfer로 파일 추가
    const dt = new DataTransfer();
    
    // 기존 파일들 먼저 추가
    if (fileInput.files) {
      Array.from(fileInput.files).forEach(file => dt.items.add(file));
    }
    
    // 새 파일들 추가
    dt.items.add(promptFile);
    dt.items.add(htmlFile);
    
    fileInput.files = dt.files;
    refreshFileList(fileInput.files);

    // 프롬프트 창 비우기
    promptEl.value = '';
    autoGrow(promptEl);

    // 모달 닫기
    hideResultModal();

    // 상태 메시지 업데이트
    statusEl.textContent = '이전 결과물이 추가되었습니다. 수정 사항을 입력하고 다시 생성하세요.';
  });

  modalCloseBtn.addEventListener('click', hideResultModal);

  // 모달 배경 클릭 시 닫기
  resultModal.addEventListener('click', (e) => {
    if (e.target === resultModal) {
      hideResultModal();
    }
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
    statusEl.textContent = '';

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
        
        // HTML 가져오기 (없으면 빈 문자열)
        const htmlContent = j.html || '';
        
        // 생성 완료 팝업 표시
        showResultModal(htmlContent, pdfUrl, 'pdf');
      } else if (j && j.html) {
        // PDF 변환 실패, HTML만 제공
        const blob = new Blob([j.html], { type: 'text/html;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const filename = `handout_${new Date().toISOString().slice(0,10)}.html`;
        
        // 생성 완료 팝업 표시
        showResultModal(j.html, url, 'html', filename);
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
