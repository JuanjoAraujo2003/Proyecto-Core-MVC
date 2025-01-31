import React, { useState } from "react";
import ProjectList from "./components/ProjectList";
import TaskList from "./components/TaskList";

const App = () => {
  const [selectedProject, setSelectedProject] = useState(null);

  return (
    <div className="bg-gray-900 min-h-screen p-10">
      <div className="container mx-auto">
        <ProjectList setSelectedProject={setSelectedProject} />
        {selectedProject && <TaskList projectId={selectedProject} />}
      </div>
    </div>
  );
};

export default App;
