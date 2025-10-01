import './css/test.css';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// App.js로부터 selectedFile prop을 받습니다.
const Test = ({ selectedFile }) => {
    const navigate = useNavigate();

    const [isLoading, setIsLoading] = useState(true); // 문제 로딩 상태
    const [questions, setQuestions] = useState([]); // API로부터 받아온 문제 목록
    const [userAnswers, setUserAnswers] = useState({}); // 사용자가 선택한 답안
    const [score, setScore] = useState(null); // 채점 후 점수 (null이면 아직 채점 전)
    const [finalLevel, setFinalLevel] = useState(''); // 점수에 따라 결정된 최종 난이도

    // (시뮬레이션) 컴포넌트가 로드될 때 API를 호출하여 문제를 받아오는 부분
    useEffect(() => {

        if (!selectedFile) {
            alert("선택된 파일이 없습니다. 메인 페이지로 돌아갑니다.");
            navigate('/');
            return;
        }

        console.log(`'${selectedFile.name}' 파일을 기반으로 문제 생성을 시작합니다.`);

        // 가짜데이터(API 받아와야함)
        setTimeout(() => {
            const mockQuestions = [
                { id: 1, question: "이 PPT의 핵심 주제는 무엇인가요?", options: ["A", "B", "C", "D"], answer: "A" },
                { id: 2, question: "발표의 주요 결론은 무엇인가요?", options: ["결론1", "결론2", "결론3"], answer: "결론2" },
                { id: 3, question: "가장 중요하게 언급된 데이터는 무엇인가요?", options: ["Data X", "Data Y", "Data Z"], answer: "Data Z" },
            ];

            setQuestions(mockQuestions); // 문제 상태 업데이트
            setIsLoading(false); // 로딩 상태 종료
        }, 2000); // 2초 딜레이

    }, [selectedFile, navigate]);

    // 사용자가 답안을 선택할 때마다 userAnswers 상태를 업데이트하는 함수
    const handleAnswerChange = (questionId, answer) => {
        setUserAnswers(prevAnswers => ({
            ...prevAnswers,
            [questionId]: answer,
        }));
    };

    // "채점하기" 버튼 클릭 시 실행될 함수
    const handleSubmitQuiz = () => {
        let correctAnswers = 0;
        questions.forEach(q => {
            if (q.answer === userAnswers[q.id]) {
                correctAnswers++;
            }
        });

        const calculatedScore = Math.round((correctAnswers / questions.length) * 100);
        setScore(calculatedScore);

        // 점수에 따라 최종 난이도 결정
        if (calculatedScore >= 80) {
            setFinalLevel('상');
        } else if (calculatedScore >= 50) {
            setFinalLevel('중');
        } else {
            setFinalLevel('하');
        }
    };
    
    // 최종 결과 페이지로 이동하는 함수
    const goToResultPage = () => {
        console.log(`최종 결정 난이도 '${finalLevel}'와 함께 결과 페이지로 이동합니다.`);
        // navigate의 state 옵션을 사용해 Result 페이지로 데이터를 전달합니다.
        navigate('/result', { state: { finalLevel: finalLevel } });
    }

    // 렌더링 부분
    if (isLoading) {
        return (
            <div className="test-container">
                <h2>AI가 PPT를 분석하여 문제를 생성 중입니다...</h2>
                <p>잠시만 기다려주세요.</p>
            </div>
        );
    }

    // 결과 표시
    if (score !== null) {
        return (
            <div className="test-container result-view">
                <h2>퀴즈 결과</h2>
                <p className="score">당신의 점수는 <strong>{score}점</strong> 입니다.</p>
                <p>사용자 수준을 분석하여 **'{finalLevel}'** 난이도로 요약을 진행합니다.</p>
                <button onClick={goToResultPage} className="btn-submit">
                    결과 보기
                </button>
            </div>
        )
    }

    return (
        <div className="test-container">
            <h1>{selectedFile.name} 내용 확인 퀴즈</h1>
            <p>문제를 풀고 자신에게 맞는 요약 수준을 추천받으세요.</p>
            <div className="quiz-form">
                {questions.map((q, index) => (
                    <div key={q.id} className="question-block">
                        <h3>{index + 1}. {q.question}</h3>
                        <div className="options">
                            {q.options.map(option => (
                                <label key={option} className="option-label">
                                    <input
                                        type="radio"
                                        name={`question-${q.id}`}
                                        value={option}
                                        onChange={() => handleAnswerChange(q.id, option)}
                                        checked={userAnswers[q.id] === option}
                                    />
                                    {option}
                                </label>
                            ))}
                        </div>
                    </div>
                ))}
                <button onClick={handleSubmitQuiz} className="btn-submit">채점하기</button>
            </div>
        </div>
    );
};

export default Test;