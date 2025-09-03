import React, { useState } from "react";
import { FaTowerBroadcast } from "react-icons/fa6";
import EventComponent from "./EventComponent.jsx";
import ViewEvents from "./ViewEvents.jsx";

const CurrentEvent = () => {
  const [view, setView] = useState(false);

  return (
    <div>
      <div className="flex justify-between items-center p-2">
        <div className="flex gap-2 items-center">
          <FaTowerBroadcast className="text-[#9797DE] md:text-base lg:text-lg xl:text-3xl" />
          <div className="lg:space-y-1 text-white">
            <div className="md:text-base lg:text-lg xl:text-2xl">
              Current & Upcoming
            </div>
            <div className="md:text-xs lg:text-base text-xl">
              Recent tournament results
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
        <EventComponent events={"currentEvent"} limit={"ten"} />
      </div>

      {view && (
        <div className="fixed inset-0 bg-black/50 z-10">
          <div className="fixed bg-white md:w-80 lg:w-1/3 xl:w-2/5 h-full right-0">
            <ViewEvents events={"currentEvent"} setView={setView} />
          </div>
        </div>
      )}
    </div>
  );
};

export default CurrentEvent;
