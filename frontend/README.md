# Game Tournament Platform Frontend

A modern, responsive web application for managing and showcasing gaming tournaments, built with React and Vite.

## 🎮 Project Overview

This is a frontend application designed to manage and display gaming tournament information, leaderboards, events, and a media gallery. The platform features a sleek, dark-themed UI with modern design elements and interactive components.

## 🚀 Features

- **Dynamic Homepage** with video background and engaging UI
- **Current & Previous Events** display
- **Live Leaderboard** tracking
- **Image Gallery** showcasing tournament moments
- **Team Franchises** showcase
  - AMC Warriors
  - CDD Daredevils
  - DFOI Titans
  - SS Super Kings
- **Real-time Updates** using modern state management
- **Responsive Design** for all device sizes

## 🛠️ Tech Stack

- **Frontend Framework:** React 19
- **Build Tool:** Vite
- **Routing:** React Router DOM v7
- **State Management:** Zustand
- **HTTP Client:** Axios
- **Styling:** TailwindCSS
- **Icons:** React Icons, Lucide React
- **Code Quality:** ESLint

## 📁 Project Structure

```
frontend/
├── public/
│   └── images/            # Static images and media assets
│       ├── franchises/    # Team franchise logos
│       └── gallery/       # Tournament photo gallery
├── src/
│   ├── Component/        # Reusable UI components
│   ├── Pages/           # Page components
│   ├── instance/        # Axios instance configuration
│   └── utils/           # Utility functions and state management
```

## 🚀 Getting Started

1. **Install Dependencies**

   ```bash
   npm install
   ```

2. **Run Development Server**

   ```bash
   npm run dev
   ```

3. **Build for Production**

   ```bash
   npm run build
   ```

4. **Preview Production Build**
   ```bash
   npm run preview
   ```

## 🧩 Key Components

- **HomePage:** Main landing page with video background and content sections
- **EventComponent:** Displays tournament events information
- **LeaderBoard:** Shows current tournament standings
- **GalleryComponent:** Media gallery for tournament photos
- **Marquee:** Animated announcements and updates
- **Footer:** Site footer with navigation and information

## 🔧 Configuration

The project uses standard Vite configuration with ESLint for code quality. Configuration files include:

- `vite.config.js`
- `eslint.config.js`

## 🎨 Design

The application features a dark theme with:

- Primary background: #202225
- Modern UI components
- Responsive design
- Interactive elements
- Video backgrounds
- High-quality imagery

## 📝 License

This project is private and proprietary. All rights reserved.

## 🛠️ Development

The project follows modern React practices including:

- Functional components
- React Hooks
- Component-based architecture
- Modular styling
- State management with Zustand
