import React, { useEffect, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Forum = () => {
  const [threads, setThreads] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const fetchThreads = async () => {
    try {
      const res = await axios.get(`${BACKEND_URL}/forum/threads`);
      setThreads(res.data);
    } catch (err) {
      console.error("Failed to fetch threads", err);
    }
  };

  useEffect(() => {
    fetchThreads();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${BACKEND_URL}/forum/threads`, {
        title,
        content,
      });
      setTitle("");
      setContent("");
      fetchThreads();
    } catch (err) {
      console.error("Failed to create thread", err);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Forum</h1>
      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Thread title"
          className="w-full p-2 border rounded"
          required
        />
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Thread content"
          className="w-full p-2 border rounded"
          rows={4}
          required
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Post
        </button>
      </form>
      <div className="space-y-4">
        {threads.map((thread) => (
          <div key={thread.id} className="p-4 border rounded">
            <h2 className="text-xl font-semibold">{thread.title}</h2>
            <p className="text-gray-700 mt-2">{thread.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Forum;
