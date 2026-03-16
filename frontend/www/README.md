# RAG 챗봇 프론트엔드

Next.js 기반 RAG 챗봇 UI입니다.

## 개발 환경 설정

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

브라우저에서 http://localhost:3000 접속

## 빌드

```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start
```

## 환경 변수

`.env.local` 파일을 생성하여 다음 변수를 설정하세요:

```env
# 백엔드 API URL
# 로컬 개발: http://localhost:8000
# 프로덕션: 실제 백엔드 서버 URL (예: https://api.yourdomain.com)
NEXT_PUBLIC_API_URL=http://localhost:8000

# 프론트엔드 URL (선택사항)
# 로컬 개발: http://localhost:3000
# 프로덕션: 실제 프론트엔드 서버 URL (예: https://yourdomain.com)
# 설정하지 않으면 자동으로 window.location.origin 사용
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000
```

### 클라우드 배포 시

프로덕션 환경에서는 `.env.local` 대신 배포 플랫폼의 환경 변수 설정 기능을 사용하세요:

- **Vercel**: Settings → Environment Variables
- **Netlify**: Site settings → Environment variables
- **Docker**: `docker run -e NEXT_PUBLIC_API_URL=...` 또는 docker-compose.yml의 `environment` 섹션

## 주요 기능

- 실시간 채팅 인터페이스
- 참조 문서 표시
- 반응형 디자인
- Tailwind CSS 스타일링

