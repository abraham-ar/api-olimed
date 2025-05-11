"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"
import "./HomePage.css"

function HomePage() {
  const [showDropdown, setShowDropdown] = useState(false)
  const navigate = useNavigate()

  // Toggle dropdown visibility
  const toggleDropdown = () => {
    setShowDropdown(!showDropdown)
  }

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem("userToken")
    localStorage.removeItem("userRole")

    // Redirect to login
    navigate("/login")
  }
  

  // Handle account deletion
  const handleDeleteAccount = async () => {
    const confirmed = window.confirm("¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer.")
  
    if (!confirmed) return
  
    try {
      const token = localStorage.getItem("userToken")
      const userId = localStorage.getItem("userId")
  
      const response = await fetch(`http://localhost:8000/paciente/${userId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      })
  
      if (!response.ok) {
        throw new Error("Error al eliminar la cuenta")
      }
  
      localStorage.removeItem("userToken")
      localStorage.removeItem("userId")
      localStorage.removeItem("userRole")
      alert("Tu cuenta ha sido eliminada.")
      navigate("/login")
    } catch (error) {
      console.error("Error:", error)
      alert("Hubo un error al intentar eliminar la cuenta.")
    }
  }
  

  // Sample notification data
  const notifications = [
    {
      id: 1,
      type: "user",
      content:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula auctor eros sed hendrerit. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas tincidunt ex eget tincidunt sagittis",
    },
    {
      id: 2,
      type: "calendar",
      content:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula auctor eros sed hendrerit. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas tincidunt ex eget tincidunt sagittis",
    },
    {
      id: 3,
      type: "payment",
      content:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula auctor eros sed hendrerit. "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula auctor eros sed hendrerit. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas tincidunt ex eget tincidunt sagittis',
    },
    {
      id: 4,
      type: "user",
      content:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula auctor eros sed hendrerit. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas tincidunt ex eget tincidunt sagittis",
    },
  ]

  // Icons for the sidebar and notifications
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

  const SettingsIcon = () => (
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
      <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
      <circle cx="12" cy="12" r="3" />
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

  // Function to render the appropriate icon based on notification type
  const renderNotificationIcon = (type) => {
    switch (type) {
      case "user":
        return <UserIcon />
      case "calendar":
        return <CalendarIcon />
      case "payment":
        return <PaymentIcon />
      default:
        return <UserIcon />
    }
  }

  const PaymentIcon = () => (
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
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <circle cx="12" cy="14" r="2" />
      <path d="M14 2v4a2 2 0 0 0 2 2h4" />
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
              <button onClick={handleDeleteAccount} className="dropdown-item">
                Eliminar cuenta
              </button>
              <div className="dropdown-divider"></div>
            </div>
          )}
        </div>
      </header>

      <div className="divider-line"></div>

      <div className="content-wrapper">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="sidebar-item active">
            <BellIcon />
          </div>
          <div className="sidebar-item" onClick={() => navigate("/calendar")}>
            <CalendarIcon />
          </div>
          <div className="sidebar-item" onClick={() => navigate("/patients")}>
            <FolderIcon />
          </div>
          <div className="sidebar-item" onClick={() => navigate("/settings")}>
            <SettingsIcon />
          </div>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {notifications.map((notification) => (
            <div className="notification-item" key={notification.id}>
              <div className="notification-icon">{renderNotificationIcon(notification.type)}</div>
              <div className="notification-content">
                <p>{notification.content}</p>
              </div>
            </div>
          ))}
        </main>
      </div>
    </div>
  )
}

export default HomePage