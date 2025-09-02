import React from "react";
import { FaTowerBroadcast } from "react-icons/fa6";
import Icon from "./Icon";
import EventComponent from "./EventComponent.jsx";

const CurrentEvent = () => {
  return (
    <div>
      <div className="flex gap-24 items-center">
        <div className="flex gap-8 items-center">
          <FaTowerBroadcast className="text-[#9797DE] text-3xl" />
          <div className="space-y-2 text-white">
            <div className="text-2xl">Current & Upcoming</div>
            <div className="text-lg">Recent tournament results</div>
          </div>
        </div>
        <Icon />
      </div>

      <div className="mt-10">
        <EventComponent events={"currentEvent"} />
      </div>
    </div>
  );
};

export default CurrentEvent;
