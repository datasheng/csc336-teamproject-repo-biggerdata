import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft, FaShoppingCart } from "react-icons/fa";
import "./Schedule.css";

const Schedule = () => {
  const navigate = useNavigate();
  const [schedule, setSchedule] = useState([]);
  const [cart, setCart] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

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

  const addToSchedule = (course) => {
    const conflict = schedule.find((c) => c.schedule === course.schedule);
    if (conflict) {
      window.alert(`Schedule conflict with: ${conflict.name}`);
      return;
    }
    setSchedule([...schedule, course]);
  };

  const removeFromSchedule = (courseId) => {
    setSchedule(schedule.filter((course) => course.id !== courseId));
  };

  const addToCart = (course) => {
    setCart([...cart, course]);
  };

  const removeFromCart = (course) => {
    setCart(cart.filter((item) => item.id !== course.id));
  };
  

  const filteredCourses = mockCourses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const renderCalendar = () => {
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
    const times = [
      "8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM",
      "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", 
      "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM"
    ];

    return (
      <div className="calendar">
        <div className="calendar-header">
          <div className="time-column-header"></div>
          {days.map((day) => (
            <div key={day} className="calendar-day-header">{day}</div>
          ))}
        </div>
        <div className="calendar-grid">
          {times.map((time) => (
            <div key={time} className="calendar-time-row">
              <div className="time-column">{time}</div>
              {days.map((day) => {
                const coursesAtTime = schedule.filter(
                  (c) => c.schedule.includes(day) && c.schedule.includes(time)
                );
                return (
                  <div key={day + time} className="calendar-cell">
                    {coursesAtTime.length > 0 && (
                      <div className="course-list">
                        {coursesAtTime.map((course) => (
                          <div key={course.id} className="calendar-course">
                            {course.name} ({course.schedule})
                            <button
                              onClick={() => removeFromSchedule(course.id)}
                              className="remove-button"
                            >
                              Remove
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="schedule-container">
        <button className="sched-back-button" onClick={() => navigate("/user-homepage")}>
          <FaArrowLeft /> Back to Homepage
        </button>

      <div className="schedule-content">
        <div className="search-and-details">
          <input
            type="text"
            placeholder="Search for classes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-bar"
          />
          <div className="course-list">
            {filteredCourses.map((course) => (
              <div key={course.id} className="course-card">
                <h3>{course.name}</h3>
                <p><strong>Credits:</strong> {course.credits}</p>
                <p><strong>Professor:</strong> {course.professor}</p>
                <p><strong>Schedule:</strong> {course.schedule}</p>
                <div className="card-buttons">
                  <button onClick={() => addToCart(course)}>Add to Cart</button>
                  <button onClick={() => addToSchedule(course)}>Add to Schedule</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="calendar-section">
          <h2>Your Schedule</h2>
          {renderCalendar()}
        </div>

        <div className="cart-section">
  <h2>Cart <FaShoppingCart /> </h2>
  <ul>
    {cart.map((course) => (
      <li key={course.id}>
        {course.name}
        <button onClick={() => removeFromCart(course)} className="remove-button">
          Remove
        </button>
      </li>
    ))}
  </ul>
</div>

      </div>
    </div>
  );
};

export default Schedule;
