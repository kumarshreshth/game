import React, { useState } from "react";
import { FaTimes } from "react-icons/fa";
import { FaBars, FaEllipsisVertical, FaFilter } from "react-icons/fa6";

const Icon = ({ section }) => {
  const [showOption, setShowOption] = useState(false);
  const [filterPopUp, setFilterPopUp] = useState(false);

  const handleFilter = () => {
    setShowOption(false);
    setFilterPopUp(true);
  };

  const handleClose = () => {
    setFilterPopUp(false);
  };

  const handleClick = () => {
    if (!showOption) {
      setShowOption(true);
    } else {
      setShowOption(false);
    }
  };
  return (
    <div className="relative">
      <div
        className={`p-2 hover:bg-[##959595] rounded-sm ${
          showOption ? "bg-[#2c3037]" : ""
        }`}
      >
        <FaEllipsisVertical
          className={`md:text-sm lg:text-lg xl:text-xl lx:text-lg cursor-pointer ${
            showOption ? "text-black" : "text-white"
          }`}
          onClick={() => handleClick()}
        />
      </div>
      {showOption && (
        <div className="absolute top-6 xl:top-8 right-0 bg-[#2c3037]/90 rounded-sm md:w-30 lg:w-40 xl:w-50">
          <ul className="w-full space-y-4 xl:space-y-6 list-none text-center p-2 text-white">
            <li
              className="md:text-sm lg:text-lg xl:text-xl font-semibold hover:text-gray-500 cursor-pointer"
              onClick={() => handleSort()}
            >
              Sort by Recent
            </li>
            <li
              className="md:text-sm lg:text-lg xl:text-xl font-semibold hover:text-gray-500 cursor-pointer"
              onClick={() => handleFilter()}
            >
              Filter
            </li>
          </ul>
        </div>
      )}

      {filterPopUp && (
        <div className="fixed inset-0 bg-black/60 z-10">
          <div className="fixed top-0 right-0 h-full w-2/7 bg-white">
            <div className="h-20 bg-[#9797DE]">
              <div className="flex justify-between items-center p-4">
                <div className="flex justify-center items-center space-x-8">
                  <FaBars className="text-4xl" />
                  <div className="text-5xl font-semibold">Filter</div>
                </div>
                <FaTimes
                  className="text-4xl text-white cursor-pointer hover:text-gray-400"
                  onClick={() => handleClose()}
                />
              </div>
            </div>

            <div className="mt-5 p-4">
              <div className="text-2xl font-bold">{section}</div>
              <div className="mt-5">
                <form className="space-y-4">
                  <div className="flex flex-col space-y-2">
                    <label
                      htmlFor="fromDate"
                      className="text-lg font-medium text-gray-700"
                    >
                      From Date
                    </label>
                    <input
                      id="fromDate"
                      type="date"
                      className="border border-gray-300 rounded-md p-2 outline-none"
                      placeholder="Select Date"
                    />
                  </div>
                  <div className="flex flex-col space-y-2">
                    <label
                      htmlFor="endDate"
                      className="text-lg font-medium text-gray-700"
                    >
                      End Date
                    </label>
                    <input
                      id="endDate"
                      type="date"
                      className="border border-gray-300 rounded-md p-2 outline-none"
                      placeholder="Select Date"
                    />
                  </div>

                  <div className="flex flex-col space-y-2">
                    <label
                      htmlFor="sport"
                      className="text-lg font-medium text-gray-700"
                    >
                      Sports
                    </label>
                    <select
                      id="sport"
                      className="border border-gray-300 rounded-md p-2 outline-none overflow-auto"
                      defaultValue="1"
                    >
                      <option value="1" disabled>
                        Select sport
                      </option>
                      <option>Box Cricket</option>
                      <option>Table Tennis</option>
                      <option>Pool</option>
                      <option>Carom</option>
                      <option>Pickle ball</option>
                      <option>Chess</option>
                      <option>Foosball</option>
                      <option>Badminton</option>
                    </select>
                  </div>

                  <div className="mt-5 space-y-4">
                    <button
                      className="w-full text-center p-2 bg-yellow-300 font-bold rounded-xl border border-amber-600 cursor-pointer hover:bg-gray-500"
                      onClick={() => handleApply()}
                    >
                      Apply
                    </button>
                    <button
                      type="reset"
                      className="w-full text-center p-2 bg-yellow-300 font-bold rounded-xl border border-amber-600 cursor-pointer hover:bg-gray-500"
                      onClick={() => handleReset()}
                    >
                      Reset
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Icon;
