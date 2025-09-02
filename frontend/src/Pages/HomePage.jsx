import React from "react";
import Marquee from "../Component/Marquee";
import LeaderBoard from "../Component/LeaderBoard";
import CurrentEvent from "../Component/CurrentEvent";
import PreviousEvent from "../Component/PreviousEvent";
import FameElement from "../Component/FameElement";
import { FaImages } from "react-icons/fa";
import GalleryComponent from "../Component/GalleryComponent";
import Footer from "../Component/Footer";

const HomePage = () => {
  return (
    <div>
      {/* Header Section */}
      <div className="relative w-full h-[580px]">
        {/* Video Background */}
        <video
          className="w-full h-full object-cover"
          autoPlay
          muted
          loop
          playsInline
        >
          <source src="/images/bg.mp4" type="video/mp4" />
        </video>

        {/* Logo overlay */}
        <div className="absolute inset-0 bg-black/60 ">
          <div className="flex justify-center items-center">
            <div className="flex flex-col items-center gap-4">
              <img
                src="/images/logo.webp"
                alt="logo"
                className="w-80 h-80 object-contain"
              />
              <button className="bg-yellow-400 font-bold text-lg p-2 hover:bg-yellow-400/80 cursor-pointer rounded-xl">
                View Schedule
              </button>
            </div>
          </div>

          {/* Marquee Section */}
          <div className="mt-20 w-full">
            <Marquee />
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="m-20 mb-0">
        <div className="flex flex-col gap-4">
          {/* LeaderBoard Section */}
          <LeaderBoard />
        </div>

        <div className="mt-10 h-0.5 w-full bg-white"></div>

        {/* Event Section */}
        <div className="mt-10">
          <div className="grid grid-cols-3 gap-4">
            <CurrentEvent />
            <PreviousEvent />
            <FameElement />
          </div>
        </div>

        <div className="relative mt-10 -mx-20">
          <div
            className="w-full h-40 bg-contain"
            style={{ backgroundImage: "url('/images/contentBg.png')" }}
          ></div>
          <div className="absolute inset-0 flex justify-center items-center p-4">
            <div className="flex flex-col items-center text-white space-y-4">
              <div className="text-3xl font-bold">
                FEARING MISSING OUT ON EVENTS ?
              </div>
              <div className="text-sm">
                We got your back. View the schedule and be part of the match
              </div>
              <div className="pt-2 pb-2 pl-4 pr-4 text-black bg-yellow-300 font-bold rounded-xl cursor-pointer hover:bg-yellow-300/40">
                View Schedule
              </div>
            </div>
          </div>
        </div>

        <div className="mt-10">
          <div className="w-full h-0.5 bg-white"></div>
        </div>

        {/* Gallery Section */}
        <div className="mt-10">
          <div className="flex gap-4 items-center">
            <FaImages className="text-5xl text-[#9797DE]" />
            <div className="space-y-2 text-white">
              <div className="text-4xl">Game Highlights</div>
              <div className="text-xl">Best moments from recent matches</div>
            </div>
          </div>

          <div className="m-10 mb-0">
            <GalleryComponent />
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-20">
        <Footer />
      </div>
    </div>
  );
};

export default HomePage;
