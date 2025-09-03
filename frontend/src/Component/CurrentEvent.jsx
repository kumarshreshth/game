import React from "react";
import { FaTowerBroadcast } from "react-icons/fa6";
import Icon from "./Icon";
import EventComponent from "./EventComponent.jsx";

const CurrentEvent = () => {
  return (
    <div>
      <div className="flex justify-between items-center p-2">
        <div className="flex gap-2 items-center">
          <FaTowerBroadcast className="text-[#9797DE] md:text-base lg:text-xl xl:text-3xl" />
          <div className="lg:space-y-1 text-white">
            <div className="md:text-base lg:text-xl xl:text-3xl">
              Current & Upcoming
            </div>
            <div className="md:text-xs lg:text-lg text-2xl">
              Recent tournament results
            </div>
          </div>
        </div>
        <Icon section={"Coming & Upcoming Events"} />
      </div>

      <div className="mt-10">
        <EventComponent events={"currentEvent"} />
      </div>
    </div>
  );
};

export default CurrentEvent;
