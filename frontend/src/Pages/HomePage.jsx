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
      <div className="relative w-full md:h-[430px] lg:h-[500px] xl:h-[560px]">
        {/* Video Background */}
        <video className="w-full h-full object-cover" autoPlay muted loop>
          <source src="/images/bg.mp4" type="video/mp4" />
        </video>

        {/* Logo overlay */}
        <div className="absolute inset-0">
          <div className="flex justify-center items-center">
            <div className="flex flex-col items-center gap-4">
              <img
                src="/images/logo.webp"
                alt="logo"
                className="md:w-60 md:h-60 lg:w-70 lg:h-70 xl:w-80 xl:h-80 object-contain"
              />
              <button className="bg-yellow-400 font-bold md:text-base lg:text-xl xl:text-2xl p-2 hover:bg-yellow-400/80 cursor-pointer rounded-xl">
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
      <div className="m-4">
        {/* LeaderBoard Section */}
        <div className="mt-20 flex flex-col gap-4">
          <LeaderBoard />
        </div>

        <div className="mt-20 h-0.5 w-full bg-white"></div>

        {/* Event Section */}
        <div className="mt-20">
          <div className="grid grid-cols-3 gap-4">
            <CurrentEvent />
            <PreviousEvent />
            <FameElement />
          </div>
        </div>

        <div className="relative mt-20 -mx-4">
          <div className="w-full md:h-30 lg:h-40 xl:h-50">
            <img
              src="/images/contentBg.png"
              className="w-full h-full object-contain"
            />
          </div>
          <div className="absolute inset-0 flex justify-center items-center">
            <div className="flex flex-col items-center text-white space-y-1 lg:space-y-2">
              <div className="md:text-[18px] lg:text-xl xl:text-2xl font-bold">
                FEARING MISSING OUT ON EVENTS ?
              </div>
              <div className="md:text-[10px] lg:text-sm xl:text-xl">
                We got your back. View the schedule and be part of the match
              </div>
              <div className="p-1 xl:p-2 text-black md:text-[10px] lg:text-sm xl:text-base bg-yellow-300 font-bold rounded-xl cursor-pointer hover:bg-yellow-300/40">
                View Schedule
              </div>
            </div>
          </div>
        </div>

        <div className="mt-20">
          <div className="w-full h-0.5 bg-white"></div>
        </div>

        {/* Gallery Section */}
        <div className="mt-20">
          <div className="flex gap-4 items-center">
            <FaImages className="md:text-2xl lg:text-xl xl:text-6xl text-[#9797DE]" />
            <div className="space-y-2 text-white">
              <div className="md:text-xl lg:text-3xl xl:text-5xl">
                Game Highlights
              </div>
              <div className="md:text-base lg:text-xl xl:text-3xl">
                Best moments from recent matches
              </div>
            </div>
          </div>

          <div className="m-6 xl:m-8 mb-0">
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
