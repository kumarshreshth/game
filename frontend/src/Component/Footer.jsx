import React from "react";

const Footer = () => {
  return (
    <div className="w-full p-6 bg-[#37393F]">
      <div className="flex justify-between items-center">
        <div className="w-1/6 h-10">
          <img
            src="/images/footerLogo.png"
            className="w-full h-full object-contain"
          />
        </div>
        <div className="flex flex-row items-center gap-4 underline text-base text-white">
          <div>Sport Guidelines</div>
          <div>Contact Us</div>
        </div>
      </div>
    </div>
  );
};

export default Footer;
