import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [contacts, setContacts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentContact, setCurrentContact] = useState({});
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    try {
      setLoading(true);
      let url = "http://localhost:5000/contacts";
      if (searchTerm) {
        url += "?search=" + encodeURIComponent(searchTerm);
      }
      const response = await fetch(url);
      const data = await response.json();
      setContacts(data.contacts);
    } catch (error) {
      console.error("Error fetching contacts:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContacts();
  }, [searchTerm]);

  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentContact({});
  };

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true);
  };

  const openEditModal = (contact) => {
    if (isModalOpen) return;
    setCurrentContact(contact);
    setIsModalOpen(true);
  };

  const onUpdate = () => {
    closeModal();
    fetchContacts();
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Contact Management System</h1>
        <p>Manage your contacts efficiently</p>
      </header>
      
      <main className="app-main">
        <div className="controls">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Search contacts..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-field"
            />
          </div>
          <button className="create-btn" onClick={openCreateModal}>
            + Add New Contact
          </button>
        </div>

        {loading ? (
          <div className="loading">Loading contacts...</div>
        ) : (
          <div className="contact-list">
            <h2>Contacts ({contacts.length})</h2>
            <div className="contacts-grid">
              {contacts.map((contact) => (
                <div key={contact.id} className="contact-card">
                  <div className="contact-header">
                    <h3>{contact.firstName} {contact.lastName}</h3>
                    <div className="contact-actions">
                      <button onClick={() => openEditModal(contact)}>✏️</button>
                      <button onClick={() => handleDelete(contact.id)}>🗑️</button>
                    </div>
                  </div>
                  <p>📧 {contact.email}</p>
                  {contact.phone && <p>📞 {contact.phone}</p>}
                  {contact.category && <span className="category-badge">{contact.category}</span>}
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {isModalOpen && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <span className="close" onClick={closeModal}>&times;</span>
            <ContactForm existingContact={currentContact} updateCallback={onUpdate} />
          </div>
        </div>
      )}
    </div>
  );
}

function ContactForm({ existingContact = {}, updateCallback }) {
  const [formData, setFormData] = useState({
    firstName: existingContact.firstName || "",
    lastName: existingContact.lastName || "",
    email: existingContact.email || "",
    phone: existingContact.phone || "",
    category: existingContact.category || ""
  });

  const updating = Object.keys(existingContact).length > 0;

  const onSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = "http://localhost:5000/" + (updating ? `update_contact/${existingContact.id}` : "create_contact");
      const options = {
        method: updating ? "PATCH" : "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      };

      const response = await fetch(url, options);
      const data = await response.json();

      if (response.ok) {
        updateCallback();
      } else {
        alert(data.message || "An error occurred");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("An error occurred while saving the contact");
    }
  };

  return (
    <div className="contact-form">
      <h2>{updating ? "Edit Contact" : "Add New Contact"}</h2>
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label>First Name *</label>
          <input
            type="text"
            value={formData.firstName}
            onChange={(e) => setFormData({...formData, firstName: e.target.value})}
            required
          />
        </div>
        <div className="form-group">
          <label>Last Name *</label>
          <input
            type="text"
            value={formData.lastName}
            onChange={(e) => setFormData({...formData, lastName: e.target.value})}
            required
          />
        </div>
        <div className="form-group">
          <label>Email *</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            required
          />
        </div>
        <div className="form-group">
          <label>Phone</label>
          <input
            type="tel"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
          />
        </div>
        <div className="form-group">
          <label>Category</label>
          <select
            value={formData.category}
            onChange={(e) => setFormData({...formData, category: e.target.value})}
          >
            <option value="">Select category</option>
            <option value="Personal">Personal</option>
            <option value="Work">Work</option>
            <option value="Family">Family</option>
            <option value="Friends">Friends</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <button type="submit" className="submit-btn">
          {updating ? "Update Contact" : "Create Contact"}
        </button>
      </form>
    </div>
  );
}

export default App;
