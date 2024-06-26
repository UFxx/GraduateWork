import React, { useEffect, useState } from "react";
import Discipline from "./Discipline/Discipline";
import axios from "axios";

function Filter(props) {
  const inputs = document.querySelectorAll(".discipline input");
  const ratings = document.querySelectorAll(".rating");

  const [isOpen, toggleOpen] = useState(true);
  const disciplines = [];

  function toggleFilters() {
    toggleOpen(!isOpen);
  }

  function clearFilters() {
    inputs.forEach((input) => (input.checked = false));
    ratings.forEach((rating) => {
      rating.style.opacity = 100;
      rating.style.display = "flex";
    });
  }

  const subjectsEndpoint = `http://127.0.0.1:8000/api-student_performance/scores/${props.userSlug}/`;
  useEffect(() => {
    axios
      .get(subjectsEndpoint)
      .then((data) => props.setSubject(data.data.subjects));
      
      // eslint-disable-next-line
  }, [props.subject, subjectsEndpoint]);

  for (let i = 0; i < props.subjects.length; i++) {
    disciplines.push(
      <Discipline disciplineName={props.subjects[i].subject} id={i} key={i} />
    );
  }

  return (
    <>
      <div className="subject-filter" onClick={toggleFilters}>
        <i className="fas fa-filter"></i>
      </div>
      <div
        className={
          isOpen
            ? "filters-container__unactive"
            : "filters-container__active"
        }
      >
        <div>
          <i className="fas fa-times" onClick={toggleFilters}></i>
          <p className="filters-title">Фильтры</p>
        </div>
        <div className="filters-content">
          <p className="filters-content-title">Выберите дисциплину:</p>
          <div className="disciplines">{disciplines}</div>
          <button className="clear-filter" onClick={clearFilters}>
            Сбросить фильтр
          </button>
        </div>
      </div>
    </>
  );
}

export default Filter;
