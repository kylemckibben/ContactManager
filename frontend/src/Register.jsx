import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const checkUserExists = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/user/exists/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email }),
      });

      if (response.status == 200) {
        setError("");
        return false;
      } else {
        setError("Username or email already exists");
        return true;
      }
    } catch (error) {
      console.error("Error checking user existence:", error);
      setError("An error occurred while checking the username or email.");
    }
  };


  const handleRegister = async (e) => {
    e.preventDefault();
    const exists = await checkUserExists();

    if (exists) {
      return;
    }

    if (password !== passwordConfirm) {
      setError("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/user/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
          email: email,
          first_name: firstName,
          last_name: lastName,
        }),
      });

      if (!response.ok) {
        throw new Error("Registration failed");
      }

      navigate("/login");
    } catch (error) {
      console.error("Registration failed: ", error);
      setError("")
    }
  }

  return (
    <>
      <div style={styles.container}>
        <div style={styles.card}>
          <h2 style={styles.title}>Register</h2>
          <form onSubmit={handleRegister}>
            {error && <div style={styles.error}>{error}</div>}
            <div style={styles.inputGroup}>
              <label htmlFor="username">Username:</label>
              <input
                type="text"
                id="username"
                style={styles.input}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="password">Password:</label>
              <input
                type="password"
                id="password"
                style={styles.input}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="password">Confirm password:</label>
              <input
                type="password"
                id="password"
                style={styles.input}
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                style={styles.input}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="first_name">First name:</label>
              <input
                type="text"
                id="first_name"
                style={styles.input}
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="last_name">Last name:</label>
              <input
                type="text"
                id="last_name"
                style={styles.input}
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>
            <div style={styles.buttonContainer}>
              <button type="submit" style={styles.submitButton}>
                Register
              </button>
              <button
                onClick={() => navigate("/login")}
                style={styles.cancelButton}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

const styles = {
  container: {
    maxWidth: "400px",
    margin: "50px auto",
    padding: "20px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    textAlign: "center",
    backgroundColor: "lightGray"
  },
  form: {
    display: "flex",
    flexDirection: "column",
  },
  inputGroup: {
    marginBottom: "15px",
  },
  input: {
    width: "95%",
    padding: "10px",
    fontSize: "16px",
  },
  buttonContainer: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    gap: "10px",
  },
  submitButton: {
    padding: "10px 20px",
    backgroundColor: "#4CAF50",
    color: "#fff",
    fontSize: "16px",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  cancelButton: {
    padding: "10px",
    backgroundColor: "#FF6347",
    color: "#fff",
    fontSize: "16px",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  error: {
    color: "red",
    marginBottom: "15px",
  },
};

export default Register;