import React from "react";
import { FaCalendar } from "react-icons/fa";
import Icon from "./Icon";
import EventComponent from "./EventComponent";

const PreviousEvent = () => {
  return (
    <div>
      <div className="flex justify-between items-center p-2">
        <div className="flex gap-2 items-center">
          <FaCalendar className="text-[#9797DE] md:text-base lg:text-xl xl:text-3xl" />
          <div className="lg:space-y-1 text-white">
            <div className="md:text-base lg:text-xl xl:text-3xl">
              Previous Events
            </div>
            <div className="md:text-xs lg:text-lg xl:text-2xl">
              Previous tournament results
            </div>
          </div>
        </div>
        <Icon section={"Previous Events"} />
      </div>

      <div className="mt-10">
        <EventComponent events={"previousEvent"} />
      </div>
    </div>
  );
};

export default PreviousEvent;
