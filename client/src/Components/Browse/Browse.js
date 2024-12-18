import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";
import "./Browse.css";

const Browse = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);

  const mockCourses = [
    { id: 1, name: "Intro to CS", credits: 3, professor: "John Doe", schedule: "Mon 9:00 AM - 10:15 AM" },
    { id: 2, name: "Data Structures", credits: 4, professor: "Jane Smith", schedule: "Tue 10:30 AM - 11:45 AM" },
    { id: 3, name: "Algorithms", credits: 3, professor: "Emily White", schedule: "Wed 12:00 PM - 1:15 PM" },
    { id: 4, name: "Calculus I", credits: 3, professor: "Michael Brown", schedule: "Thu 1:30 PM - 2:45 PM" },
    { id: 5, name: "Linear Algebra", credits: 4, professor: "Sarah Taylor", schedule: "Fri 3:00 PM - 4:15 PM" },
    { id: 6, name: "Discrete Math", credits: 3, professor: "David Lee", schedule: "Mon 4:30 PM - 5:45 PM" },
    { id: 7, name: "Mechanics", credits: 3, professor: "Alice Wilson", schedule: "Tue 9:00 AM - 10:15 AM" },
    { id: 8, name: "Electromagnetism", credits: 4, professor: "Robert Harris", schedule: "Wed 10:30 AM - 11:45 AM" },
    { id: 9, name: "Quantum Mechanics", credits: 3, professor: "John Doe", schedule: "Thu 12:00 PM - 1:15 PM" },
    { id: 10, name: "Computer Organization", credits: 3, professor: "Jane Smith", schedule: "Fri 1:30 PM - 2:45 PM" },
    { id: 11, name: "Operating Systems", credits: 3, professor: "Emily White", schedule: "Mon 3:00 PM - 4:15 PM" },
    { id: 12, name: "Calculus II", credits: 3, professor: "Michael Brown", schedule: "Tue 4:30 PM - 5:45 PM" },
    { id: 13, name: "Differential Equations", credits: 4, professor: "Sarah Taylor", schedule: "Wed 9:00 AM - 10:15 AM" },
    { id: 14, name: "Thermodynamics", credits: 3, professor: "David Lee", schedule: "Thu 10:30 AM - 11:45 AM" },
    { id: 15, name: "Astrophysics", credits: 4, professor: "Alice Wilson", schedule: "Fri 12:00 PM - 1:15 PM" }
  ];

  const handleInputChange = (e) => {
    const input = e.target.value;
    setSearchTerm(input);

    if (input.trim() === "") {
      setFilteredCourses([]);
      return;
    }

    const results = mockCourses.filter((course) =>
      course.name.toLowerCase().includes(input.toLowerCase())
    );
    setFilteredCourses(results);
  };

  const handleCourseSelect = (course) => {
    setSelectedCourse(course);
    setSearchTerm("");
    setFilteredCourses([]);
  };

  return (
    <div className="browse-page">
      {/* Header */}
      <header className="browse-header">
        <button className="browse-back-button" onClick={() => navigate('/homepage')}>
          <FaArrowLeft /> Back to Homepage
        </button>
        <h1>Browse Courses</h1>
        <button className="fwd-button" onClick={() => navigate('/schedule_build')}>
          <FaArrowRight /> View Schedule
        </button>
      </header>

      {/* Main Container */}
      <div className="browse-container">
        <div className="search-section">
          <input
            type="text"
            className="search-bar"
            placeholder="Search for courses..."
            value={searchTerm}
            onChange={handleInputChange}
          />

          <h3>Available Courses</h3>
          <p> <i>Enter course name above for more details!</i> </p>
          {!selectedCourse && (
            <div className="main-courses">
              {mockCourses.slice(0, 16).map((course) => (
                <div key={course.id} className="browse-course-card">
                  <h3>{course.name}</h3>
                  <p>{course.professor}</p>
                  <p>{course.schedule}</p>
                </div>
              ))}
            </div>
          )}

          {/* Dropdown */}
          {filteredCourses.length > 0 && (
            <ul className="dropdown">
              {filteredCourses.map((course) => (
                <li
                  key={course.id}
                  className="dropdown-item"
                  onClick={() => handleCourseSelect(course)}
                >
                  {course.name}
                </li>
              ))}
            </ul>
          )}

          {filteredCourses.length === 0 && searchTerm.trim() !== "" && (
            <ul className="dropdown">
              <li className="dropdown-item no-match">No matching courses found</li>
            </ul>
          )}
        </div>

        {/* Course Details */}
        {selectedCourse && (
          <div className="course-details">
            <h2>Course Details</h2>
            <p><strong>Course Name:</strong> {selectedCourse.name}</p>
            <p><strong>Credits:</strong> {selectedCourse.credits}</p>
            <p><strong>Professor:</strong> {selectedCourse.professor}</p>
            <p><strong>Schedule:</strong> {selectedCourse.schedule}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Browse;
