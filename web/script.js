// Script pour charger et afficher les données des projets
document.addEventListener("DOMContentLoaded", function () {
  loadProjects();
});

async function loadProjects() {
  const projectsGrid = document.getElementById("projectsGrid");
  const totalProjectsElement = document.getElementById("totalProjects");
  const totalLinksElement = document.getElementById("totalLinks");
  const lastUpdateElement = document.getElementById("lastUpdate");

  try {
    // Afficher l'état de chargement
    projectsGrid.innerHTML =
      '<div class="loading">Chargement des projets...</div>';

    // Charger les données du CSV
    const response = await fetch("../list.csv");
    const csvText = await response.text();

    // Parser le CSV
    const projects = parseCSV(csvText);

    if (projects.length === 0) {
      projectsGrid.innerHTML = `
                <div class="empty-state">
                    <h3>Aucun projet trouvé</h3>
                    <p>Lancez le script de scraping pour découvrir les projets !</p>
                </div>
            `;
      return;
    }

    // Afficher les projets
    displayProjects(projects);

    // Mettre à jour les statistiques
    updateStats(
      projects,
      totalProjectsElement,
      totalLinksElement,
      lastUpdateElement
    );
  } catch (error) {
    console.error("Erreur lors du chargement des données:", error);
    projectsGrid.innerHTML = `
            <div class="empty-state">
                <h3>Erreur de chargement</h3>
                <p>Impossible de charger les données. Vérifiez que le fichier CSV existe.</p>
            </div>
        `;
  }
}

function parseCSV(csvText) {
  const lines = csvText.trim().split("\n");
  const projects = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    // Parser la ligne CSV (gestion basique des guillemets)
    const columns = parseCSVLine(line);

    if (columns.length >= 5) {
      projects.push({
        day: columns[0],
        title: columns[1],
        linksProject: columns[2],
        linksMore: columns[3],
        linksSupport: columns[4],
      });
    }
  }

  // Trier par jour (numérique)
  projects.sort((a, b) => parseInt(b.day) - parseInt(a.day));

  return projects;
}

function parseCSVLine(line) {
  const columns = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"' && (i === 0 || line[i - 1] === ",")) {
      inQuotes = true;
    } else if (
      char === '"' &&
      inQuotes &&
      (i === line.length - 1 || line[i + 1] === ",")
    ) {
      inQuotes = false;
    } else if (char === "," && !inQuotes) {
      columns.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }

  columns.push(current.trim());
  return columns;
}

function displayProjects(projects) {
  const projectsGrid = document.getElementById("projectsGrid");

  projectsGrid.innerHTML = projects
    .map(
      (project) => `
        <div class="project-card">
            <div class="project-header">
                <span class="project-day">Jour ${project.day}</span>
                <h3 class="project-title">${escapeHtml(project.title)}</h3>
            </div>
            <div class="project-links">
                ${
                  project.linksProject
                    ? `<a href="${project.linksProject}" class="project-link" target="_blank" rel="noopener">Projet</a>`
                    : ""
                }
                ${
                  project.linksMore
                    ? `<a href="${project.linksMore}" class="project-link more-link" target="_blank" rel="noopener">En savoir plus</a>`
                    : ""
                }
                ${
                  project.linksSupport
                    ? `<a href="${project.linksSupport}" class="project-link support-link" target="_blank" rel="noopener">Soutenir</a>`
                    : ""
                }
            </div>
        </div>
    `
    )
    .join("");
}

function updateStats(
  projects,
  totalProjectsElement,
  totalLinksElement,
  lastUpdateElement
) {
  // Compter le nombre total de projets
  totalProjectsElement.textContent = projects.length;

  // Compter le nombre total de liens
  let totalLinks = 0;
  projects.forEach((project) => {
    if (project.linksProject) totalLinks++;
    if (project.linksMore) totalLinks++;
    if (project.linksSupport) totalLinks++;
  });
  totalLinksElement.textContent = totalLinks;

  // Afficher la date de dernière mise à jour
  const now = new Date();
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  lastUpdateElement.textContent = now.toLocaleDateString("fr-FR", options);
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Fonction pour rafraîchir les données
function refreshData() {
  loadProjects();
}
