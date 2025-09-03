import React, { useState, useEffect } from "react";
import { FaTrophy } from "react-icons/fa";
import app from "../instance/axios.js";
import { Loader } from "lucide-react";
import useDataVariable from "../utils/state.js";

const LeaderBoard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { leaderBoardDataFiltering } = useDataVariable();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const franchiseInfoDetail = await app.get(
          "/api/v1/franchises/?skip=0&limit=100"
        );
        const franchiseMatchDetail = await app.get(
          "/api/v1/leaderboard/franchises?limit=10"
        );

        if (franchiseInfoDetail.data && franchiseMatchDetail.data) {
          const filteredData = leaderBoardDataFiltering(
            franchiseInfoDetail.data,
            franchiseMatchDetail.data
          );
          setData(filteredData);
        } else {
          console.log("data unavailable");
        }
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    const interval = setInterval(fetchData, 15 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (loading)
    return (
      <div className="flex justify-center items-center h-40">
        <Loader className="animate-spin w-10 h-10 text-white" />
      </div>
    );

  return (
    <div>
      <div className="flex flex-row gap-4 items-center">
        <FaTrophy className="md:text-2xl lg:text-xl xl:text-6xl text-[#9797DE]" />
        <div className="space-y-2 text-white">
          <div className="md:text-xl lg:text-3xl xl:text-5xl">Top Team</div>
          <div className="md:text-base lg:text-xl xl:text-3xl">
            Current season leaderboard
          </div>
        </div>
      </div>

      <div className="mt-10">
        {data && (
          <div className="grid grid-cols-4 gap-2">
            {Object.values(data).map((element, index) => (
              <div
                key={index}
                className="w-full md:h-50 lg:h-60 xl:h-70 bg-[#2F3136] rounded-xl"
              >
                <div className="flex flex-row gap-2 items-center md:m-2 lg:m-4 xl:m-6">
                  <div className="md:w-8 md:h-8 lg:w-10 lg:h-10 xl:w-12 xl:h-12">
                    <img
                      src={element.imagePath}
                      className=" w-full h-full object-cover rounded-full object-center"
                    />
                  </div>
                  <div className="flex flex-col gap-2 text-white">
                    <div className="md:text-xs lg:text-base lg:font-bold xl:text-xl">
                      {element.name}
                    </div>
                    <div className="space-x-2 xl:space-x-4">
                      <span className="bg-yellow-400 p-1 rounded-lg md:text-xs lg:text-sm xl:text-lg text-black font-bold">
                        #{index + 1}
                      </span>
                      <span className="md:text-xs lg:text-lg lg:font-bold xl:text-xl">
                        {element.totalScore} Points
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-8 m-1">
                  <div className="grid grid-cols-3 gap-2">
                    <div className=" w-full h-full bg-[#37393F] text-center space-y-2 xl:space-y-4 rounded-lg p-1">
                      <div className="text-green-500 md:text-base lg:text-xl lg:font-bold xl:text-2xl">
                        {element.wonScore}
                      </div>
                      <div className="md:text-base lg:text-xl lg:font-bold xl:text-2xl text-white">
                        WINS
                      </div>
                    </div>
                    <div className=" w-full h-full bg-[#37393F] text-center space-y-2 xl:space-y-4 rounded-lg p-1">
                      <div className="text-red-500 md:text-base lg:text-xl lg:font-bold xl:text-2xl">
                        {element.lostScore}
                      </div>
                      <div className="md:text-base lg:text-xl lg:font-bold xl:text-2xl text-white">
                        LOSES
                      </div>
                    </div>
                    <div className="w-full h-full bg-[#37393F] text-center space-y-2 xl:space-y-4 rounded-lg p-1">
                      <div className="text-[#9797DE] md:text-base lg:text-xl lg:font-bold xl:text-2xl">
                        {element.wonScore + element.lostScore === 0
                          ? "0%"
                          : `${(
                              (element.wonScore / element.totalMatches) *
                              100
                            ).toFixed(0)}%`}
                      </div>
                      <div className="md:text-base lg:text-xl lg:font-bold xl:text-2xl text-white">
                        WIN RATE
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default LeaderBoard;
