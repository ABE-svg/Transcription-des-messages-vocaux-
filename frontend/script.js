// ===============================
// Configuration
// ===============================

const API_BASE = "";
const ENDPOINT = "/whisper";

// Récupération des éléments du DOM
const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const summaryToggle = document.getElementById("summaryToggle");
const submitBtn = document.getElementById("submitBtn");
const progress = document.getElementById("progress");
const errorBox = document.getElementById("errorBox");
const infoBox = document.getElementById("infoBox");
const transcriptEl = document.getElementById("transcript");
const summaryEl = document.getElementById("summary");

// ===============================
// Utils d'affichage
// ===============================
function setText(el, text) {
  el.textContent = text ?? "";
}

function show(el) {
  el.style.display = "block";
}

function hide(el) {
  el.style.display = "none";
}

function resetOutputs() {
  hide(errorBox);
  hide(infoBox);
  setText(transcriptEl, "");
  setText(summaryEl, "");
}

// ===============================
// Validation du fichier
// ===============================
function validateFile(file) {
  if (!file) {
    return "Veuillez sélectionner un fichier audio ou vidéo.";
  }

  // Limite de taille : ici 100 Mo
  const maxBytes = 100 * 1024 * 1024;
  if (file.size > maxBytes) {
    return "Fichier trop volumineux (max 50 Mo).";
  }

  // On pourrait vérifier le type MIME si besoin :
  // if (!file.type.startsWith("audio/") && !file.type.startsWith("video/")) {
  //   return "Merci d'envoyer un fichier audio ou vidéo.";
  // }

  return null;
}

// ===============================
// Gestion du formulaire d'upload
// ===============================
uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  resetOutputs();

  const file = fileInput.files[0];
  const err = validateFile(file);
  if (err) {
    setText(errorBox, err);
    show(errorBox);
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("summary", summaryToggle.checked ? "true" : "false");

  // UI : désactiver le bouton et afficher "chargement"
  submitBtn.disabled = true;
  setText(submitBtn, "Transcription en cours...");
  show(progress);
  setText(infoBox, "Transcription en cours, merci de patienter...");
  show(infoBox);

  try {
    const res = await fetch(`${API_BASE}${ENDPOINT}`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const errorText = await res.text().catch(() => "");
      throw new Error(
        `Erreur serveur (${res.status}) : ${errorText || res.statusText}`
      );
    }

    const data = await res.json();

    // On s'attend à { filename, transcript, summary }
    const transcript = data.transcript ?? "";
    const summary = data.summary ?? "";

    if (!transcript) {
      setText(errorBox, "La transcription est vide ou indisponible.");
      show(errorBox);
      return;
    }

    setText(transcriptEl, transcript);

    if (summaryToggle.checked && summary) {
      setText(summaryEl, summary);
    } else if (summaryToggle.checked && !summary) {
      setText(
        summaryEl,
        "(fonctionnalité à améliorer côté serveur)."
      );
    } else {
      setText(summaryEl, "Résumé désactivé.");
    }

    setText(infoBox, "Transcription terminée avec succès.");
    show(infoBox);
  } catch (err) {
    console.error(err);
    setText(
      errorBox,
      "Une erreur est survenue pendant la transcription : " + err.message
    );
    show(errorBox);
  } finally {
    submitBtn.disabled = false;
    setText(submitBtn, "Transcrire");
    hide(progress);
  }
});
