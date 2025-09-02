import { Loader } from "lucide-react";
import React, { useEffect, useState } from "react";
import useDataVariable from "../utils/state";
import app from "../instance/axios";
import { FaTrophy } from "react-icons/fa";

const EventComponent = ({ events }) => {
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
  }
  return (
    matchData &&
    gameData &&
    info && (
      <div className="w-100 max-h-[600px] overflow-y-scroll">
        <div className="flex flex-col gap-8 items-center">
          {array.map((element, index) => {
            const tag =
              events === "currentEvent"
                ? getEventTag(element.match_date, element.match_time, 90)
                : element.round;

            return (
              <div key={index} className="w-full h-60 bg-[#37393F] rounded-lg">
                <div className="space-y-4 p-4">
                  <div className="flex justify-between items-center">
                    <div className="text-white text-xl">
                      {gameData[element.game_id]}
                    </div>
                    <div
                      className={`p-2 rounded-xl border border-amber-300 text-white font-semibold ${
                        tag === "Ongoing" ? "bg-amber-300" : ""
                      }`}
                    >
                      {tag}
                    </div>
                  </div>

                  {info && (
                    <div className="flex justify-evenly items-center">
                      <div className="flex flex-col items-center space-y-2 p-2">
                        <div className="w-10 h-10 relative">
                          <img
                            src={info?.[element.home_franchise_id]?.imagePath}
                            className="w-full h-full object-cover rounded-full"
                          />
                          {events === "previousEvent" &&
                            element.winner_id === element.home_franchise_id && (
                              <div className="absolute -top-1 left-8 w-6 h-6 bg-amber-300 rounded-full">
                                <FaTrophy className="w-full h-full text-black p-1" />
                              </div>
                            )}
                        </div>
                        <div className="text-white text-lg">
                          {info?.[element.home_franchise_id]?.code}
                        </div>
                      </div>
                      <div className="text-white text-lg">VS</div>
                      <div className="flex flex-col items-center space-y-2 p-2">
                        <div className="w-10 h-10 relative">
                          <img
                            src={info?.[element.away_franchise_id]?.imagePath}
                            className="w-full h-full object-cover rounded-full"
                          />
                          {events === "previousEvent" &&
                            element.winner_id === element.away_franchise_id && (
                              <div className="absolute -top-1 left-8 w-6 h-6 bg-amber-300 rounded-full">
                                <FaTrophy className="w-full h-full text-black p-1" />
                              </div>
                            )}
                        </div>
                        <div className="text-white text-lg">
                          {info?.[element.away_franchise_id]?.code}
                        </div>
                      </div>
                    </div>
                  )}

                  <div
                    className="flex justify-center items-center w-full p-4 text-white underline cursor-pointer hover:text-gray-300"
                    onClick={() => {}}
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
