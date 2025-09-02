import React, { useState } from "react";
import { FaEllipsisVertical } from "react-icons/fa6";

const Icon = () => {
  const [showOption, setShowOption] = useState(false);

  const handleClick = () => {
    if (!showOption) {
      setShowOption(true);
    } else {
      setShowOption(false);
    }
  };
  return (
    <div className="relative">
      <div
        className={`p-2 hover:bg-[##959595] rounded-sm ${
          showOption ? "bg-[#959595]" : ""
        }`}
      >
        <FaEllipsisVertical
          className={`text-2xl cursor-pointer ${
            showOption ? "text-black" : "text-white"
          }`}
          onClick={() => handleClick()}
        />
      </div>
      {showOption && (
        <div className="absolute top-9 right-0 bg-[#959595] rounded-sm w-50">
          <ul className="w-full space-y-4 list-none text-center p-2 text-white">
            <li className="text-2xl font-semibold hover:text-gray-900 cursor-pointer">
              Sort by Recent
            </li>
            <li className="text-2xl font-semibold hover:text-gray-900 cursor-pointer">
              Filter
            </li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default Icon;
