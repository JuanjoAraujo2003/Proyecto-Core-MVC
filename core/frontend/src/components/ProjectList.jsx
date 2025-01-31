import React, { useEffect, useState } from "react";
import axios from "axios";

const ProjectList = ({ setSelectedProject }) => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/projects/")
      .then((response) => setProjects(response.data))
      .catch((error) => console.error("Error fetching projects:", error));
  }, []);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-white mb-6 text-center">Gestión de Proyectos</h1>
      <h2 className="text-2xl font-semibold text-gray-300 mb-4">Lista de Proyectos</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {projects.map((project) => (
          <div
            key={project.id}
            onClick={() => setSelectedProject(project.id)}
            className="cursor-pointer bg-gray-800 p-4 rounded-lg shadow-md hover:bg-gray-700 transition-all duration-300"
          >
            <h3 className="text-xl font-bold text-white">{project.name}</h3>
            <p className="text-gray-400">{project.description}</p>
            <p className="text-sm text-gray-500 mt-2">
              <span className="font-semibold">Prioridad:</span> {project.priority}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProjectList;
