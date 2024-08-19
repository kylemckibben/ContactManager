// Navbar.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div style={styles.navbar}>
      <button
        style={styles.navbarButton}
        onClick={() => navigate("/contacts")}
      >
        Home
      </button>
      <button
        style={styles.navbarButton}
        onClick={() => navigate(`/user/${localStorage.getItem("id")}`)}
      >
        Account
      </button>
      <button
        style={styles.navbarButtonLogout}
        onClick={handleLogout}
      >
        Logout
      </button>
    </div>
  );
};

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 20px",
    backgroundColor: "#333",
    color: "#fff",
  },
  navbarButton: {
    backgroundColor: "transparent",
    color: "#fff",
    border: "none",
    fontSize: "16px",
    cursor: "pointer",
    margin: "0 10px",
  },
  navbarButtonLogout: {
    backgroundColor: "transparent",
    color: "#fff",
    border: "none",
    fontSize: "16px",
    cursor: "pointer",
    margin: "0 10px",
  },
};

export default Navbar;
