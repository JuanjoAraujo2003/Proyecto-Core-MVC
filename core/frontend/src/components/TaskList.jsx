import React, { useEffect, useState } from "react";
import axios from "axios";

const TaskList = ({ projectId }) => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/api/tasks/?project=${projectId}`)
      .then((response) => setTasks(response.data))
      .catch((error) => console.error("Error fetching tasks:", error));
  }, [projectId]);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold text-gray-300 mb-4">Tareas del Proyecto</h2>

      {tasks.length === 0 ? (
        <p className="text-gray-400">No hay tareas asignadas a este proyecto.</p>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <div key={task.id} className="bg-gray-800 p-4 rounded-lg shadow-md">
              <h3 className="text-lg font-bold text-white">{task.title}</h3>
              <p className="text-gray-400">{task.description}</p>
              <p className="text-sm text-gray-500 mt-2">
                <span className="font-semibold">Estado:</span> {task.status}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;
