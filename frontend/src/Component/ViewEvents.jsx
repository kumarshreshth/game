import React from "react";
import EventComponent from "./EventComponent";
import { FaTimes } from "react-icons/fa";

const ViewEvents = ({ events, setView }) => {
  return (
    <div>
      <div className="flex justify-between items-center md:text-lg lg:text-xl xl:text-3xl bg-[#9797DE] p-4">
        <div className="text-center font-semibold">
          {events === "currentEvent"
            ? "Current and Upcoming Event"
            : "Previous Events"}
        </div>
        <FaTimes
          className="hover:text-white/60 cursor-pointer"
          onClick={() => setView(false)}
        />
      </div>
      <div className="m-8">
        <EventComponent events={events} limit={"full"} />
      </div>
    </div>
  );
};

export default ViewEvents;
