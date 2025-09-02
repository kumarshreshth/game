import React from "react";
import { SlBadge } from "react-icons/sl";

const FameElement = () => {
  return (
    <div>
      <div className="flex gap-8 items-center">
        <SlBadge className="text-[#9797DE] text-3xl" />
        <div className="space-y-2 text-white">
          <div className="text-2xl">Wall of Fame</div>
          <div className="text-lg">Players who made history</div>
        </div>
      </div>
    </div>
  );
};

export default FameElement;
