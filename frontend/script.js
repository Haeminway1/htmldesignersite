// API 기본 URL (Render 배포 시 실제 백엔드 URL로 변경)
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : 'https://your-backend.onrender.com';  // 실제 백엔드 URL로 변경 필요

let selectedFiles = [];

// DOM 요소들
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const uploadForm = document.getElementById('uploadForm');
const generateBtn = document.getElementById('generateBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const promptTextarea = document.getElementById('prompt');

// 이벤트 리스너 등록
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateGenerateButton();
    
    // 기본 프롬프트 설정
    promptTextarea.value = "해당 파일을 기반으로 영어 단어장을 새롭게 디자인해줘.";
    
    // API 서버 상태 체크
    checkServerStatus();
});

function initializeEventListeners() {
    // 파일 업로드 영역 이벤트
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);

    // 프롬프트 자동 높이 조절
    promptTextarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        updateGenerateButton();
    });

    // 폼 제출 처리
    uploadForm.addEventListener('submit', handleFormSubmit);
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

function addFiles(files) {
    // 파일 개수 제한 체크
    if (selectedFiles.length + files.length > 20) {
        alert('최대 20개 파일까지만 업로드할 수 있습니다.');
        return;
    }

    // 파일 크기 체크 및 추가
    files.forEach(file => {
        if (file.size > 16 * 1024 * 1024) {
            alert(`파일이 너무 큽니다: ${file.name} (최대 16MB)`);
            return;
        }

        // 중복 파일 체크
        if (selectedFiles.find(f => f.name === file.name && f.size === file.size)) {
            return;
        }

        selectedFiles.push(file);
    });

    updateFileList();
    updateGenerateButton();
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
    updateGenerateButton();
}

function updateFileList() {
    fileList.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        
        const fileIcon = getFileIcon(file.name);
        const fileName = file.name.length > 30 ? file.name.substring(0, 30) + '...' : file.name;
        const fileSize = formatFileSize(file.size);
        
        fileInfo.innerHTML = `
            <span class="file-icon">${fileIcon}</span>
            <span class="file-name">${fileName}</span>
            <span class="file-size">(${fileSize})</span>
        `;
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-file';
        removeBtn.innerHTML = '×';
        removeBtn.onclick = () => removeFile(index);
        
        fileItem.appendChild(fileInfo);
        fileItem.appendChild(removeBtn);
        fileList.appendChild(fileItem);
    });
}

function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
        'pdf': '📄',
        'doc': '📝', 'docx': '📝',
        'xls': '📊', 'xlsx': '📊',
        'ppt': '📽️', 'pptx': '📽️',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
        'txt': '📃', 'md': '📃',
        'json': '⚙️', 'xml': '⚙️',
        'html': '🌐', 'htm': '🌐',
        'zip': '📦', 'epub': '📚'
    };
    return icons[ext] || '📄';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function updateGenerateButton() {
    const hasFiles = selectedFiles.length > 0;
    const hasPrompt = promptTextarea.value.trim().length > 0;
    generateBtn.disabled = !(hasFiles && hasPrompt);
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (selectedFiles.length === 0) {
        alert('최소 1개의 파일을 선택해주세요.');
        return;
    }

    const prompt = promptTextarea.value.trim();
    if (!prompt) {
        alert('생성 요청사항을 입력해주세요.');
        return;
    }

    // UI 상태 변경
    generateBtn.disabled = true;
    loading.classList.add('show');
    result.classList.remove('show');

    try {
        // FormData 생성
        const formData = new FormData();
        formData.append('prompt', prompt);
        
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        // API 호출
        const response = await fetch(`${API_BASE}/api/convert`, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (data.success) {
            showResult('success', '🎉 교재 생성 완료!', 
                `AI가 멋진 PDF 교재를 생성했습니다!<br>
                 <a href="${API_BASE}${data.pdf_url}" class="download-btn" download>📥 PDF 다운로드</a>
                 ${data.cached ? '<br><small>캐시된 결과입니다.</small>' : ''}`);
        } else {
            showResult('error', '❌ 생성 실패', data.error || '알 수 없는 오류가 발생했습니다.');
        }

    } catch (error) {
        console.error('API 호출 실패:', error);
        showResult('error', '❌ 연결 실패', 
            '서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.');
    } finally {
        generateBtn.disabled = false;
        loading.classList.remove('show');
    }
}

function showResult(type, title, message) {
    result.className = `result show ${type}`;
    result.innerHTML = `<strong>${title}</strong><br>${message}`;
}

async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        if (response.ok) {
            console.log('✅ 서버 연결 정상');
        } else {
            console.warn('⚠️ 서버 응답 이상');
        }
    } catch (error) {
        console.error('❌ 서버 연결 실패:', error);
        showResult('error', '⚠️ 서버 연결 확인', 
            'AI 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
    }
}
