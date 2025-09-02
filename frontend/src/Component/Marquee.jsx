import React from "react";

const Marquee = () => {
  return (
    <div className="relative w-full overflow-hidden">
      <div className="flex animate-marquee whitespace-nowrap">
        {Array(10)
          .fill(null)
          .map((_, idx) => (
            <span
              key={idx}
              className="mx-8 font-bold text-5xl flex items-center"
            >
              <span className="text-blue-600">LIVE</span>
              <span className="text-white ml-2">• JOIN CCL</span>
            </span>
          ))}
      </div>

      <div className="absolute top-0 left-0 h-full w-8 pointer-events-none bg-gradient-to-r from-black/40 to-black/0"></div>
      <div className="absolute top-0 right-0 h-full w-8 pointer-events-none bg-gradient-to-l from-black/40 to-black/0"></div>
    </div>
  );
};

export default Marquee;
