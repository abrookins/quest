import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import GoalDetail from "./GoalDetail";
import TaskModel from "./TaskModel";
import "../css/application.scss";
import "../css/tasks.scss";

let model = new TaskModel('tasks');

const GoalDetailPage = (props) => (
  <DataProvider endpoint={`/api/goal/${props.goalId}`}
                render={data => <GoalDetail goal={data} model={model}/>}/>
);

const wrapper = document.getElementById("goal");
const goalId = document.getElementById("goal-id").dataset.id;

function render() {
  console.log(wrapper);
  wrapper ? ReactDOM.render(<GoalDetailPage goalId={goalId}/>, wrapper) : null;
}

model.subscribe(render);
render();
