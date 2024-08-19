import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar from "./Navbar";

const EditContact = () => {
  const [contact, setContact] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { id } = useParams();
  const navigate = useNavigate();

  const fetchContact = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:8000/api/contacts/${id}/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch contact details");
      }

      const data = await response.json();
      setContact(data);
    } catch (err) {
      setError("Unable to load contact.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateContact = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:8000/api/contacts/${id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(contact),
      });

      if (!response.ok) {
        throw new Error("Failed to update contact");
      }

      navigate("/contacts");
    } catch (err) {
      setError("Unable to update contact.");
      console.error(err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setContact({ ...contact, [name]: value });
  };

  useEffect(() => {
    fetchContact();
  }, []);

  if (loading) {
    return <div>Loading contact details...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <>
      <Navbar />
      <div style={styles.container}>
        <h2 style={styles.title}>Edit Contact</h2>
        <form onSubmit={handleUpdateContact} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label} htmlFor="first_name">First Name:</label><br/>
            <input
              type="text"
              id="first_name"
              name="first_name"
              style={styles.input}
              value={contact.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label} htmlFor="last_name">Last Name:</label><br/>
            <input
              type="text"
              id="last_name"
              name="last_name"
              style={styles.input}
              value={contact.last_name}
              onChange={handleChange}
              required
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label} htmlFor="email">Email:</label><br/>
            <input
              type="email"
              id="email"
              name="email"
              style={styles.input}
              value={contact.email}
              onChange={handleChange}
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label} htmlFor="phone">Phone:</label><br/>
            <input
              type="text"
              id="phone"
              name="phone"
              style={styles.input}
              value={contact.phone}
              onChange={handleChange}
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label} htmlFor="notes">Notes:</label><br/>
            <textarea
              id="notes"
              name="notes"
              style={styles.textarea}
              value={contact.notes}
              onChange={handleChange}
            />
          </div>
          <div style={styles.buttonGroup}>
            <button type="submit" style={styles.submitButton}>Save</button>
            <button type="button" onClick={() => navigate("/contacts")} style={styles.cancelButton}>Cancel</button>
          </div>
        </form>
      </div>
    </>
  );
};

const styles = {
  container: {
    margin: "20px auto",
    padding: "20px",
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
    padding: "20px auto",
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
};

export default EditContact;
