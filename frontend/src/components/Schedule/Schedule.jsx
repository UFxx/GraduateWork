import React, { useState, useEffect } from "react";
import axios from "axios";
import DailySchedule from "./DailySchedule/DailySchedule";
import DoublePair from "./DoublePair/DoublePair";
import Pair from "./Pair/Pair";

function Schedule(props) {
  const [pairs, setPairs] = useState("");
  const mondayPairs = [];
  const tuesdayPairs = [];
  const wednesdayPairs = [];
  const thursdayPairs = [];
  const fridayPairs = [];
  const saturdayPairs = [];

  // Tommorow's schedule
  const daysOfWeek = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
  ];

  const tommorowDay = daysOfWeek[new Date().getDay()];

  function pairsMatchingOnThisDay() {
    switch (tommorowDay) {
      case daysOfWeek[0]:
        return mondayPairs;
      case daysOfWeek[1]:
        return tuesdayPairs;
      case daysOfWeek[2]:
        return wednesdayPairs;
      case daysOfWeek[3]:
        return thursdayPairs;
      case daysOfWeek[4]:
        return fridayPairs;
      case daysOfWeek[5]:
        return saturdayPairs;
      default:
        return (
          <Pair subjectName="Пар нет, уходите!" pairNumber="0" audience="0" />
        );
    }
  }

  // Weekly schedule
  const scheduleEndpoint = `http://127.0.0.1:8000/api-timetable/timetable/${props.groupSlug}/`;
  useEffect(() => {
    axios.get(scheduleEndpoint).then((data) => setPairs(data.data.timetable));
  }, [scheduleEndpoint]);

  console.log(pairs);

  for (let i = 0; i < pairs.length; i++) {
    pairs[i].lecturer.user = pairs[i].lecturer.user
      .replace("-", " ")
      .replace("_", " ");
    let pair = "";

    if (
      pairs[i].evenness === "четная" &&
      pairs[i + 1].evenness === "нечетная"
    ) {
      pair = (
        <DoublePair
          pairNumber={pairs[i].lesson_number}
          subjectName={pairs[i].subject}
          teacherName={pairs[i].lecturer.user}
          audience={pairs[i].classroom}
          time={`${pairs[i].start_time} - ${pairs[i].end_time}`}
          secondSubjectName={pairs[i + 1].subject}
          secondTeacherName={pairs[i + 1].lecturer.user}
          secondAudience={pairs[i + 1].classroom}
          key={pairs[i].id}
        />
      );
    } else {
      pair = (
        <Pair
          pairNumber={pairs[i].lesson_number}
          subjectName={pairs[i].subject}
          teacherName={pairs[i].lecturer.user}
          audience={pairs[i].classroom}
          time={`${pairs[i].start_time} - ${pairs[i].end_time}`}
          key={pairs[i].id}
        />
      );
    }
    switch (pairs[i].day_of_the_week) {
      case daysOfWeek[0].toLowerCase():
        mondayPairs.push(pair);
        break;
      case daysOfWeek[1].toLowerCase():
        tuesdayPairs.push(pair);
        break;
      case daysOfWeek[2].toLowerCase():
        wednesdayPairs.push(pair);
        break;
      case daysOfWeek[3].toLowerCase():
        thursdayPairs.push(pair);
        break;
      case daysOfWeek[4].toLowerCase():
        fridayPairs.push(pair);
        break;
      case daysOfWeek[5].toLowerCase():
        saturdayPairs.push(pair);
        break;
      default:
        return;
    }
  }

  return (
    <>
      <div className="daily-schedule schedule-content">
        <p>Расписание на завтра</p>
        <table className="daily-schedule">
          <tbody>
            <DailySchedule day={tommorowDay} pairs={pairsMatchingOnThisDay()} />
          </tbody>
        </table>
      </div>

      <div className="schedule-content">
        <p>Расписание на неделю</p>
        <table className="daily-schedule">
          <tbody>
            <DailySchedule day="Понедельник" pairs={mondayPairs} />
            <DailySchedule day="Вторник" pairs={tuesdayPairs} />
            <DailySchedule day="Среда" pairs={wednesdayPairs} />
            <DailySchedule day="Четверг" pairs={thursdayPairs} />
            <DailySchedule day="Пятница" pairs={fridayPairs} />
            <DailySchedule day="Суббота" pairs={saturdayPairs} />
          </tbody>
        </table>
      </div>
    </>
  );
}

export default Schedule;
