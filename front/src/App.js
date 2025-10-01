import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react'; // 1. useState 훅 import

// 컴포넌트 import
import Header from './component/header';
import Footer from './component/footer';
import Main from './pages/main';
import Result from './pages/result';
import Test from './pages/test';

function App() {
  // 2. Main.js에 있던 파일과 레벨 상태를 App.js로 가져옵니다.
  const [selectedFile, setSelectedFile] = useState(null);
  const [level, setLevel] = useState('');

  return (
    <BrowserRouter>
      <Header />
      <div className="content-wrap">
        <Routes>
          {/* 3. 각 컴포넌트에 상태와 상태 변경 함수를 props로 전달합니다. */}
          <Route 
            path="/" 
            element={<Main 
              selectedFile={selectedFile} 
              setSelectedFile={setSelectedFile} 
              setLevel={setLevel} 
            />} 
          />
          <Route 
            path="/test" 
            element={<Test selectedFile={selectedFile} />} 
          />
          <Route 
            path="/result" 
            element={<Result selectedFile={selectedFile} level={level} />} 
          />
        </Routes>
      </div>
      <Footer />
    </BrowserRouter>
  );
}

export default App;