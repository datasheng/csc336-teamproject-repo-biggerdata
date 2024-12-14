import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import FilterPopup from "../FilterPopup/FilterPopup";
import './Browse.css'; // Import the new CSS for styling

const Browse = () => {
  const [filterActive, setFilterActive] = useState(false);
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    subject: '',
    day: '',
  });

  const handleFilterPopup = () => {
    setFilterActive(true);
  }

  const closePopup = () => {
    setFilterActive(false);
  }

  const handleApplyFilters = (newFilters) => {
    setFilters(newFilters);
    setFilterActive(false);
  }


  return (
    <>
      <header className="browse-header">
        <button className="back-button" onClick={() => navigate('/user-homepage')}>
          <FaArrowLeft /> Back
        </button>
        <h1>Browse Courses</h1>
      </header>

      <div className="browse-courses">
        {/* Search Bar */}
        <input
          type="text"
          placeholder="Search for courses"
          className="search-bar"
        />

        {/* Filter Button */}
        <p2 onClick={handleFilterPopup}>Filter</p2>
      </div>

      <FilterPopup
        show={filterActive}
        onClose={closePopup}
        onApply={handleApplyFilters}
        currentFilters={filters}
      />
    </>
  );
};

export default Browse;
