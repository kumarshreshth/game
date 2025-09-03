import { Loader } from "lucide-react";
import React, { useEffect, useState } from "react";
import useDataVariable from "../utils/state";
import app from "../instance/axios";
import { FaTrophy } from "react-icons/fa";

const EventComponent = ({ events, limit }) => {
  const [loading, setLoading] = useState(true);
  const [gameDetail, setGameDetail] = useState(null);
  const [matchData, setMatchData] = useState(null);
  const [info, setInfo] = useState(null);
  const { matchDetails, leaderBoard } = useDataVariable();
  const [currentTime, setCurrentTime] = useState(new Date());

  let nextEvents, previousEvents, array, gameData;

  const getEventTag = (startDate, startTime, duration) => {
    const start = new Date(`${startDate}T${startTime}`);
    const end = new Date(`${startDate}T${startTime + duration}`);

    if (start <= currentTime && end && currentTime <= end) {
      return "Ongoing";
    } else if (start > currentTime) {
      return "Upcoming";
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 15 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data } = await app.get("/api/v1/games/?skip=0&limit=100");
        if (data) setGameDetail(data);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (matchDetails) {
      setMatchData(matchDetails);
    }
  }, [matchDetails]);

  useEffect(() => {
    if (leaderBoard) {
      setInfo(leaderBoard);
    }
  }, [leaderBoard]);

  if (loading)
    return (
      <div className="flex justify-center items-center h-40">
        <Loader className="animate-spin w-10 h-10 text-white" />
      </div>
    );

  if (matchData && gameDetail && info) {
    nextEvents = matchData
      .filter((element) => element.status === "scheduled")
      .sort((a, b) => {
        const dateTimeA = new Date(`${a.date}T${a.time}`);
        const dateTimeB = new Date(`${b.date}T${b.time}`);
        return dateTimeA - dateTimeB;
      });

    previousEvents = matchData
      .filter((element) => element.status === "completed")
      .sort((a, b) => {
        const dateTimeA = new Date(`${a.date}T${a.time}`);
        const dateTimeB = new Date(`${b.date}T${b.time}`);
        return dateTimeB - dateTimeA;
      });

    gameData = Object.fromEntries(
      gameDetail.map((item) => [item.id, item.name])
    );

    array = events === "currentEvent" ? nextEvents : previousEvents;
    array = limit === "ten" ? array.slice(0, 10) : array;
  }
  return (
    matchData &&
    gameData &&
    info && (
      <div
        className="w-full max-h-[600px] overflow-y-scroll"
        style={{ scrollbarWidth: "none" }}
      >
        <div className="flex flex-col items-center gap-4">
          {array.slice(0, 10).map((element, index) => {
            const tag =
              events === "currentEvent"
                ? getEventTag(element.match_date, element.match_time, 90)
                : element.round;

            return (
              <div
                key={index}
                className={`w-full md:h-48 lg:h-56 xl:h-64 ${
                  limit === "ten" ? "bg-[#37393F]" : "bg-gray-100"
                } rounded-lg`}
              >
                <div className="space-y-4 p-4">
                  <div className="flex justify-between items-center">
                    <div
                      className={`${
                        limit === "ten" ? "text-white" : "text-black"
                      } md:text-base lg:text-xl xl:text-2xl`}
                    >
                      {gameData[element.game_id]}
                    </div>
                    <div
                      className={`p-1 rounded-xl border ${
                        limit === "ten" ? "text-white" : "text-black"
                      } md:text-xs lg:text-sm xl:text-base font-semibold ${
                        tag === "Ongoing" ? "bg-amber-300 border-amber-300" : ""
                      }`}
                    >
                      {tag}
                    </div>
                  </div>

                  {info && (
                    <div className="flex justify-evenly items-center">
                      <div className="flex flex-col items-center space-y-2 p-2">
                        <div className="md:w-6 md:h-6 lg:w-10 lg:h-10 xl:w-14 xl:h-14 relative">
                          <img
                            src={info?.[element.home_franchise_id]?.imagePath}
                            className="w-full h-full object-cover rounded-full"
                          />
                          {events === "previousEvent" &&
                            element.winner_id === element.home_franchise_id && (
                              <div className="absolute -top-1 left-4 lg:left-6 xl:left-10 md:w-5 md:h-5 lg:w-6 lg:h-6 xl:w-8 xl:h-8 bg-amber-300 rounded-full">
                                <FaTrophy className="w-full h-full text-black p-1" />
                              </div>
                            )}
                        </div>
                        <div
                          className={`${
                            limit === "ten" ? "text-white" : "text-black"
                          } md:text-sm lg:text-base xl:text-2xl`}
                        >
                          {info?.[element.home_franchise_id]?.code}
                        </div>
                      </div>
                      <div
                        className={`${
                          limit === "ten" ? "text-white" : "text-black"
                        } md:text-sm lg:text-base xl:text-xl`}
                      >
                        VS
                      </div>
                      <div className="flex flex-col items-center space-y-2 p-2">
                        <div className="md:w-6 md:h-6 lg:w-10 lg:h-10 xl:w-14 xl:h-14 relative">
                          <img
                            src={info?.[element.away_franchise_id]?.imagePath}
                            className="w-full h-full object-cover rounded-full"
                          />
                          {events === "previousEvent" &&
                            element.winner_id === element.away_franchise_id && (
                              <div className="absolute -top-1 left-4 lg:left-6 xl:left-10 md:w-5 md:h-5 lg:w-6 lg:h-6 xl:w-8 xl:h-8 bg-amber-300 rounded-full">
                                <FaTrophy className="w-full h-full text-black p-1" />
                              </div>
                            )}
                        </div>
                        <div
                          className={`${
                            limit === "ten" ? "text-white" : "text-black"
                          } md:text-sm lg:text-base xl:text-2xl`}
                        >
                          {info?.[element.away_franchise_id]?.code}
                        </div>
                      </div>
                    </div>
                  )}

                  <div
                    className={`flex justify-center items-center w-full p-2 ${
                      limit === "ten" ? "text-white" : "text-black"
                    } md:text-sm lg:text-base xl:text-lg underline cursor-pointer ${
                      limit === "ten"
                        ? "hover:text-gray-300"
                        : "hover:text-black/80"
                    }`}
                    onClick={() => handleClick()}
                  >
                    View Details
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    )
  );
};

export default EventComponent;
