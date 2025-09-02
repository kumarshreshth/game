import React from "react";
import { FaCalendar } from "react-icons/fa";
import Icon from "./Icon";
import EventComponent from "./EventComponent";

const PreviousEvent = () => {
  return (
    <div>
      <div className="flex gap-24 items-center">
        <div className="flex gap-6 items-center">
          <FaCalendar className="text-[#9797DE] text-3xl" />
          <div className="space-y-2 text-white">
            <div className="text-2xl">Previous Events</div>
            <div className="text-lg">Previous tournament results</div>
          </div>
        </div>
        <Icon />
      </div>

      <div className="mt-10">
        <EventComponent events={"previousEvent"} />
      </div>
    </div>
  );
};

export default PreviousEvent;
