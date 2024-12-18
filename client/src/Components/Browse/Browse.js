import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft, FaArrowRight, FaSync } from "react-icons/fa";
import FilterPopup from "../FilterPopup/FilterPopup";
import "./Browse.css";

const Browse = () => {
  const navigate = useNavigate();
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [currentFilters, setCurrentFilters] = useState({
    subject: '',
    day: '',
    credits: ''
  });

  const mockCourses = [
    { id: 1, name: "Intro to CS", credits: 3, professor: "John Doe", schedule: "Mon 9:00 AM - 10:15 AM", subject: "Computer Science", day: "Monday", seats: 30 },
    { id: 2, name: "Data Structures", credits: 4, professor: "Jane Smith", schedule: "Tue 10:30 AM - 11:45 AM", subject: "Computer Science", day: "Tuesday", seats: 25 },
    { id: 3, name: "Algorithms", credits: 3, professor: "Emily White", schedule: "Wed 12:00 PM - 1:15 PM", subject: "Computer Science", day: "Wednesday", seats: 35 },
    { id: 4, name: "Calculus I", credits: 3, professor: "Michael Brown", schedule: "Thu 1:30 PM - 2:45 PM", subject: "Mathematics", day: "Thursday", seats: 20 },
    { id: 5, name: "Linear Algebra", credits: 4, professor: "Sarah Taylor", schedule: "Fri 3:00 PM - 4:15 PM", subject: "Mathematics", day: "Friday", seats: 25 },
    { id: 6, name: "Discrete Math", credits: 3, professor: "David Lee", schedule: "Mon 4:30 PM - 5:45 PM", subject: "Mathematics", day: "Monday", seats: 30 },
    { id: 7, name: "Mechanics", credits: 3, professor: "Alice Wilson", schedule: "Tue 9:00 AM - 10:15 AM", subject: "Physics", day: "Tuesday", seats: 30 },
    { id: 8, name: "Electromagnetism", credits: 4, professor: "Robert Harris", schedule: "Wed 10:30 AM - 11:45 AM", subject: "Physics", day: "Wednesday", seats: 25 },
    { id: 9, name: "Quantum Mechanics", credits: 3, professor: "John Doe", schedule: "Thu 12:00 PM - 1:15 PM", subject: "Physics", day: "Thursday", seats: 20 },
    { id: 10, name: "Computer Organization", credits: 3, professor: "Jane Smith", schedule: "Fri 1:30 PM - 2:45 PM", subject: "Computer Science", day: "Friday", seats: 30 },
    { id: 11, name: "Operating Systems", credits: 3, professor: "Emily White", schedule: "Mon 3:00 PM - 4:15 PM", subject: "Computer Science", day: "Monday", seats: 25 },
    { id: 12, name: "Calculus II", credits: 3, professor: "Michael Brown", schedule: "Tue 4:30 PM - 5:45 PM", subject: "Mathematics", day: "Tuesday", seats: 20 },
    { id: 13, name: "Differential Equations", credits: 4, professor: "Sarah Taylor", schedule: "Wed 9:00 AM - 10:15 AM", subject: "Mathematics", day: "Wednesday", seats: 25 },
    { id: 14, name: "Thermodynamics", credits: 3, professor: "David Lee", schedule: "Thu 10:30 AM - 11:45 AM", subject: "Physics", day: "Thursday", seats: 30 },
    { id: 15, name: "Astrophysics", credits: 4, professor: "Alice Wilson", schedule: "Fri 12:00 PM - 1:15 PM", subject: "Physics", day: "Friday", seats: 25 }
  ];
  

  const handleFilterToggle = () => {
    setShowPopup(prevState => !prevState);  // Toggle popup visibility
  };

  const handleApplyFilters = (filters) => {
    setCurrentFilters(filters);
    
    // Filter the courses based on the current filters
    const filtered = mockCourses.filter(course => {
      return (
        (filters.subject ? course.subject === filters.subject : true) &&
        (filters.day ? course.day === filters.day : true) &&
        (filters.credits ? course.credits === parseInt(filters.credits) : true)
      );
    });
  
    if (filtered.length === 0) {
      window.alert('No courses match your filter criteria.');
    }
  
    setFilteredCourses(filtered);
    setShowPopup(false); 
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  const handleCourseSelect = (course) => {
    setSelectedCourse(course);
  };

  const handleRefresh = () => {
    setSelectedCourse(null); // Reset selected course
    setFilteredCourses([]);  // Clear the filtered courses
    setCurrentFilters({ subject: '', day: '', credits: '' }); // Reset filters
  };

  return (
    <>
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
            <p className="filter-text" onClick={handleFilterToggle}>Filter</p>

            <h3>Available Courses
              <button className="refresh-button" onClick={handleRefresh}>
                <FaSync /> Refresh
              </button>
            </h3>
            <p> <i>Select a course to view class details!</i> </p>

            {/* Course Cards */}
            <div className="main-courses">
              {selectedCourse ? (
                <div className="browse-course-card">
                  <h3>{selectedCourse.name}</h3>
                  <p><b>Professor:</b> {selectedCourse.professor}</p>
                  <p><b>Schedule:</b> {selectedCourse.schedule}</p>
                  <p><b>Credits:</b> {selectedCourse.credits}</p>
                  <p><b>Subject:</b> {selectedCourse.subject}</p>
                  <p><b>Seats Available:</b> {selectedCourse.seats}</p>
                </div>
              ) : (
                (filteredCourses.length > 0 ? filteredCourses : mockCourses).map((course) => (
                  <div
                    key={course.id}
                    className="browse-course-card"
                    onClick={() => handleCourseSelect(course)}
                  >
                    <h3>{course.name}</h3>
                    <p>{course.professor}</p>
                    <p>{course.schedule}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      <FilterPopup
        show={showPopup}
        onClose={closePopup}
        onApply={handleApplyFilters}
        currentFilters={currentFilters}
      />
    </>
  );
};

export default Browse;
