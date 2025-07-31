"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function Home() {
  const [notes, setNotes] = useState([]);
  const [name, setName] = useState("");
  const [noteText, setNoteText] = useState("");
  const [editingId, setEditingId] = useState(null);

  const API = "http://localhost:8000/notes/notes/"; 
  const fetchNotes = async () => {
    try {
      const res = await axios.get(API);
      setNotes(res.data);
    } catch (err) {
      console.error("Error fetching notes:", err);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  // Submit: Create or Update
  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { name, node: noteText };

    try {
      if (editingId) {
        const res = await axios.put(API + editingId, data);
        setNotes(notes.map((n) => (n.id === editingId ? res.data : n)));
      } else {
        const res = await axios.post(API, data);
        setNotes([res.data, ...notes]);
      }
      setName("");
      setNoteText("");
      setEditingId(null);
    } catch (err) {
      console.error("Error submitting note:", err);
    }
  };

  // Delete
  const handleDelete = async (id) => {
    try {
      await axios.delete(API + id);
      setNotes(notes.filter((n) => n.id !== id));
      if (editingId === id) {
        setEditingId(null);
        setName("");
        setNoteText("");
      }
    } catch (err) {
      console.error("Error deleting note:", err);
    }
  };

  // Edit
  const handleEdit = (note) => {
    setEditingId(note.id);
    setName(note.name);
    setNoteText(note.node); // Note the key is "node" from backend
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "1rem" }}>
      <h1>📝 Notes</h1>

      {/* Form */}
      <form onSubmit={handleSubmit} style={{ marginBottom: "1.5rem" }}>
        <h3>{editingId ? "Edit Note" : "Create Note"}</h3>
        <input
          type="text"
          placeholder="Note name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ width: "100%", padding: "0.5rem", marginBottom: "0.5rem" }}
        />
        <textarea
          placeholder="Note text"
          value={noteText}
          onChange={(e) => setNoteText(e.target.value)}
          required
          rows={4}
          style={{ width: "100%", padding: "0.5rem", marginBottom: "0.5rem" }}
        />
        <button type="submit" style={{ padding: "0.5rem 1rem" }}>
          {editingId ? "Update" : "Create"}
        </button>
      </form>

      {/* Notes List */}
      {notes.length === 0 ? (
        <p>No notes yet.</p>
      ) : (
        notes.map((note) => (
          <div
            key={note.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: "4px",
              padding: "0.75rem",
              marginBottom: "1rem",
            }}
          >
            <h4>{note.name}</h4>
            <p>{note.node}</p>
            <button onClick={() => handleEdit(note)} style={{ marginRight: "0.5rem" }}>
              Edit
            </button>
            <button onClick={() => handleDelete(note.id)}>Delete</button>
          </div>
        ))
      )}
    </div>
  );
}
