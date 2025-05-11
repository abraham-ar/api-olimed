"use client"

import React from "react"

import { useState } from "react"
import Link from "next/link"
import { EyeOff, Eye } from "lucide-react"

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle login logic here
    console.log("Login attempt with:", { email, password })
  }

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url(/images/background.png)" }}
    >
      <div className="w-full max-w-6xl flex items-center justify-center p-4">
        {/* Logo Section */}
        <div className="hidden md:flex md:w-1/2 justify-center items-center">
          <div className="bg-gray-100 rounded-full w-64 h-64 flex items-center justify-center">
            <h1 className="text-4xl font-bold text-gray-800">LOGO</h1>
          </div>
        </div>

        {/* Form Section */}
        <div className="w-full md:w-1/2 max-w-md">
          <div className="bg-gray-100/90 backdrop-blur-sm rounded-3xl p-8 shadow-lg">
            <h2 className="text-2xl font-semibold text-center text-navy-800 mb-6">INICIO DE SESIÓN</h2>

            <form onSubmit={handleSubmit}>
              <div className="space-y-6">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-navy-700 mb-2">
                    Correo electronico o telefono
                  </label>
                  <input
                    id="email"
                    type="text"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white border-0 focus:ring-2 focus:ring-blue-500"
                    placeholder="ejemplo@ejemplo.com"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-navy-700 mb-2">
                    Contraseña
                  </label>
                  <div className="relative">
                    <input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full px-4 py-3 rounded-lg bg-white border-0 focus:ring-2 focus:ring-blue-500"
                      required
                    />
                    <button
                      type="button"
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? (
                        <EyeOff className="h-5 w-5 text-navy-600" />
                      ) : (
                        <Eye className="h-5 w-5 text-navy-600" />
                      )}
                    </button>
                  </div>
                </div>

                <div className="text-right">
                  <Link href="/recover-password" className="text-sm text-blue-700 hover:underline">
                    Recuperar contraseña
                  </Link>
                </div>

                <button
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition duration-300"
                >
                  Iniciar sesión
                </button>

                <div className="text-center mt-4">
                  <p className="text-sm text-navy-700">
                    No tienes una cuenta?{" "}
                    <Link href="/register" className="text-blue-700 hover:underline">
                      Registrate aquí
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

