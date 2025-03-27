import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import "./App.css"
import Login from "./components/Login"
import Register from "./components/Register"
import RecoverPassword from "./components/RecoverPassword"
import HomePage from "./components/HomePage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/recover-password" element={<RecoverPassword />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

