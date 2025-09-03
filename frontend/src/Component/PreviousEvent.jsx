import React, { useState } from "react";
import { FaCalendar } from "react-icons/fa";
import EventComponent from "./EventComponent";
import ViewEvents from "./ViewEvents";

const PreviousEvent = () => {
  const [view, setView] = useState(false);

  return (
    <div>
      <div className="flex justify-between items-center p-2">
        <div className="flex gap-2 items-center">
          <FaCalendar className="text-[#9797DE] md:text-base lg:text-lg xl:text-3xl" />
          <div className="lg:space-y-1 text-white">
            <div className="md:text-base lg:text-lg xl:text-2xl">
              Previous Events
            </div>
            <div className="md:text-xs lg:text-base text-xl">
              Previous tournament results
            </div>
          </div>
        </div>
        <div
          className="text-white md:text-xs lg:text-base xl:text-xl underline cursor-pointer hover:text-gray-300"
          onClick={() => setView(true)}
        >
          View All
        </div>
      </div>

      <div className="mt-10">
        <EventComponent events={"previousEvent"} limit={"ten"} />
      </div>

      {view && (
        <div className="fixed inset-0 bg-black/50 z-10">
          <div className="fixed bg-white md:w-80 lg:w-1/3 xl:w-2/5 h-full right-0">
            <ViewEvents events={"previousEvent"} setView={setView} />
          </div>
        </div>
      )}
    </div>
  );
};

export default PreviousEvent;
