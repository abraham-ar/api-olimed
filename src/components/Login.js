"use client"

import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import "./Auth.css"

function Login() {
  const [showPassword, setShowPassword] = useState(false)
  const [clave, setClave] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log("Login attempt with:", { clave, password })

    let role = ""

    if (clave === "Medico123") {
      role = "medico"
    } else if (clave === "Recep456") {
      role = "recepcionista"
    } else if (clave === "Patient") {
      role = "paciente"
    }else {
      alert("Clave incorrecta. Intenta con una clave válida.")
      return
    }

    localStorage.setItem("userRole", role)
    navigate("/home")
  }

  const EyeIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  )

  const EyeOffIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
      <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68" />
      <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61" />
      <line x1="2" x2="22" y1="2" y2="22" />
    </svg>
  )

  return (
    <div className="auth-container">
      <div className="auth-wrapper">
        <div className="logo-section">
          <div className="logo-circle">
            <h1 className="logo-text">LOGO</h1>
          </div>
        </div>

        <div className="form-section">
          <div className="form-container">
            <h2 className="form-title">INICIO DE SESIÓN</h2>

            <form onSubmit={handleSubmit}>
              <div className="form-fields">
                <div className="form-field">
                  <label htmlFor="clave" className="field-label">
                    Clave de acceso
                  </label>
                  <input
                    id="clave"
                    type="text"
                    value={clave}
                    onChange={(e) => setClave(e.target.value)}
                    className="field-input"
                    placeholder="Ej. claveMedico123"
                    required
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="password" className="field-label">
                    Contraseña
                  </label>
                  <div className="password-field">
                    <input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="field-input"
                      required
                    />
                    <button type="button" className="password-toggle" onClick={() => setShowPassword(!showPassword)}>
                      {showPassword ? <EyeOffIcon /> : <EyeIcon />}
                    </button>
                  </div>
                </div>

                <div className="forgot-password">
                  <Link to="/recover-password" className="link">
                    Recuperar contraseña
                  </Link>
                </div>

                <button type="submit" className="submit-button">
                  Iniciar sesión
                </button>

                <div className="auth-footer">
                  <p className="footer-text">
                    ¿No tienes una cuenta?{" "}
                    <Link to="/register" className="link">
                      Regístrate aquí
                    </Link>
                  </p>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
