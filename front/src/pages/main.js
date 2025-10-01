import './css/main.css';
import { useState } from 'react'; // level 상태 관리
import { useNavigate } from 'react-router-dom'; 

const LEVELS = ["하", "중", "상", "테스트"];

// App.js로부터 selectedFile(파일 정보)과 setSelectedFile(파일 정보 변경 함수)를 props로
const Main = ({ selectedFile, setSelectedFile }) => {
    const [level, setLevel] = useState('');
    const navigate = useNavigate();

    // 파일 선택 시 App.js의 selectedFile 상태를 변경하는 함수
    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            // props로 받은 setSelectedFile 함수를 호출합니다.
            setSelectedFile(e.target.files[0]);
        }
    };

    // 폼 제출 시 실행될 함수
    const handleSubmit = (e) => {
        e.preventDefault(); // 기본 새로고침 동작 방지

        // 파일 선택 여부는 props로 받은 selectedFile로 확인
        if (!selectedFile) {
            alert("파일을 선택해주세요.");
            return;
        }
        // 난이도 선택 여부는 Main 컴포넌트의 자체 level 상태로 확인
        if (!level) {
            alert("난이도를 선택해주세요.");
            return;
        }

        // '테스트' 레벨을 선택했다면 /test 경로로 이동
        if (level === '테스트') {
            console.log("'테스트'를 선택하여 문제 풀이 페이지로 이동합니다.");
            navigate('/test');
        } else {
            // 그 외의 경우, API 호출 및 결과 페이지 이동 로직을 수행
            // (현재는 alert만 표시)
            console.log(`'${level}' 난이도로 요약을 시작합니다.`);
            alert(`파일: ${selectedFile.name}\n난이도: ${level}\n(API 요약 요청 및 Result 페이지 이동 로직 필요)`);
            // 예: navigate('/result');
        }
    };

    return (
        <div>
            <div className='upload'>
                <p className='intro'>
                    PPT 내용을 한 번에 정리하고 설명해드립니다.<br />
                    정리된 내용을 저장하고 활용해보세요!
                </p>
                <form onSubmit={handleSubmit}>
                    <div className='space-upload'>
                        <label className='btn-upload' htmlFor='input-file'>
                            {/* 파일 이름 표시는 props로 받은 selectedFile을 사용합니다. */}
                            {selectedFile ? selectedFile.name : "파일 업로드"}
                        </label>
                        <input
                            type='file'
                            id='input-file'
                            style={{ display: 'none' }}
                            onChange={handleFileChange}
                            accept=".ppt, .pptx"
                        />
                    </div>
                    <div className='level-select'>
                        <div className="level-buttons">
                            {LEVELS.map((lv) => (
                                <label
                                    key={lv}
                                    className={`level-btn ${level === lv ? "active" : ""}`}
                                >
                                    <input
                                        type="radio"
                                        name="level"
                                        value={lv}
                                        checked={level === lv}
                                        // level 상태는 Main 컴포넌트 자체의 setLevel을 사용합니다.
                                        onChange={(e) => setLevel(e.target.value)}
                                    />
                                    {lv}
                                </label>
                            ))}
                        </div>
                    </div>
                    <button type='submit' className='btn-submit'>
                        정리 시작하기
                    </button>
                </form>
            </div>

            <div className='method'>
                <div className="method-content">
                    <h1>사용방법</h1>
                    <ol>
                        <li>원하는 PPT파일을 업로드하고 정리 시작하기 버튼을 누르세요.</li>
                        <li>AI가 파일을 읽고 전체적인 내용을 정리하는동안 기다리세요.</li>
                        <li>결과창으로 넘어가지면 다운로드 버튼을 눌러 저장하세요.</li>
                    </ol>
                </div>
                <div className="method-image"></div>
            </div>
        </div>
    );
};

export default Main;