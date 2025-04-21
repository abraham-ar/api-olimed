import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import Login from "./components/Login"
import Register from "./components/Register"
import RecoverPassword from "./components/RecoverPassword"
import HomePage from "./components/HomePage"
import CalendarPage from "./components/CalendarPage"
import PatientPage from "./components/PatientPage"
import SettingsPage from "./components/SettingsPage"

import HomePageRecep from "./components/HomePageRecep"
import CalendarPageRecep from "./components/CalendarPageRecep"
import PatientPageRecep from "./components/PatientPageRecep"

import "./App.css"

function App() {
  const userRole = localStorage.getItem("userRole")

  const getHomeComponent = () => {
    if (userRole === "recepcionista") return <HomePageRecep />
    return <HomePage />
  }

  const getCalendarComponent = () => {
    if (userRole === "recepcionista") return <CalendarPageRecep />
    return <CalendarPage />
  }

  const getPatientComponent = () => {
    if (userRole === "recepcionista") return <PatientPageRecep />
    return <PatientPage />
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/recover-password" element={<RecoverPassword />} />
        <Route path="/home" element={getHomeComponent()} />
        <Route path="/calendar" element={getCalendarComponent()} />
        <Route path="/patients" element={getPatientComponent()} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  )
}

export default App
