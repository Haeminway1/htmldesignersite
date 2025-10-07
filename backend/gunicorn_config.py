# Gunicorn 설정 (Render 최적화)
import multiprocessing
import os

# 워커 설정
workers = 1  # 메모리 제한으로 1개만 사용
worker_class = 'sync'
worker_connections = 1000
timeout = 300  # 5분 (AI API 응답 대기)
keepalive = 5
max_requests = 100
max_requests_jitter = 10

# 로깅
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 바인딩
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# 프로세스 이름
proc_name = 'htmldesigner'

# 서버 재시작
preload_app = False
reload = False

# 메모리 관리
worker_tmp_dir = '/dev/shm'  # tmpfs 사용
