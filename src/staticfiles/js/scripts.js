document.addEventListener("DOMContentLoaded", function () {
  // Menu Toggle pour version mobile
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector("nav ul");

  if (menuToggle) {
    menuToggle.addEventListener("click", () => {
      navLinks.classList.toggle("active");
    });
  }

  // Fonction de validation pour le formulaire de création de compte
  const formCreateMedecin = document.querySelector("#form-create-medecin");
  if (formCreateMedecin) {
    formCreateMedecin.addEventListener("submit", function (e) {
      e.preventDefault(); // Empêche le formulaire de se soumettre avant validation

      const username = document.querySelector("#username").value;
      const email = document.querySelector("#email").value;
      const password = document.querySelector("#password").value;

      if (username === "" || email === "" || password === "") {
        alert("Tous les champs doivent être remplis");
        return;
      }

      // Si la validation est réussie, vous pouvez envoyer le formulaire ici
      this.submit();
    });
  }

  // Recherche en temps réel pour la page des enregistrements
  const searchInput = document.querySelector("#search-input");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const query = this.value.toLowerCase();
      const rows = document.querySelectorAll("table tbody tr");
      rows.forEach((row) => {
        const cells = row.getElementsByTagName("td");
        let matchFound = false;
        for (let i = 0; i < cells.length; i++) {
          if (cells[i].innerText.toLowerCase().includes(query)) {
            matchFound = true;
          }
        }
        row.style.display = matchFound ? "" : "none";
      });
    });
  }

  // Fonction de confirmation avant suppression d'un enregistrement
  const deleteButtons = document.querySelectorAll(".delete-btn");
  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      if (!confirm("Êtes-vous sûr de vouloir supprimer cet enregistrement ?")) {
        e.preventDefault(); // Annule l'action si l'utilisateur refuse
      }
    });
  });
});
