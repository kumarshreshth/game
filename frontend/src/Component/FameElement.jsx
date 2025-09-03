import React from "react";
import { SlBadge } from "react-icons/sl";

const FameElement = () => {
  return (
    <div>
      <div className="flex justify-between items-center p-2">
        <div className="flex gap-2 items-center">
          <SlBadge className="text-[#9797DE] md:text-base lg:text-xl xl:text-3xl" />
          <div className="lg:space-y-1 text-white">
            <div className="md:text-base lg:text-xl xl:text-3xl">
              Wall of Fame
            </div>
            <div className="md:text-xs lg:text-lg xl:text-2xl">
              Players who made history
            </div>
          </div>
        </div>
        <div
          className="text-white md:text-xs lg:text-base xl:text-xl underline cursor-pointer hover:text-gray-300"
          onClick={() => handleClick()}
        >
          View All
        </div>
      </div>
    </div>
  );
};

export default FameElement;
