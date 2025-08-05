import React, { useEffect, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Exercises = ({ chapter }) => {
  const [exercises, setExercises] = useState([]);
  const [answers, setAnswers] = useState({});
  const [showSolutions, setShowSolutions] = useState({});

  useEffect(() => {
    const fetchExercises = async () => {
      try {
        const res = await axios.get(`${API}/exercises/${chapter}`);
        setExercises(res.data.exercises || []);
      } catch (err) {
        console.error("Error fetching exercises", err);
      }
    };
    fetchExercises();
  }, [chapter]);

  const handleAnswerChange = (index, value) => {
    setAnswers({ ...answers, [index]: value });
  };

  const revealSolution = (index) => {
    setShowSolutions({ ...showSolutions, [index]: true });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Exercises - Chapter {chapter}</h1>
      {exercises.map((ex, idx) => (
        <div key={idx} className="mb-6 p-4 border rounded-lg">
          <p className="mb-2 font-medium">{ex.question}</p>
          <input
            type="text"
            value={answers[idx] || ""}
            onChange={(e) => handleAnswerChange(idx, e.target.value)}
            className="w-full p-2 border rounded mb-2"
          />
          <button
            onClick={() => revealSolution(idx)}
            className="bg-blue-500 text-white px-3 py-1 rounded"
          >
            Show Solution
          </button>
          {showSolutions[idx] && (
            <div className="mt-2 text-green-700">{ex.solution || ex.answer}</div>
          )}
        </div>
      ))}
      {exercises.length === 0 && (
        <p>No exercises found for this chapter.</p>
      )}
    </div>
  );
};

export default Exercises;
