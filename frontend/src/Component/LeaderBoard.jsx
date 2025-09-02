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
        <FaTrophy className="text-5xl text-[#9797DE]" />
        <div className="space-y-2 text-white">
          <div className="text-4xl">Top Team</div>
          <div className="text-xl">Current season leaderboard</div>
        </div>
      </div>

      <div className="mt-10">
        {data && (
          <div className="grid grid-cols-4 gap-6">
            {Object.values(data).map((element, index) => (
              <div key={index} className="w-full h-70 bg-[#2F3136] rounded-xl">
                <div className="flex flex-row gap-6 items-center m-4">
                  <div className="w-12 h-12">
                    <img
                      src={element.imagePath}
                      className=" w-full h-full object-cover rounded-full object-center"
                    />
                  </div>
                  <div className="flex flex-col gap-4 text-white">
                    <div className="text-base font-bold">{element.name}</div>
                    <div className="space-x-2">
                      <span className="bg-yellow-400 pl-3 pr-3 pt-2 pb-2 rounded-2xl text-sm text-black font-bold">
                        #{index + 1}
                      </span>
                      <span className="text-sm">
                        {element.totalScore} Points
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-8 ml-4 mr-4">
                  <div className="grid grid-cols-3 gap-4">
                    <div className=" w-full h-full bg-[#37393F] text-center space-y-8 rounded-lg p-2">
                      <div className="text-green-500 text-2xl font-bold">
                        {element.wonScore}
                      </div>
                      <div className="text-2xl text-white font-bold">WINS</div>
                    </div>
                    <div className=" w-full h-full bg-[#37393F] text-center space-y-8 rounded-lg p-2">
                      <div className="text-red-500 text-2xl font-bold">
                        {element.lostScore}
                      </div>
                      <div className="text-2xl text-white font-bold">LOSES</div>
                    </div>
                    <div className="w-full h-full bg-[#37393F] text-center space-y-8 rounded-lg p-2">
                      <div className="text-[#9797DE] text-2xl font-bold">
                        {element.wonScore + element.lostScore === 0
                          ? "0%"
                          : `${(
                              (element.wonScore / element.totalMatches) *
                              100
                            ).toFixed(0)}%`}
                      </div>
                      <div className="text-2xl text-white font-bold">
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
