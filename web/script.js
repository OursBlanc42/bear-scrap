document.addEventListener("DOMContentLoaded", loadProjects);

async function loadProjects() {
  const projectsGrid = document.getElementById("projectsGrid");

  try {
    // Charger les données du CSV
    const response = await fetch("../data/list.csv");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const csvText = await response.text();
    const projects = parseCSV(csvText);

    // Afficher les projets
    projectsGrid.innerHTML = projects
      .map(
        (project) => `
        <tr>
          <td class="day-cell">Jour ${project.day}</td>
          <td class="title-cell">${project.title}</td>
          <td class="description-cell">${project.description}</td>
          <td class="links-cell">
            ${
              project.link1 &&
              project.link1 !== "none" &&
              project.link1 !== "null"
                ? `<a href="${project.link1}" target="_blank">Projet</a>`
                : ""
            }
            ${
              project.link2 &&
              project.link2 !== "none" &&
              project.link2 !== "null"
                ? `<a href="${project.link2}" target="_blank">En savoir plus</a>`
                : ""
            }
            ${
              project.link3 &&
              project.link3 !== "none" &&
              project.link3 !== "null"
                ? `<a href="${project.link3}" target="_blank">Soutenir</a>`
                : ""
            }
          </td>
        </tr>
      `
      )
      .join("");

    // Mettre à jour les statistiques
    updateStats(projects);
  } catch (error) {
    console.error("Erreur lors du chargement des données:", error);
    projectsGrid.innerHTML =
      "<tr><td colspan='4'>Erreur de chargement des données.</td></tr>";
  }
}

// To avoid problem with quotes and comma in descriptions, we use a simple CSV parser
// The first two columns, then lasts columns, and the description is everything in between
function parseCSV(csvText) {
  const lines = csvText.trim().split("\n");
  return (
    lines
      .map((line) => {
        // Simple parsing
        const parts = line.split(",");
        if (parts.length < 5) return null; // At least 5 columns are required (day, title, description, 3 links)

        const day = parts[0].trim();
        const title = parts[1].trim();

        // Last columns are links
        const link1 = parts[parts.length - 3].trim();
        const link2 = parts[parts.length - 2].trim();
        const link3 = parts[parts.length - 1].trim();

        // Description is everything in between the first two columns and the last three
        const description = parts
          .slice(2, -3)
          .join(",")
          .trim()
          .replace(/^"|"$/g, "");

        return { day, title, description, link1, link2, link3 };
      })
      // remove empty lines
      .filter((project) => project && project.day && project.title)
      .sort((a, b) => parseInt(b.day) - parseInt(a.day))
  );
}

function updateStats(projects) {
  const totalProjects = projects.length;

  // Update the number of projects
  document.getElementById("totalProjects").textContent = totalProjects;

  // Mettre à jour la date de dernière mise à jour depuis le fichier
  loadLastUpdateDate();
}

async function loadLastUpdateDate() {
  try {
    const response = await fetch("../data/last_update.txt");
    if (response.ok) {
      const lastUpdateText = await response.text();
      document.getElementById("lastUpdate").textContent = lastUpdateText.trim();
    } else {
      document.getElementById("lastUpdate").textContent =
        "Données non disponibles";
    }
  } catch (error) {
    console.error(
      "Erreur lors du chargement de la date de mise à jour:",
      error
    );
    document.getElementById("lastUpdate").textContent = "Erreur de chargement";
  }
}
