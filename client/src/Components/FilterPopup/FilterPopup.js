import React, { useState, useEffect } from 'react';
import './FilterPopup.css';

const FilterPopup = ({ show, onClose, onApply, currentFilters }) => {
  const [subject, setSubject] = useState(currentFilters.subject);
  const [day, setDay] = useState(currentFilters.day);

  useEffect(() => {
    setSubject(currentFilters.subject);
    setDay(currentFilters.day);
  }, [currentFilters]);

  const handleClose = () => {
    onClose();
  }

  const handleApply = () => {
    onApply({ subject, day });
  }

  return (
    show && (
      <div className="popup">
        <div className="popup-content">
          <h2>Filter</h2>

          <label>
            Subject:
            <select value={subject} onChange={(e) => setSubject(e.target.value)}>
              <option value="">Any Subject</option>
              <option value="CompSci">Computer Science</option>
              <option value="Math">Mathematics</option>
              <option value="Phy">Physics</option>
            </select>
          </label>

          <label>
            Day:
            <select value={day} onChange={(e) => setDay(e.target.value)}>
              <option value="">Any Day</option>
              <option value="Monday">Monday</option>
              <option value="Tuesday">Tuesday</option>
              <option value="Wednesday">Wednesday</option>
              <option value="Thursday">Thursday</option>
              <option value="Friday">Friday</option>
            </select>
          </label>

          <div className="buttons">
            <button onClick={handleApply} className="apply-bttn">Apply</button>
            <button onClick={handleClose} className="close-bttn">Close</button>
          </div>
        </div>
      </div>
    )
  );
};

export default FilterPopup;
