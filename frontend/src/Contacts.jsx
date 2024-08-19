import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import { fuzzySearch } from "./utility/fuzzySearch";

const ContactsPage = () => {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [query, setQuery] = useState("");
  const [newContact, setNewContact] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    notes: ""
  });
  const navigate = useNavigate();

  const fetchContacts = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await fetch("http://localhost:8000/api/contacts/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch contacts");
      }

      const data = await response.json();
      setContacts(data);
    } catch (err) {
      setError("Unable to load contacts.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddContact = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:8000/api/contacts/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(newContact),
      });

      if (!response.ok) {
        throw new Error("Failed to add contact");
      }

      const data = await response.json();
      setContacts([...contacts, data]);
      setNewContact({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        notes: ""
      });
      setShowForm(false);
    } catch (err) {
      setError("Unable to add contact.");
      console.error(err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewContact({ ...newContact, [name]: value });
  };

  const handleCancel = () => {
    setShowForm(false);
    setNewContact({
      first_name: "",
      last_name: "",
      email: "",
      phone: "",
      notes: ""
    });
  };

  const handleDelete = async (id) => {
    try {
      const token = localStorage.getItem("token");
      await fetch(`http://localhost:8000/api/contacts/${id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
      });
      fetchContacts();
    } catch (error) {
      console.error('Error deleting contact:', error);
    }
  };

  const filteredContacts = contacts.filter(contact => {
    const fullName = `${contact.first_name} ${contact.last_name}`.toLowerCase();
    return fullName.includes(query.toLowerCase());
  });

  useEffect(() => {
    fetchContacts();
  }, []);

  if (loading) {
    return <div>Loading contacts...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <>
      <Navbar />
      <div style={styles.container}>
        <h2 style={styles.title}>Your Contacts</h2>
        {!showForm && (
          <button
            onClick={() => setShowForm(true)}
            style={styles.toggleFormButton}
          >
            Add New Contact
          </button>
        )}
        <input
          type="text"
          placeholder="Search contacts by name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.searchInput}
        />
        {showForm && (
          <form onSubmit={handleAddContact} style={styles.form}>
            <div style={styles.inputGroup}>
              <label htmlFor="first_name">First Name:</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                style={styles.input}
                value={newContact.first_name}
                onChange={handleChange}
                required
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="last_name">Last Name:</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                style={styles.input}
                value={newContact.last_name}
                onChange={handleChange}
                required
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                name="email"
                style={styles.input}
                value={newContact.email}
                onChange={handleChange}
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="phone">Phone:</label>
              <input
                type="text"
                id="phone"
                name="phone"
                style={styles.input}
                value={newContact.phone}
                onChange={handleChange}
              />
            </div>
            <div style={styles.inputGroup}>
              <label htmlFor="notes">Notes:</label>
              <textarea
                id="notes"
                name="notes"
                style={styles.textarea}
                value={newContact.notes}
                onChange={handleChange}
              />
            </div>
            <button type="submit" style={styles.submitButton}>Add Contact</button>
            <button type="button" onClick={handleCancel} style={styles.cancelButton}>Cancel</button>
          </form>
        )}
        {filteredContacts.length > 0 ? (
          <ul style={styles.list}>
            {filteredContacts.map((contact) => (
              <li key={contact.id} style={styles.listItem}>
                <div style={styles.contactInfo}>
                  <strong>{contact.first_name} {contact.last_name} | </strong>
                  <em><strong>Email</strong>: {contact.email} </em>
                  <span> </span>
                  <em><strong>Phone</strong>: {contact.phone}</em> <br />
                  <em><strong>Notes</strong>: {contact.notes}</em> <br />
                </div>
                <div style={styles.buttonContainer}>
                  <button
                    onClick={() => navigate(`/contacts/edit/${contact.id}`)}
                    style={styles.editButton}
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(contact.id)}
                    style={styles.deleteButton}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div>No contacts found.</div>
        )}
      </div>
    </>
  );
};

const styles = {
  container: {
    padding: "20px",
    margin: "20px auto",
    backgroundColor: "lightGray",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
  },
  searchInput: {
    width: "100%",
    padding: "10px",
    marginBottom: "20px",
    borderRadius: "4px",
    border: "1px solid #ccc",
    fontSize: "16px",
  },
  list: {
    listStyleType: "none",
    padding: 0,
  },
  listItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px",
    borderBottom: "1px solid #ccc",
    backgroundColor: "darkGray",
    marginBottom: "10px",
  },
  contactInfo: {
    flex: 1,
    paddingRight: "10px",
  },
  buttonContainer: {
    display: "flex",
    gap: "10px",
  },
  editButton: {
    padding: "5px 10px",
    fontSize: "14px",
    backgroundColor: "#1E90FF",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  deleteButton: {
    padding: "5px",
    fontSize: "14px",
    backgroundColor: "#f44336",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  toggleFormButton: {
    display: "block",
    marginBottom: "20px",
    padding: "10px",
    backgroundColor: "#4CAF50",
    color: "#fff",
    fontSize: "16px",
    border: "none",
    cursor: "pointer",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    margin: "20px auto",
    maxWidth: "600px"
  },
  inputGroup: {
    marginBottom: "15px",
  },
  input: {
    padding: "10px",
    fontSize: "16px",
    width: "96%",
  },
  textarea: {
    padding: "10px",
    fontSize: "16px",
    width: "96%",
    height: "80px",
  },
  submitButton: {
    padding: "10px",
    backgroundColor: "#4CAF50",
    color: "#fff",
    fontSize: "16px",
    border: "none",
    cursor: "pointer",
  },
  cancelButton: {
    marginTop: "10px",
    padding: "10px",
    backgroundColor: "#f44336",
    color: "#fff",
    fontSize: "16px",
    border: "none",
    cursor: "pointer",
  },
};


export default ContactsPage;
