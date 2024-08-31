'use client';

import React, { useState } from 'react';

// 質問データ（夏に関する抽象的な質問に変更）
const questions = [
  { id: 'danceability', text: '夏の日差しで踊りたくなりますか？' },
  { id: 'acousticness', text: '夏の風を感じる音楽は好きですか？' },
  { id: 'energy', text: '夏の暑さにエネルギーを感じますか？' },
  { id: 'instrumentalness', text: '夏の夜にインストゥルメンタルな音楽を楽しみますか？' },
  { id: 'liveness', text: '夏祭りの活気を感じますか？' },
  { id: 'loudness', text: '夏のビーチで音楽の音量を上げたいですか？' },
  { id: 'speechiness', text: '夏の思い出を語りたくなりますか？' },
  { id: 'tempo', text: '夏のテンポで動きたくなりますか？' },
  { id: 'time_signature', text: '夏のリズムに乗れますか？' },
  { id: 'valence', text: '夏はあなたを明るい気持ちにさせますか？' }, // 最後の質問
];

// 回答の選択肢
const options = [
  'はい',
  'どちらかといえばはい',
  'どちらともいえない',
  'どちらかといえばいいえ',
  'いいえ',
];

const Questionnaire = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null); // 推奨結果を保存
  const [showRecommendation, setShowRecommendation] = useState(false); // 推奨画面表示用のフラグ
  const [showSubmitButton, setShowSubmitButton] = useState(false); // 結果ボタン表示用のフラグ

  const handleResponse = (response: string) => {
    const questionId = questions[currentQuestionIndex].id;
    setResponses((prev) => ({
      ...prev,
      [questionId]: response,
    }));

    // 最後の質問かどうかをチェック
    if (currentQuestionIndex < questions.length - 1) {
      // 次の質問に進む
      setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
    } else {
      // 最後の質問が終わったら「結果を見ますか」ボタンを表示
      setShowSubmitButton(true);
    }
  };

  // 質問の回答を送信する関数
  const handleSubmit = async () => {
    try {
      console.log('Sending data:', responses); // デバッグ用にリクエストデータを出力
      const response = await fetch('http://127.0.0.1:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(responses),
      });

      if (!response.ok) {
        const errorMessage = await response.text(); // エラーメッセージを取得
        throw new Error(`APIリクエストに失敗しました: ${errorMessage}`);
      }

      const result = await response.json();
      console.log('Received result:', result); // デバッグ用にレスポンスデータを出力
      setResult(result); // 推奨された曲を結果にセット
      setShowRecommendation(true); // 推奨画面を表示するフラグを立てる
    } catch (err) {
      setError((err as Error).message);
      console.error('Error during fetch:', err); // エラーの詳細をコンソールに出力
    }
  };

  // 推奨画面のコンポーネント
  const Recommendation = () => (
    <div className="mt-8 bg-blue-100 p-10 rounded-lg shadow-xl max-w-3xl mx-auto text-center">
      <h2 className="text-4xl font-semibold text-blue-800">今日のおすすめの一曲:</h2>
      <h3 className="mt-6 text-2xl text-gray-800">{result?.recommended_track?.name || 'データがありません'}</h3>
      {result?.recommended_track?.track_id && (
        <iframe
          src={`https://open.spotify.com/embed/track/${result.recommended_track.track_id}?autoplay=1&theme=0`}
          width="500"
          height="300"
          frameBorder="0"
          allow="autoplay; encrypted-media"
          className="mt-2"
        />
      )}
      <button 
        className="mt-12 bg-blue-400 text-white px-8 py-4 rounded-full hover:bg-yellow-500 transition text-2xl"
        onClick={() => {
          // 質問をリセット
          setCurrentQuestionIndex(0);
          setResponses({});
          setResult(null);
          setShowRecommendation(false);
          setShowSubmitButton(false);
        }}
      >
        もう一度質問する
      </button>
    </div>
  );

  return (
    <div className="p-8 bg-gradient-to-r from-blue-300 via-blue-200 to-blue-100 min-h-screen flex flex-col justify-center items-center">
      {showRecommendation ? (
        <Recommendation />
      ) : (
        <>
          <h2 className="text-3xl font-bold text-blue-800 mb-8">{questions[currentQuestionIndex].text}</h2>
          <div className="flex space-x-6">
            {options.map((option) => (
              <button
                key={option}
                className="bg-blue-500 text-white px-6 py-3 rounded-full hover:bg-blue-600 transition text-lg"
                onClick={() => handleResponse(option)}
              >
                {option}
              </button>
            ))}
          </div>
          {showSubmitButton && (
            <button 
              className="mt-8 bg-green-500 text-white px-6 py-3 rounded-full hover:bg-green-600 transition text-lg"
              onClick={handleSubmit}
            >
              結果を見ますか
            </button>
          )}
          {error && <p className="text-red-500 mt-4">{error}</p>}
        </>
      )}
    </div>
  );
};

export default Questionnaire;
