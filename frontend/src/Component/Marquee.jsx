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
              className="mx-8 font-bold md:text-3xl lg:text-4xl xl:text-5xl flex items-center"
            >
              <span className="text-blue-600">LIVE</span>
              <span className="text-white ml-2">• JOIN CCL</span>
            </span>
          ))}
      </div>
    </div>
  );
};

export default Marquee;
