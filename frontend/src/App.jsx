import React from "react";
import HomePage from "./Pages/HomePage";
import { Route, Routes } from "react-router-dom";

const App = () => {
  return (
    <div className="bg-[#202225] min-h-screen">
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </div>
  );
};

export default App;
