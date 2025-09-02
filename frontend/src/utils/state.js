// store/leaderboardStore.js
import { create } from "zustand";

const useDataVariable = create((set, get) => ({
  leaderBoard: {},
  imageInfo: [],
  matchDetails: [],

  leaderBoardDataFiltering: (dataSet1, dataSet2) => {
    let filteredData = {};
    const idSet = dataSet1.map((item) => item.id);

    idSet.forEach((idValue) => {
      const info = dataSet1.find((item) => item.id === idValue);
      const points = dataSet2.find((item) => item.id === idValue);
      filteredData[idValue] = {
        name: info.name,
        code: info.franchise_code,
        imagePath: info.logo_path,
        totalScore: points.total_points,
        wonScore: points.matches_won,
        lostScore: points.matches_lost,
        totalMatches: points.matches_played,
      };
    });

    set({ leaderBoard: filteredData });
    return filteredData;
  },

  getImageInformation: (dataSet1, dataSet2) => {
    set({ matchDetails: dataSet2 });
    const data = get().leaderBoard;
    const tempList = dataSet1.map((obj) => ({
      imagePath: obj.image_path,
      game: obj.title,
      matchId: obj.match_id,
    }));

    const tempMap = Object.fromEntries(dataSet2.map((t) => [t.id, t]));

    const filteredList = tempList.map((obj) => {
      const info = tempMap[obj.matchId];
      return {
        ...obj,
        ...(info
          ? {
              team1: data[`${info.home_franchise_id}`]?.code,
              team2: data[`${info.away_franchise_id}`]?.code,
              iconPath1: data[`${info.home_franchise_id}`]?.imagePath,
              iconPath2: data[`${info.away_franchise_id}`]?.imagePath,
              date: info.match_date,
            }
          : {}),
      };
    });

    set({ imageInfo: filteredList });
    return filteredList;
  },
}));

export default useDataVariable;
