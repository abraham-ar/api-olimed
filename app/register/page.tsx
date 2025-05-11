"use client"

import React from "react"

import { useState } from "react"
import Link from "next/link"
import { EyeOff, Eye } from "lucide-react"

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [name, setName] = useState("")
  const [age, setAge] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [acceptTerms, setAcceptTerms] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle registration logic here
    console.log("Registration attempt with:", { name, age, email, password, acceptTerms })
  }

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url(/images/background.png)" }}
    >
      <div className="w-full max-w-6xl flex items-center justify-center p-4">
        {/* Form Section */}
        <div className="w-full max-w-md">
          <div className="bg-gray-100/90 backdrop-blur-sm rounded-3xl p-8 shadow-lg">
            <div className="flex justify-between items-start">
              <h2 className="text-2xl font-semibold text-navy-800 mb-6">REGISTRO</h2>

              {/* Logo on the right side for larger screens */}
              <div className="hidden md:flex">
                <div className="bg-gray-200 rounded-full w-32 h-32 flex items-center justify-center">
                  <h1 className="text-2xl font-bold text-gray-800">LOGO</h1>
                </div>
              </div>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-navy-700 mb-2">
                    Nombre
                  </label>
                  <input
                    id="name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white border-0 focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="age" className="block text-sm font-medium text-navy-700 mb-2">
                    Edad
                  </label>
                  <input
                    id="age"
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white border-0 focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="register-email" className="block text-sm font-medium text-navy-700 mb-2">
                    Correo electronico o telefono
                  </label>
                  <input
                    id="register-email"
                    type="text"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white border-0 focus:ring-2 focus:ring-blue-500"
                    placeholder="ejemplo@ejemplo.com"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="register-password" className="block text-sm font-medium text-navy-700 mb-2">
                    Contraseña
                  </label>
                  <div className="relative">
                    <input
                      id="register-password"
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

                <div className="flex items-center">
                  <input
                    id="terms"
                    type="checkbox"
                    checked={acceptTerms}
                    onChange={(e) => setAcceptTerms(e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    required
                  />
                  <label htmlFor="terms" className="ml-2 block text-sm text-navy-700">
                    Acepto{" "}
                    <Link href="/terms" className="text-blue-700 underline">
                      terminos y condiciones
                    </Link>
                  </label>
                </div>

                <button
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition duration-300 mt-4"
                  disabled={!acceptTerms}
                >
                  Registrarse
                </button>

                <div className="text-center mt-4">
                  <p className="text-sm text-navy-700">
                    Ya tienes cuenta?{" "}
                    <Link href="/login" className="text-blue-700 hover:underline">
                      Iniciar Sesión
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

