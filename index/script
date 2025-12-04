const API_BASE = window.location.origin; // si frontend monté par FastAPI
const ENDPOINT = "/whisper"; 

const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const summaryToggle = document.getElementById("summaryToggle");
const submitBtn = document.getElementById("submitBtn");

const progress = document.getElementById("progress");
const errorBox = document.getElementById("errorBox");
const infoBox = document.getElementById("infoBox");

const transcriptEl = document.getElementById("transcript");
const summaryEl = document.getElementById("summary");

function show(el) { el.classList.remove("hidden"); }
function hide(el) { el.classList.add("hidden"); }
function setText(el, text) { el.textContent = text ?? ""; }

function resetOutputs() {
  setText(transcriptEl, "");
  setText(summaryEl, "");
  hide(errorBox);
  hide(infoBox);
}

function validateFile(file) {
  // Exemple: limite 50MB, formats audio courants
  const maxBytes = 50 * 1024 * 1024;
  const allowed = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp4", "audio/aac", "audio/ogg", "audio/webm"];
  if (!file) return "Aucun fichier sélectionné.";
  if (file.size > maxBytes) return "Fichier trop volumineux (max 50MB).";
  if (!allowed.includes(file.type) && !file.name.toLowerCase().match(/\.(mp3|wav|m4a|aac|ogg|webm)$/)) {
    return "Format non reconnu. Essaie mp3, wav, m4a, aac, ogg, webm.";
  }
  return null;
}

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
  //  "file" ou "files"
  formData.append("file", file);
  // API demande un param "summary" booléen ou string:
  formData.append("summary", summaryToggle.checked ? "true" : "false");

  try {
    submitBtn.disabled = true;
    show(progress);

    const res = await fetch(`${API_BASE}${ENDPOINT}`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `Erreur HTTP ${res.status}`);
    }

    const data = await res.json();


    const transcript = data.transcript ?? data?.results?.[0]?.transcript ?? "";
    const summary = data.summary ?? data?.results?.[0]?.summary ?? "";

    setText(transcriptEl, transcript || "—");
    setText(summaryEl, summary || (summaryToggle.checked ? "—" : "Résumé désactivé"));

    setText(infoBox, "Transcription terminée.");
    show(infoBox);
  } catch (error) {
    setText(errorBox, `Échec: ${error.message}`);
    show(errorBox);
  } finally {
    hide(progress);
    submitBtn.disabled = false;
  }
});
