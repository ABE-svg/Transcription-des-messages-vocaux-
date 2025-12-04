// Gestion du formulaire d'upload
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

//
function validateFile(file) {
  const maxBytes = 100 * 1024 * 1024; // limite 100MB
  if (!file) return "Aucun fichier sélectionné.";
  if (file.size > maxBytes) return "Fichier trop volumineux (max 50MB).";
  // Pas de restriction sur le type MIME ou l'extension
  return null;
}

// Helpers pour afficher/masquer et écrire du texte
function setText(el, text) {
  el.textContent = text;
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
