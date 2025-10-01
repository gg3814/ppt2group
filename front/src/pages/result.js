import './css/result.css';
import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Result = ({ selectedFile, level }) => {
    const navigate = useNavigate();
    const location = useLocation();

    // 1. 텍스트 대신 HTML 콘텐츠를 저장할 상태
    const [isLoading, setIsLoading] = useState(true);
    const [htmlContent, setHtmlContent] = useState(""); // 요약 텍스트 -> HTML 콘텐츠로 변경

    const finalEffectiveLevel = location.state?.finalLevel || level;

    useEffect(() => {
        if (!selectedFile) {
            alert("요약할 파일이 없습니다. 메인 페이지로 돌아갑니다.");
            navigate('/');
            return;
        }

        // 2. (시뮬레이션) API가 HTML을 생성했다고 가정
        setTimeout(() => {
            // API가 생성해주는 HTML+CSS 문자열 예시
            const mockHtmlResponse = `
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${selectedFile.name} 요약 노트</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 30px; background-color: #f9f9f9; }
        .container { max-width: 800px; margin: auto; background-color: #ffffff; padding: 25px 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        ul { list-style-type: disc; padding-left: 20px; }
        li { margin-bottom: 10px; }
        code { background-color: #ecf0f1; padding: 2px 5px; border-radius: 3px; }
        .footer { text-align: center; margin-top: 40px; font-size: 0.9em; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>${selectedFile.name} | ${finalEffectiveLevel} 난이도 요약 노트</h1>
        <h2>핵심 내용 요약</h2>
        <ul>
            <li>AI 기술의 발전은 사회 전반에 큰 영향을 미치고 있습니다.</li>
            <li>특히 <code>자연어 처리(NLP)</code>와 <code>컴퓨터 비전</code> 분야의 성장이 두드러집니다.</li>
            <li>AI 시장은 연평균 30% 이상의 높은 성장률을 보이고 있습니다.</li>
        </ul>
        <h2>주요 결론</h2>
        <p>AI 기술의 긍정적인 측면을 수용하는 동시에, 발생 가능한 윤리적 문제에 대한 깊이 있는 사회적 논의가 반드시 필요합니다.</p>
        <div class="footer">
            <p>본 문서는 '한눈에 PPT' 서비스를 통해 생성되었습니다.</p>
        </div>
    </div>
</body>
</html>
            `;
            
            setHtmlContent(mockHtmlResponse.trim()); // HTML 결과 상태 업데이트
            setIsLoading(false); // 로딩 종료
        }, 3000);

    }, [selectedFile, finalEffectiveLevel, navigate]);

    // 3. HTML 문자열을 파일로 만들어 다운로드하는 함수
    const handleDownload = () => {
        // Blob 객체를 사용해 메모리상에 파일을 만듭니다. (타입: 'text/html')
        const blob = new Blob([htmlContent], { type: 'text/html' });

        // 파일에 접근할 수 있는 임시 URL을 생성합니다.
        const url = URL.createObjectURL(blob);

        // 보이지 않는 <a> 태그를 만들어 다운로드를 실행시킵니다.
        const a = document.createElement('a');
        a.href = url;
        a.download = `${selectedFile.name.split('.')[0]}_note.html`; // 파일명 설정 (e.g., '내문서_note.html')
        document.body.appendChild(a); // a 태그를 DOM에 추가
        a.click(); // 클릭 이벤트 실행
        
        // 다운로드 후 임시 URL과 a 태그를 정리합니다.
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const handleGoHome = () => navigate('/');

    if (isLoading) {
        return (
            <div className="result-container">
                <h2>AI가 노트를 HTML 파일로 생성 중입니다...</h2>
                <p>잠시만 기다려주세요.</p>
            </div>
        );
    }

    return (
        <div className="result-container">
            <h1>생성된 노트 미리보기</h1>
            <div className="preview-box">
                {/* 4. iframe의 srcDoc 속성에 HTML 문자열을 전달하여 미리보기를 구현 */}
                <iframe
                    srcDoc={htmlContent}
                    title="결과 미리보기"
                    width="100%"
                    height="500px"
                    frameBorder="0"
                ></iframe>
            </div>
            <div className="button-group">
                <button onClick={handleDownload} className="btn-result download">파일 다운로드</button>
                <button onClick={handleGoHome} className="btn-result go-home">처음으로</button>
            </div>
        </div>
    );
};

export default Result;