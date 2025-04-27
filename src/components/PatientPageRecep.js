"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"
import "./PatientPage.css"
import { format } from "date-fns"

function PatientPage() {
  const navigate = useNavigate()
  const [expandedPatient, setExpandedPatient] = useState(null)
  const [showPatientDetails, setShowPatientDetails] = useState(false)
  const [showPatientHistory, setShowPatientHistory] = useState(false)
  const [expandedAppointment, setExpandedAppointment] = useState(null)
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [selectedAppointment, setSelectedAppointment] = useState(null)

  // Sample patient data
  const patients = [
    {
      id: 1,
      name: "Andrei Martínez Bahena",
      age: 20,
      address: {
        state: "Morelos",
        municipality: "Amacuzac",
        street: "Juan Alvarez",
        number: "S/N",
      },
      contact: {
        email: "Hungryblock117@Hotmail.com",
        phone1: "734 153 9607",
        phone2: "734 153 1000",
      },
      appointments: [
        {
          id: 1,
          date: "03/02/2025",
          symptoms:
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula auctor eros sed hendrerit. Orci varius natoque penatibus",
          diagnosis:
            "Proin turpis nisl, sagittis a lobortis sit amet, efficitur vel nibh. In et felis fermentum, dictum tortor ut, molestie magna. Proin volutpat augue sollicitudin magna ullamcorper, quis rutrum enim scelerisque.",
          treatment:
            "Proin turpis nisl, sagittis a lobortis sit amet, efficitur vel nibh. In et felis fermentum, dictum tortor ut, molestie magna. Proin volutpat augue sollicitudin magna ullamcorper, quis rutrum enim scelerisque.",
        },
        {
          id: 2,
          date: "15/01/2025",
          symptoms:
            "Dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
          diagnosis:
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
          treatment:
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        },
      ],
    },
    {
      id: 2,
      name: "Aranza Castañeda Juarez",
      age: 25,
      address: {
        state: "Morelos",
        municipality: "Cuernavaca",
        street: "Reforma",
        number: "123",
      },
      contact: {
        email: "aranza.castaneda@gmail.com",
        phone1: "777 123 4567",
        phone2: "",
      },
      appointments: [
        {
          id: 1,
          date: "10/03/2025",
          symptoms: "Dolor de cabeza, fiebre y malestar general.",
          diagnosis: "Infección viral de vías respiratorias superiores.",
          treatment: "Paracetamol 500mg cada 8 horas por 3 días. Reposo y abundantes líquidos.",
        },
      ],
    },
    {
      id: 3,
      name: "Daniela Zayuri Sanchez Gomez",
      age: 30,
      address: {
        state: "Morelos",
        municipality: "Jiutepec",
        street: "Independencia",
        number: "45",
      },
      contact: {
        email: "daniela.sanchez@outlook.com",
        phone1: "777 987 6543",
        phone2: "777 456 7890",
      },
      appointments: [
        {
          id: 1,
          date: "20/02/2025",
          symptoms: "Dolor abdominal, náuseas y vómito.",
          diagnosis: "Gastroenteritis aguda.",
          treatment: "Butilhioscina 10mg cada 8 horas. Dieta blanda y abundantes líquidos.",
        },
        {
          id: 2,
          date: "05/01/2025",
          symptoms: "Tos seca, dolor de garganta y congestión nasal.",
          diagnosis: "Faringitis aguda.",
          treatment: "Ibuprofeno 400mg cada 8 horas por 5 días. Gárgaras con agua tibia y sal.",
        },
      ],
    },
  ]

  // Toggle patient expansion
  const togglePatient = (patientId) => {
    if (expandedPatient === patientId) {
      setExpandedPatient(null)
      setShowPatientDetails(false)
      setShowPatientHistory(false)
    } else {
      setExpandedPatient(patientId)
      const patient = patients.find((p) => p.id === patientId)
      setSelectedPatient(patient)
      setShowPatientDetails(true)
      setShowPatientHistory(false)
    }
  }

  // Toggle appointment expansion
  const toggleAppointment = (appointmentId) => {
    if (expandedAppointment === appointmentId) {
      setExpandedAppointment(null)
    } else {
      setExpandedAppointment(appointmentId)
      const appointment = selectedPatient.appointments.find((a) => a.id === appointmentId)
      setSelectedAppointment(appointment)
    }
  }

  // Show patient history
  const showHistory = () => {
    setShowPatientDetails(false)
    setShowPatientHistory(true)
  }

  // Show patient details
  const showDetails = () => {
    setShowPatientDetails(true)
    setShowPatientHistory(false)
  }

  // Navigate to calendar with new appointment
  const navigateToNewAppointment = () => {
    // Incluir la fecha actual para asegurar que la funcionalidad de horarios inhabilitados funcione correctamente
    const currentDate = new Date()
    navigate("/calendar", {
      state: {
        openNewAppointment: true,
        patientId: selectedPatient.id,
        selectedDate: format(currentDate, "yyyy-MM-dd"),
        fromPatientPage: true, // Añadir un flag para indicar que viene de la página de pacientes
      },
    })
  }

  // Toggle dropdown visibility
  const [showDropdown, setShowDropdown] = useState(false)
  const toggleDropdown = () => {
    setShowDropdown(!showDropdown)
  }

  // Handle logout
  const handleLogout = () => {
    navigate("/login")
  }

  // Icons
  const BellIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
      <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
    </svg>
  )

  const CalendarIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
      <line x1="16" x2="16" y1="2" y2="6" />
      <line x1="8" x2="8" y1="2" y2="6" />
      <line x1="3" x2="21" y1="10" y2="10" />
    </svg>
  )

  const FolderIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>
  )

  const UserIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  )

  const ChevronDownIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 9l6 6 6-6" />
    </svg>
  )

  const ChevronUpIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M18 15l-6-6-6 6" />
    </svg>
  )

  const PlusIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 5v14M5 12h14" />
    </svg>
  )

  return (
    <div className="home-container">
      {/* Header */}
      <header className="home-header">
        <div className="logo-container">
          <div className="logo-circle">
          <img src="/logo.jpg" alt="Logo"/>
          </div>
        </div>
        <div className="banner">
          <span className="banner-text">Para tu salud</span>
        </div>
        <div className="profile-container">
          <div className="profile-circle" onClick={toggleDropdown}>
            <UserIcon />
          </div>
          {showDropdown && (
            <div className="profile-dropdown">
              <button onClick={handleLogout} className="dropdown-item">
                Cerrar sesión
              </button>
              <button className="dropdown-item">Eliminar cuenta</button>
              <div className="dropdown-divider"></div>
            </div>
          )}
        </div>
      </header>

      <div className="divider-line"></div>

      <div className="content-wrapper">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="sidebar-item" onClick={() => navigate("/home")}>
            <BellIcon />
          </div>
          <div className="sidebar-item" onClick={() => navigate("/calendar")}>
            <CalendarIcon />
          </div>
          <div className="sidebar-item active">
            <FolderIcon />
          </div>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          <div className="patients-container">
            {/* Patient List */}
            {patients.map((patient) => (
              <div key={patient.id} className="patient-section">
                <div className="patient-header" onClick={() => togglePatient(patient.id)}>
                  <span className="patient-name">{patient.name}</span>
                  <button className="toggle-button">
                    {expandedPatient === patient.id ? <ChevronUpIcon /> : <ChevronDownIcon />}
                  </button>
                </div>

                {/* Patient Details */}
                {expandedPatient === patient.id && (
                  <div className="patient-details">
                    {showPatientDetails && (
                      <div className="patient-info">
                        <div className="patient-info-header">
                          <h2>{patient.name}</h2>
                          <button className="toggle-button" onClick={() => setShowPatientDetails(false)}>
                            <ChevronUpIcon />
                          </button>
                        </div>

                        <div className="info-field">
                          <label>Edad:</label>
                          <input type="text" value={patient.age} readOnly />
                        </div>

                        <h3>Dirección</h3>
                        <div className="info-row">
                          <div className="info-field">
                            <label>Estado:</label>
                            <input type="text" value={patient.address.state} readOnly />
                          </div>
                          <div className="info-field">
                            <label>Municipio:</label>
                            <input type="text" value={patient.address.municipality} readOnly />
                          </div>
                        </div>
                        <div className="info-row">
                          <div className="info-field">
                            <label>Calle:</label>
                            <input type="text" value={patient.address.street} readOnly />
                          </div>
                          <div className="info-field">
                            <label>Numero:</label>
                            <input type="text" value={patient.address.number} readOnly />
                          </div>
                        </div>

                        <h3>Contacto</h3>
                        <div className="info-field">
                          <label>Correo electrónico:</label>
                          <input type="text" value={patient.contact.email} readOnly />
                        </div>
                        <div className="info-row">
                          <div className="info-field">
                            <label>Teléfono 1:</label>
                            <input type="text" value={patient.contact.phone1} readOnly />
                          </div>
                          <div className="info-field">
                            <label>Teléfono 2:</label>
                            <input type="text" value={patient.contact.phone2} readOnly />
                          </div>
                        </div>

                        <div className="patient-actions">
                          <button className="appointment-button" onClick={navigateToNewAppointment}>
                            Nueva cita <PlusIcon />
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Patient History */}
                    {showPatientHistory && (
                      <div className="patient-history">
                        <div className="history-header">
                          <h2>Historial de {patient.name}</h2>
                          <button className="back-button" onClick={showDetails}>
                            Volver
                          </button>
                        </div>

                        <div className="appointments-list">
                          {patient.appointments.map((appointment) => (
                            <div key={appointment.id} className="appointment-item">
                              <div className="appointment-header" onClick={() => toggleAppointment(appointment.id)}>
                                <span className="appointment-date">{appointment.date}</span>
                                <button className="toggle-button">
                                  {expandedAppointment === appointment.id ? <ChevronUpIcon /> : <ChevronDownIcon />}
                                </button>
                              </div>

                              {expandedAppointment === appointment.id && (
                                <div className="appointment-details">
                                  <div className="medical-section">
                                    <h3>Síntomas:</h3>
                                    <div className="medical-text">{appointment.symptoms}</div>
                                  </div>

                                  <div className="medical-section">
                                    <h3>Diagnóstico:</h3>
                                    <div className="medical-text">{appointment.diagnosis}</div>
                                  </div>

                                  <div className="medical-section">
                                    <h3>Tratamiento</h3>
                                    <div className="medical-text">{appointment.treatment}</div>
                                  </div>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  )
}

export default PatientPage
