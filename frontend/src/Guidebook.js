import React, { useEffect, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const renderMarkdown = (text) => {
  return text
    .replace(/^### (.*$)/gim, "<h3>$1</h3>")
    .replace(/^## (.*$)/gim, "<h2>$1</h2>")
    .replace(/^# (.*$)/gim, "<h1>$1</h1>")
    .replace(/\*\*(.*)\*\*/gim, "<strong>$1</strong>")
    .replace(/\*(.*)\*/gim, "<em>$1</em>")
    .replace(/\n/g, "<br />");
};

const Guidebook = () => {
  const [chapters, setChapters] = useState([]);
  const [content, setContent] = useState("");
  const [active, setActive] = useState("");

  useEffect(() => {
    const fetchChapters = async () => {
      try {
        const res = await axios.get(`${BACKEND_URL}/guidebook`);
        const list = res.data.chapters || [];
        setChapters(list);
        if (list.length > 0) {
          loadChapter(list[0]);
        }
      } catch (err) {
        console.error("Error fetching guidebook chapters", err);
      }
    };
    fetchChapters();
  }, []);

  const loadChapter = async (chapter) => {
    setActive(chapter);
    try {
      const res = await axios.get(`${BACKEND_URL}/guidebook/${chapter}`, {
        responseType: "text",
      });
      const data = res.data;
      const html = chapter.endsWith(".md") ? renderMarkdown(data) : data;
      setContent(html);
    } catch (err) {
      console.error("Error loading chapter", err);
      setContent("<p>Failed to load chapter.</p>");
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Guidebook</h1>
      <div className="flex">
        <nav className="w-1/4 pr-4">
          <ul className="space-y-2">
            {chapters.map((ch) => (
              <li key={ch}>
                <button
                  onClick={() => loadChapter(ch)}
                  className={`text-left w-full hover:underline ${
                    active === ch ? "font-bold" : ""
                  }`}
                >
                  {ch.replace(/\.[^/.]+$/, "")}
                </button>
              </li>
            ))}
          </ul>
        </nav>
        <article
          className="w-3/4 prose max-w-none"
          dangerouslySetInnerHTML={{ __html: content }}
        />
      </div>
    </div>
  );
};

export default Guidebook;
