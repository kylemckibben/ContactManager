import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar
  from "./Navbar";
const Account = () => {
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { id } = useParams();
  const navigate = useNavigate();

  const fetchAccount = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:8000/api/user/${id}/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch account details");
      }

      const data = await response.json();
      setAccount(data);
    } catch (err) {
      setError("Unable to load account information.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateAccount = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:8000/api/user/${id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(account),
      });

      if (!response.ok) {
        throw new Error("Failed to update account information");
      }

      navigate("/contacts");
    } catch (err) {
      setError("Unable to update account information.");
      console.error(err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAccount({ ...account, [name]: value });
  };

  useEffect(() => {
    fetchAccount();
  }, []);

  if (loading) {
    return <div>Loading account details...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <>
      <Navbar />
      <div style={styles.container}>
        <h2 style={styles.title}>Edit Account</h2>
        <form onSubmit={handleUpdateAccount} style={styles.form}>
          <div style={styles.inputGroup}>
            <div style={styles.inputGroup}>
              <label style={styles.label} htmlFor="username">Username:</label>
              <input
                type="text"
                id="username"
                name="username"
                style={styles.input}
                value={account.username}
                disabled={true}
              />
            </div>
            <div style={styles.inputGroup}>
              <label style={styles.label} htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                name="email"
                style={styles.input}
                value={account.email}
                onChange={handleChange}
              />
            </div>
            <label style={styles.label} htmlFor="first_name">First Name:</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              style={styles.input}
              value={account.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label} htmlFor="last_name">Last Name:</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              style={styles.input}
              value={account.last_name}
              onChange={handleChange}
              required
            />
          </div>
          <div style={styles.buttonGroup}>
            <button type="submit" style={styles.submitButton}>Save</button>
            <button type="button" onClick={() => navigate(`/contacts/`)} style={styles.cancelButton}>Cancel</button>
          </div>
        </form>
      </div>
    </>
  );
};

const styles = {
  container: {
    margin: "20px auto",
    padding: "15px",
    maxWidth: "600px",
    backgroundColor: "lightGray"
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
  },
  label: {
    color: "#000",
  },
  form: {
    padding: "20px",
    borderRadius: "8px",
  },
  inputGroup: {
    marginBottom: "15px",
  },
  input: {
    width: "96%",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "4px",
  },
  textarea: {
    width: "96%",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    minHeight: "100px",
  },
  buttonGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  submitButton: {
    padding: "10px",
    fontSize: "16px",
    backgroundColor: "#4CAF50",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  cancelButton: {
    padding: "10px",
    fontSize: "16px",
    backgroundColor: "#FF6347",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
};

export default Account;
