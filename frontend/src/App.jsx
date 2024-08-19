import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import ContactsPage from "./Contacts";
import EditContact from "./EditContact";
import Account from "./Account";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/contacts" element={<ContactsPage />} />
        <Route path="/contacts/edit/:id" element={<EditContact />} />
        <Route path="/user/:id" element={<Account />} />
      </Routes>
    </Router>
  );
};

export default App;
