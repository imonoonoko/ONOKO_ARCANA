(() => {
const { CARD_BACK, cards, spreads } = window.OnokoArcanaData;

const historyKey = "onoko-arcana:desktop:history:v1";

const state = {
  spreadId: "one_card",
  drawn: [],
  revealedCount: 0,
  selectedIndex: -1,
  notes: {},
  guideVisible: false,
  restoredAt: null
};

const els = {
  questionInput: document.getElementById("questionInput"),
  spreadControls: document.getElementById("spreadControls"),
  spreadTitle: document.getElementById("spreadTitle"),
  spreadDescription: document.getElementById("spreadDescription"),
  spreadBoard: document.getElementById("spreadBoard"),
  drawButton: document.getElementById("drawButton"),
  revealButton: document.getElementById("revealButton"),
  saveReadingButton: document.getElementById("saveReadingButton"),
  resetButton: document.getElementById("resetButton"),
  progressTrack: document.getElementById("progressTrack"),
  statusLine: document.getElementById("statusLine"),
  selectedCard: document.getElementById("selectedCard"),
  noteInput: document.getElementById("noteInput"),
  noteStatus: document.getElementById("noteStatus"),
  toggleGuideButton: document.getElementById("toggleGuideButton"),
  guidePanel: document.getElementById("guidePanel"),
  historyList: document.getElementById("historyList"),
  exportHistoryButton: document.getElementById("exportHistoryButton"),
  statCards: document.getElementById("statCards"),
  statRevealed: document.getElementById("statRevealed"),
  statSaved: document.getElementById("statSaved")
};

function currentSpread() {
  return spreads.find((spread) => spread.id === state.spreadId) || spreads[0];
}

function readHistory() {
  try {
    return JSON.parse(localStorage.getItem(historyKey) || "[]");
  } catch {
    return [];
  }
}

function writeHistory(history) {
  localStorage.setItem(historyKey, JSON.stringify(history.slice(0, 48)));
}

function shuffleDeck() {
  const pool = [...cards];
  for (let index = pool.length - 1; index > 0; index -= 1) {
    const swap = Math.floor(Math.random() * (index + 1));
    [pool[index], pool[swap]] = [pool[swap], pool[index]];
  }
  return pool;
}

function drawSpread() {
  const spread = currentSpread();
  state.drawn = shuffleDeck()
    .slice(0, spread.slots.length)
    .map((card) => ({ ...card, reversed: Math.random() < 0.32 }));
  state.revealedCount = 0;
  state.selectedIndex = -1;
  state.notes = {};
  state.guideVisible = false;
  state.restoredAt = null;
  els.noteStatus.textContent = "";
  render();
}

function revealNext() {
  if (!state.drawn.length) drawSpread();
  if (state.revealedCount >= state.drawn.length) return;
  state.revealedCount += 1;
  state.selectedIndex = state.revealedCount - 1;
  state.guideVisible = false;
  els.noteStatus.textContent = "自分の読みを記録";
  render();
}

function resetTable() {
  state.drawn = [];
  state.revealedCount = 0;
  state.selectedIndex = -1;
  state.notes = {};
  state.guideVisible = false;
  state.restoredAt = null;
  els.noteStatus.textContent = "";
  render();
}

function slotIsRevealed(index) {
  return index >= 0 && index < state.revealedCount;
}

function selectedSlot() {
  const spread = currentSpread();
  if (!slotIsRevealed(state.selectedIndex)) return null;
  return {
    index: state.selectedIndex,
    slot: spread.slots[state.selectedIndex],
    card: state.drawn[state.selectedIndex]
  };
}

function slotNoteKey(slot, index) {
  return `${index + 1}:${slot.key}`;
}

function selectedNote() {
  const selected = selectedSlot();
  if (!selected) return "";
  return state.notes[slotNoteKey(selected.slot, selected.index)] || "";
}

function keywordLine(card) {
  const list = card.reversed ? card.reversedKeywords : card.uprightKeywords;
  return list.slice(0, 3).join(" / ");
}

function escapeText(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderSpreadMini(spread) {
  return `
    <span class="spread-mini" aria-hidden="true">
      ${spread.slots.map((slot, index) => `
        <span class="spread-mini-slot ${index === 0 ? "is-first" : ""}" style="--x:${slot.x}%; --y:${slot.y}%; --rot:${slot.rot}deg;"></span>
      `).join("")}
      <span class="spread-mini-count">${spread.slots.length}</span>
    </span>
  `;
}

function renderSpreadControls() {
  els.spreadControls.innerHTML = spreads.map((spread) => `
    <button class="spread-choice ${spread.id === state.spreadId ? "is-active" : ""}" type="button" data-spread-id="${spread.id}">
      ${renderSpreadMini(spread)}
      <span class="spread-choice-copy">
        <strong>${escapeText(spread.label)}</strong>
        <span>${escapeText(spread.description)}</span>
      </span>
    </button>
  `).join("");

  els.spreadControls.querySelectorAll("[data-spread-id]").forEach((button) => {
    button.addEventListener("click", () => {
      if (state.spreadId === button.dataset.spreadId) return;
      state.spreadId = button.dataset.spreadId;
      resetTable();
    });
  });
}

function boardTextMode(spread) {
  if (spread.slots.length <= 3) return "inscription";
  return "marker";
}

function renderBoard() {
  const spread = currentSpread();
  const textMode = boardTextMode(spread);
  const dense = textMode === "marker";
  els.spreadBoard.className = `spread-board layout-${spread.id} mode-${textMode} ${dense ? "is-dense-board" : ""}`;
  els.spreadBoard.innerHTML = spread.slots.map((slot, index) => {
    const card = state.drawn[index];
    const revealed = slotIsRevealed(index);
    const selected = revealed && index === state.selectedIndex;
    const image = card && revealed ? card.image : CARD_BACK;
    const slotClasses = [
      "slot",
      card ? "is-filled" : "",
      revealed ? "is-revealed" : "",
      selected ? "is-selected" : ""
    ].filter(Boolean).join(" ");
    const classes = [
      "arcana-card",
      !card ? "is-empty" : "",
      card && !revealed ? "is-hidden" : "",
      card && revealed && card.reversed ? "is-reversed" : "",
      selected ? "is-selected" : ""
    ].filter(Boolean).join(" ");
    const topLabel = card && revealed ? `${card.number} ${card.japaneseName}` : card ? "カード裏面" : "空きスロット";
    const orientation = card && revealed ? (card.reversed ? "逆位置" : "正位置") : "";
    const orientationShort = card && revealed ? (card.reversed ? "逆" : "正") : "";
    const cardInscription = card && revealed && textMode === "inscription" ? `
          <span class="card-inscription top"><span>${escapeText(topLabel)}</span><span class="orientation">${orientation}</span></span>
          <span class="card-inscription bottom">${escapeText(keywordLine(card))}</span>
        ` : "";
    const cardMarker = card && revealed && textMode === "marker" ? `
          <span class="card-marker" aria-hidden="true">
            <span>${index + 1}</span>
            <small>${orientationShort}</small>
          </span>
        ` : "";
    const slotLabelMarkup = dense ? "" : `
        <div class="slot-label" title="${index + 1}. ${escapeText(slot.label)}">
          <span class="slot-label-index">${index + 1}</span>
          <span class="slot-label-text">${escapeText(slot.label)}</span>
        </div>
      `;
    return `
      <div class="${slotClasses}" style="--x:${slot.x}%; --y:${slot.y}%; --rot:${slot.rot}deg; --counter-rot:${-slot.rot}deg;">
        ${slotLabelMarkup}
        <button class="${classes}" type="button" data-slot-index="${index}" ${!revealed ? "aria-disabled='true'" : ""}>
          ${card ? `<img class="${card.reversed && revealed ? "reversed" : ""}" src="${image}" alt="${escapeText(topLabel)}">` : "<span class='empty-mark'></span>"}
          ${cardInscription}
          ${cardMarker}
        </button>
      </div>
    `;
  }).join("");

  els.spreadBoard.querySelectorAll("[data-slot-index]").forEach((button) => {
    button.addEventListener("click", () => {
      const index = Number(button.dataset.slotIndex);
      if (!slotIsRevealed(index)) return;
      state.selectedIndex = index;
      state.guideVisible = false;
      els.noteStatus.textContent = selectedNote() ? "記録済み" : "自分の読みを記録";
      render();
    });
  });
}

function renderProgress() {
  const spread = currentSpread();
  els.progressTrack.innerHTML = spread.slots.map((slot, index) => {
    const revealed = slotIsRevealed(index);
    const selected = revealed && index === state.selectedIndex;
    return `
      <button class="progress-dot ${revealed ? "is-revealed" : ""} ${selected ? "is-selected" : ""}" type="button" data-progress-index="${index}">
        <span class="progress-gem" aria-hidden="true"></span>
        <span>${index + 1}. ${escapeText(slot.label)}</span>
      </button>
    `;
  }).join("");

  els.progressTrack.querySelectorAll("[data-progress-index]").forEach((button) => {
    button.addEventListener("click", () => {
      const index = Number(button.dataset.progressIndex);
      if (!slotIsRevealed(index)) return;
      state.selectedIndex = index;
      state.guideVisible = false;
      render();
    });
  });
}

function renderInspector() {
  const selected = selectedSlot();
  if (!selected) {
    els.selectedCard.innerHTML = `
      <img src="${CARD_BACK}" alt="カード裏面">
      <div class="selected-copy">
        <h2>未選択</h2>
        <p>カードをめくると、選択中の読みが表示されます。</p>
        <div class="badge-row"><span class="badge gold">${escapeText(currentSpread().label)}</span></div>
      </div>
    `;
    els.noteInput.value = "";
    els.noteInput.disabled = true;
    els.toggleGuideButton.disabled = true;
    els.toggleGuideButton.textContent = "ガイド表示";
    els.guidePanel.innerHTML = `<p class="empty">まだ表示するカードがありません。</p>`;
    return;
  }

  const { index, slot, card } = selected;
  const orientationText = card.reversed ? "逆位置" : "正位置";
  const activeKeywords = card.reversed ? card.reversedKeywords : card.uprightKeywords;
  const note = selectedNote();
  els.selectedCard.innerHTML = `
    <img class="${card.reversed ? "reversed" : ""}" src="${card.image}" alt="${escapeText(`${card.number} ${card.japaneseName}`)}">
    <div class="selected-copy">
      <h2>${escapeText(card.japaneseName)}</h2>
      <p>${escapeText(card.englishName)}</p>
      <div class="badge-row">
        <span class="badge gold">${index + 1}. ${escapeText(slot.label)}</span>
        <span class="badge">${escapeText(card.number)}</span>
        <span class="badge">${orientationText}</span>
      </div>
    </div>
  `;
  els.noteInput.disabled = false;
  els.noteInput.value = note;
  els.toggleGuideButton.disabled = !note.trim();
  els.toggleGuideButton.textContent = state.guideVisible ? "ガイド非表示" : "ガイド表示";

  if (!note.trim()) {
    els.guidePanel.innerHTML = `<p class="empty">先に自分の読みを一行書くと、ガイドを開けます。</p>`;
    return;
  }

  if (!state.guideVisible) {
    els.guidePanel.innerHTML = `<p class="empty">自分の読みを残しました。必要な時だけガイドを開きます。</p>`;
    return;
  }

  els.guidePanel.innerHTML = `
    <div class="guide-row"><b>${escapeText(slot.label)}</b><span>${escapeText(slot.prompt)}</span></div>
    <div class="guide-row"><b>${orientationText}</b><span>${escapeText(activeKeywords.join(" / "))}</span></div>
    <div class="guide-row"><b>学習観点</b><span>${escapeText(card.studyFocus)}</span></div>
  `;
}

function renderHistory() {
  const history = readHistory();
  els.statSaved.textContent = String(history.length);
  els.exportHistoryButton.disabled = history.length === 0;
  if (!history.length) {
    els.historyList.innerHTML = `<p class="empty">保存済みのリーディングはありません。</p>`;
    return;
  }

  els.historyList.innerHTML = history.map((item, index) => `
    <button class="history-item" type="button" data-history-index="${index}">
      <b>${escapeText(item.spreadLabel)} / ${escapeText(item.savedAt)}</b>
      <span>${escapeText(item.summary)}${item.question ? ` / ${escapeText(item.question)}` : ""}</span>
    </button>
  `).join("");

  els.historyList.querySelectorAll("[data-history-index]").forEach((button) => {
    button.addEventListener("click", () => restoreHistory(Number(button.dataset.historyIndex)));
  });
}

function renderStatus() {
  const spread = currentSpread();
  els.spreadTitle.textContent = spread.label;
  els.spreadDescription.textContent = spread.description;
  els.statCards.textContent = String(spread.slots.length);
  els.statRevealed.textContent = String(state.revealedCount);
  els.revealButton.disabled = !state.drawn.length || state.revealedCount >= state.drawn.length;
  els.saveReadingButton.disabled = state.revealedCount === 0;
  const total = state.drawn.length || spread.slots.length;
  const status = state.revealedCount
    ? `${state.revealedCount} / ${total} opened`
    : state.drawn.length
      ? "Cards placed face down"
      : "Ready";
  els.statusLine.textContent = state.restoredAt ? `${status} / restored ${state.restoredAt}` : status;
}

function render() {
  renderSpreadControls();
  renderBoard();
  renderProgress();
  renderInspector();
  renderHistory();
  renderStatus();
}

function updateCurrentNote() {
  const selected = selectedSlot();
  if (!selected) return;
  state.notes[slotNoteKey(selected.slot, selected.index)] = els.noteInput.value;
  state.guideVisible = false;
  els.noteStatus.textContent = els.noteInput.value.trim() ? "記録中" : "自分の読みを記録";
  renderInspector();
}

function saveReading() {
  const spread = currentSpread();
  if (!state.revealedCount) return;
  const revealedCards = state.drawn.slice(0, state.revealedCount).map((card, index) => {
    const slot = spread.slots[index];
    return {
      cardId: card.id,
      number: card.number,
      japaneseName: card.japaneseName,
      englishName: card.englishName,
      reversed: card.reversed,
      slotKey: slot.key,
      slotLabel: slot.label,
      note: state.notes[slotNoteKey(slot, index)] || ""
    };
  });
  const item = {
    savedAt: new Date().toLocaleString("ja-JP"),
    question: els.questionInput.value.trim(),
    spreadId: spread.id,
    spreadLabel: spread.label,
    revealedCount: state.revealedCount,
    notes: state.notes,
    cards: revealedCards,
    summary: revealedCards.map((card) => `${card.slotLabel}:${card.number}${card.reversed ? "逆" : "正"}`).join(" / ")
  };
  const history = readHistory();
  history.unshift(item);
  writeHistory(history);
  els.noteStatus.textContent = "保存しました";
  renderHistory();
  renderStatus();
}

function restoreHistory(index) {
  const item = readHistory()[index];
  if (!item) return;
  const spread = spreads.find((candidate) => candidate.id === item.spreadId);
  if (!spread) return;
  state.spreadId = spread.id;
  state.drawn = item.cards.map((entry) => {
    const card = cards.find((candidate) => candidate.id === entry.cardId);
    return card ? { ...card, reversed: entry.reversed } : null;
  }).filter(Boolean);
  state.revealedCount = state.drawn.length;
  state.selectedIndex = state.drawn.length ? 0 : -1;
  state.notes = item.notes || {};
  state.guideVisible = false;
  state.restoredAt = item.savedAt;
  els.questionInput.value = item.question || "";
  els.noteStatus.textContent = "履歴を復元";
  render();
}

function exportHistory() {
  const payload = {
    app: "ONOKO_ARCANA",
    schemaVersion: 1,
    exportedAt: new Date().toISOString(),
    history: readHistory()
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `onoko-arcana-readings-${new Date().toISOString().slice(0, 10)}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

els.drawButton.addEventListener("click", drawSpread);
els.revealButton.addEventListener("click", revealNext);
els.resetButton.addEventListener("click", resetTable);
els.saveReadingButton.addEventListener("click", saveReading);
els.exportHistoryButton.addEventListener("click", exportHistory);
els.noteInput.addEventListener("input", updateCurrentNote);
els.toggleGuideButton.addEventListener("click", () => {
  if (!selectedNote().trim()) return;
  state.guideVisible = !state.guideVisible;
  renderInspector();
});

render();
})();
