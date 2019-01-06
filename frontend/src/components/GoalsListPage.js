import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import GoalsList from "./GoalsList";
import "../css/application.scss";


const GoalsListPage = () => (
  <DataProvider endpoint="/api/goal/"
                render={data => <GoalsList data={data}/>}/>
);

const wrapper = document.getElementById("goals_list");

wrapper ? ReactDOM.render(<GoalsListPage/>, wrapper) : null;
