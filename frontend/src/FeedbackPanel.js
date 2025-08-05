import React from "react";

const FeedbackPanel = ({ feedback }) => {
  if (!feedback) return null;

  return (
    <div className="mt-4 bg-blue-50 border border-blue-200 rounded-md p-4">
      <h3 className="text-lg font-medium text-blue-800 mb-2">Suggestions</h3>
      <p className="text-sm text-blue-700 whitespace-pre-line">{feedback}</p>
    </div>
  );
};

export default FeedbackPanel;
