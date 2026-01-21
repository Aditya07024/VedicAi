import { useState } from "react";
import api from "../services/api";
import "./BirthForm.css";

function BirthForm({ onSubmit, loading, error }) {
  const [formData, setFormData] = useState({
    name: "",
    date: "2003-02-07",
    time: "03:00",
    place: "",
    latitude: 27.7081,
    longitude: 77.9367,
  });

  const [searchResults, setSearchResults] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "latitude" || name === "longitude" ? parseFloat(value) : value,
    }));
  };

  const handleSearch = async () => {
    if (!formData.place) return;
    try {
      const response = await api.get("/api/search-place", {
        params: { query: formData.place },
      });
      setSearchResults(response.data);
    } catch (err) {
      console.error("Search error:", err);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.name || !formData.place) {
      alert("Please fill all required fields");
      return;
    }

    if (formData.latitude === 0 || formData.longitude === 0) {
      alert("Please enter valid latitude and longitude");
      return;
    }

    onSubmit({
      name: formData.name,
      date: formData.date,
      time: formData.time.replace(":", ":") + ":00",
      place: formData.place,
      latitude: formData.latitude,
      longitude: formData.longitude,
    });
  };

  return (
    <div className="form-container">
      <h2>📅 Birth Details</h2>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your name"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Birth Date</label>
            <input
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Birth Time</label>
            <input
              type="time"
              name="time"
              value={formData.time}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-group">
          <label>Place Name *</label>
          <div className="search-group">
            <input
              type="text"
              name="place"
              value={formData.place}
              onChange={handleChange}
              placeholder="Enter your birth place"
              required
            />
            <button type="button" onClick={handleSearch} className="search-btn">
              🔍 Search
            </button>
          </div>
          {searchResults && (
            <div className="search-result">
              <a
                href={searchResults.search_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                👉 Search "{formData.place}" on Google
              </a>
            </div>
          )}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Latitude *</label>
            <input
              type="number"
              name="latitude"
              value={formData.latitude}
              onChange={handleChange}
              step="0.0001"
              required
            />
          </div>

          <div className="form-group">
            <label>Longitude *</label>
            <input
              type="number"
              name="longitude"
              value={formData.longitude}
              onChange={handleChange}
              step="0.0001"
              required
            />
          </div>
        </div>

        <button type="submit" className="primary submit-btn" disabled={loading}>
          {loading ? "⏳ Analyzing..." : "🔮 Generate Analysis"}
        </button>
      </form>
    </div>
  );
}

export default BirthForm;
