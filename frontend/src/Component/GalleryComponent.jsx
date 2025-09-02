import { Loader } from "lucide-react";
import React, { useState, useEffect } from "react";
import app from "../instance/axios.js";
import { FaArrowLeft } from "react-icons/fa6";
import { FaArrowRight, FaTimes } from "react-icons/fa";
import useDataVariable from "../utils/state.js";
import { MdExpand, MdExpandMore } from "react-icons/md";
import { FiMaximize } from "react-icons/fi";
import { BiExpand } from "react-icons/bi";

const GalleryComponent = () => {
  const [loading, setLoading] = useState(true);
  const [imageData, setImageData] = useState(null);
  const [page, setPage] = useState(0);
  const [imageViewer, setImageViewer] = useState(false);
  const [filePath, setFilePath] = useState("");
  const { leaderBoard, getImageInformation } = useDataVariable();

  let imagePerPage = 6,
    startIndex,
    visibleImageList;

  if (imageData) {
    startIndex = page * imagePerPage;
    visibleImageList = imageData.slice(startIndex, startIndex + imagePerPage);
  }

  const formatDate = (date) => {
    const dateObj = new Date(date);
    const options = { day: "2-digit", month: "long" };

    return dateObj.toLocaleDateString("en-US", options);
  };

  const handleNext = () => {
    if (startIndex + imagePerPage < imageData.length) {
      setPage(page + 1);
    }
  };

  const handlePrev = () => {
    if (page > 0) {
      setPage(page - 1);
    }
  };

  const openImage = (path) => {
    setImageViewer(true);
    setFilePath(path);
  };

  const closeImage = (path) => {
    setImageViewer(false);
    setFilePath("");
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const imageCollection = await app.get(
          "/api/v1/gallery/?skip=0&limit=100"
        );
        const matchDetailCollection = await app.get(
          "/api/v1/matches/?skip=0&limit=100"
        );

        if (imageCollection.data && matchDetailCollection.data) {
          const filteredImages = getImageInformation(
            imageCollection.data,
            matchDetailCollection.data
          );
          setImageData(filteredImages);
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
  }, [leaderBoard]);

  if (loading)
    return (
      <div className="flex justify-center items-center h-40">
        <Loader className="animate-spin w-10 h-10 text-white" />
      </div>
    );

  if (!imageData) {
    return (
      <div className="w-full h-85">
        <img
          className="w-full h-full object-contain rounded-xl"
          src="./images/galleryPlaceholder.png"
        />
      </div>
    );
  }

  return (
    <div>
      <div>
        <div className="grid grid-cols-3 gap-8">
          {visibleImageList.map((element, index) => (
            <div key={index} className="relative w-full h-80 group">
              <img
                src={element.imagePath}
                className="w-full h-full object-cover rounded-xl"
              />
              <div className="absolute bottom-0 left-0 w-full h-1/2 bg-[#9797DE] opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-b-xl">
                <div className="flex flex-row justify-between item-start m-8">
                  <div className="space-y-4">
                    <div className="flex flex-row gap-4 items-center">
                      <div className="flex flex-col items-center space-y-2 p-2">
                        <div className="w-8 h-8">
                          <img
                            src={element.iconPath1}
                            className="w-full h-full object-cover rounded-full"
                          />
                        </div>
                        <div>{element.team1}</div>
                      </div>
                      <div>VS</div>
                      <div className="flex flex-col items-center space-y-2 p-2">
                        <div className="w-8 h-8">
                          <img
                            src={element.iconPath2}
                            className="w-full h-full object-cover rounded-full"
                          />
                        </div>
                        <div>{element.team2}</div>
                      </div>
                    </div>
                    <div className="flex gap-4 items-center">
                      <div className="text-base">
                        {element.game.split("M")[0].trim()}
                      </div>
                      <div className="w-0.5 h-5 bg-black"></div>
                      <div className="text-base">
                        {formatDate(element.date)}
                      </div>
                    </div>
                  </div>

                  <div
                    className="p-2"
                    onClick={() => openImage(element.imagePath)}
                  >
                    <BiExpand className="text-xl text-black cursor-pointer hover:text-white" />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 flex justify-center items-center gap-10">
          <FaArrowLeft
            className="text-2xl text-white cursor-pointer hover:text-gray-400"
            onClick={() => handlePrev()}
          />
          <FaArrowRight
            className="text-2xl text-white cursor-pointer hover:text-gray-400"
            onClick={() => handleNext()}
          />
        </div>
      </div>

      <div className="mt-10 w-full">
        <div className="flex justify-center items-center">
          <div className="pl-6 pr-6 pt-2 pb-2 bg-yellow-300 rounded-xl font-bold cursor-pointer hover:bg-yellow-300/60">
            View All
          </div>
        </div>
      </div>

      {imageViewer && (
        <div className="fixed inset-0 w-full h-screen bg-black/60 flex items-center justify-center">
          <div className="relative w-5/6 h-[600px] flex justify-center items-center">
            <img src={filePath} className="w-full h-full object-contain" />

            <button className="absolute top-4 right-4">
              <FaTimes
                className="text-2xl text-white hover:text-gray-400 cursor-pointer"
                onClick={() => closeImage()}
              />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GalleryComponent;
