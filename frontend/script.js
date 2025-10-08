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

  // 랜덤 placeholder 설정
  const placeholders = [
    "세미나 안내문을 만들어줘. 모던하고 전문적인 느낌으로, 파란색 계열을 중심으로 디자인해줘. 아이콘은 적절히 넣고, 너무 화려하지 않게",
    "카페 이벤트 전단지를 따뜻하고 아늑한 분위기로 만들어줘. 베이지와 브라운 톤을 사용하고, 여백을 충분히 둬서 깔끔하게. 손글씨 느낌의 폰트로",
    "학원 수업 교재를 디자인해줘. 학생들이 집중하기 좋게 깔끔하고 구조화된 레이아웃으로. 중요한 내용은 하이라이트 박스로 강조하고, 삽화는 최소화해줘",
    "부동산 매물 안내서를 고급스럽고 신뢰감 있게 만들어줘. 다크 네이비와 골드 포인트를 사용하고, 사진이 돋보이도록 여백을 많이 둬. 과도한 장식은 빼줘",
    "동아리 모집 포스터를 만들어줘. 젊고 역동적인 느낌으로, 밝은 컬러를 과감하게 써. 그라데이션 효과를 넣고, 타이포그래피를 크고 임팩트 있게",
    "회사 보고서 표지를 미니멀하고 전문적으로 디자인해줘. 흰색과 회색 위주로 하고, 한 가지 포인트 컬러만 사용해. 도형이나 패턴은 넣지 마",
    "요가 클래스 안내문을 자연스럽고 평화로운 느낌으로 만들어줘. 연한 그린과 화이트 조합으로, 여백을 여유롭게. 손그림 스타일 일러스트를 포함해줘",
    "제품 설명서를 직관적이고 읽기 쉽게 디자인해줘. 단계별로 명확하게 구분하고, 아이콘과 번호를 활용해. 복잡한 배경은 쓰지 말고 화이트 베이스로"
  ];
  const randomPlaceholder = placeholders[Math.floor(Math.random() * placeholders.length)];
  if (promptEl) promptEl.placeholder = randomPlaceholder;

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
  const dropzoneEmpty = document.getElementById('dropzoneEmpty');
  
  function refreshFileList(files) {
    if (!files || files.length === 0) { 
      // 파일이 없으면 기본 안내 문구 표시
      dropzoneEmpty.classList.remove('hidden');
      fileList.innerHTML = ''; 
      return; 
    }
    
    // 파일이 있으면 기본 안내 문구 숨기기
    dropzoneEmpty.classList.add('hidden');
    
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
      // PDF 미리보기 (download=false)
      window.open(currentResult.url, '_blank');
    } else {
      // HTML 미리보기
      window.open(currentResult.url, '_blank');
    }
  });

  modalPdfBtn.addEventListener('click', () => {
    // PDF 다운로드 (download=true 파라미터 추가)
    const downloadUrl = currentResult.url + '?download=true';
    const a = document.createElement('a');
    a.href = downloadUrl;
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

    // 파일 크기 검증 (프론트엔드)
    if (fileInput.files && fileInput.files.length > 0) {
      let totalSize = 0;
      for (let file of fileInput.files) {
        totalSize += file.size;
      }
      const maxSize = 20 * 1024 * 1024; // 20MB
      if (totalSize > maxSize) {
        statusEl.innerHTML = `<span class="text-red-600">파일 크기가 너무 큽니다. 현재: ${(totalSize / 1024 / 1024).toFixed(2)}MB, 최대: 20MB</span>`;
        return;
      }
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

      // 타임아웃 설정 (5분)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5 * 60 * 1000);

      const res = await fetch(`${API_BASE}/api/convert`, { 
        method: 'POST', 
        body: fd,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
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
      let errorMessage = '오류가 발생했습니다.';
      
      if (err.name === 'AbortError') {
        errorMessage = '처리 시간이 너무 오래 걸립니다. 파일 크기를 줄이거나 나중에 다시 시도해주세요.';
      } else if (err.message === 'Failed to fetch') {
        errorMessage = '서버에 연결할 수 없습니다. 다음을 확인해주세요:\n• 인터넷 연결 상태\n• 1분에 10회 이상 요청하지 않았는지\n• 서버가 시작 중인지 (최초 30초 소요)';
      } else {
        errorMessage = err.message || '오류가 발생했습니다.';
      }
      
      statusEl.innerHTML = `<div class="text-red-600 whitespace-pre-line">${errorMessage}</div>`;
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
