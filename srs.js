// ──────────────────────────────────────────────────────────────
// English Lessons — SRS + State 模組
// 全部資料用 localStorage 存在使用者瀏覽器,不需要伺服器
// 對應 profile.md §9 詞彙哲學(L4 計量 + 間隔複習)
// ──────────────────────────────────────────────────────────────

const STORE_KEY = "english-lessons-v1";

const DEFAULT_STATE = {
  words: {},        // word → state
  settings: {
    lessonMode: "frequency",   // frequency / random / theme / mixed / review / challenge
    wordsPerRound: 10,
    newReviewRatio: 0.3,        // 30% 新 / 70% 複習
    rememberLastMode: true,
    syllableChunks: true,
    showPinyin: true,           // 注音顯示 / 隱藏(預設顯示)
  },
  stats: {
    totalLessons: 0,
    currentStage: 0,
    lastLesson: null,           // "R1" / "R2"...
    startedAt: null,
  },
  history: [],                  // [{round, date, mode, wordIds, evalEmoji}]
};

// ── 讀寫 ─────────────────────────────────────────────────────
function loadState() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (!raw) return structuredClone(DEFAULT_STATE);
    return Object.assign(structuredClone(DEFAULT_STATE), JSON.parse(raw));
  } catch (e) { return structuredClone(DEFAULT_STATE); }
}
function saveState(s) {
  localStorage.setItem(STORE_KEY, JSON.stringify(s));
}
function resetState() { localStorage.removeItem(STORE_KEY); }

// ── 字狀態初始化 ─────────────────────────────────────────────
function ensureWordState(state, wordKey, seedData) {
  if (state.words[wordKey]) return state.words[wordKey];
  state.words[wordKey] = {
    word: wordKey,
    mean: seedData?.mean || "",
    img: seedData?.img || "",
    chunks: seedData?.chunks || [wordKey],
    py: seedData?.py || "",
    split: seedData?.split || "",
    theme: seedData?.theme || "",
    stage: seedData?.stage ?? 0,
    level: "L1",           // L1 / L2 / L3 / L4 / L5
    first: null,           // 第一次學的輪次 R<n>
    lastSeen: null,        // 上次見過 R<n>
    nextDue: null,         // 該複習 R<n>
    interval: 1,           // 距離單位:輪
    ease: "normal",        // easy / normal / hard
    playCount: 0,          // 點唸整字次數
    chunkPlays: {},        // {chunk: count}
    knewItCount: 0,        // 標記「會」累計
    forgotCount: 0,        // 標記「不會」累計
    consecutiveForgot: 0,  // 連續忘記次數(連 3 次退一層)
    lastMark: null,        // 最近一次標記 "know" / "forgot"(供 UI 還原按鈕變色)
    lastInteraction: null,
  };
  return state.words[wordKey];
}

// ── 點擊計數 ─────────────────────────────────────────────────
function logWordPlay(wordKey, seedData) {
  const state = loadState();
  const w = ensureWordState(state, wordKey, seedData);
  w.playCount += 1;
  w.lastInteraction = new Date().toISOString();
  saveState(state);
}
function logChunkPlay(wordKey, chunk, seedData) {
  const state = loadState();
  const w = ensureWordState(state, wordKey, seedData);
  w.chunkPlays[chunk] = (w.chunkPlays[chunk] || 0) + 1;
  w.lastInteraction = new Date().toISOString();
  saveState(state);
}

// ── SRS 演算法(SuperMemo lite)─────────────────────────────
// interval 表示距離下次複習要幾輪。每次互動更新:
//   會  + easy   → interval × 2.5,推一層
//   會  + normal → interval × 2,看狀態決定升層
//   不會          → interval ÷ 2(最少 1),連續 3 次退一層
const LEVELS = ["L1", "L2", "L3", "L4", "L5"];

function knewIt(wordKey, currentRound, easeOverride) {
  const state = loadState();
  const w = state.words[wordKey];
  if (!w) return;
  const ease = easeOverride || w.ease || "normal";
  const mult = ease === "easy" ? 2.5 : ease === "hard" ? 1.5 : 2;
  w.knewItCount += 1;
  w.lastMark = "know";
  w.consecutiveForgot = 0;
  w.interval = Math.max(1, Math.round(w.interval * mult));
  // 升層條件:點擊次數低(< 3) + 連續答對 ≥ 2 → 升一層
  const idx = LEVELS.indexOf(w.level);
  if (idx < LEVELS.length - 1 && w.knewItCount >= 2 && w.playCount < 5) {
    w.level = LEVELS[idx + 1];
  }
  w.lastSeen = currentRound;
  w.nextDue = bumpRound(currentRound, w.interval);
  saveState(state);
}

function forgotIt(wordKey, currentRound) {
  const state = loadState();
  const w = state.words[wordKey];
  if (!w) return;
  w.forgotCount += 1;
  w.lastMark = "forgot";
  w.consecutiveForgot += 1;
  w.interval = Math.max(1, Math.floor(w.interval / 2));
  // 連續忘 3 次 → 退一層
  if (w.consecutiveForgot >= 3) {
    const idx = LEVELS.indexOf(w.level);
    if (idx > 0) w.level = LEVELS[idx - 1];
    w.consecutiveForgot = 0;
  }
  w.lastSeen = currentRound;
  w.nextDue = bumpRound(currentRound, w.interval);
  saveState(state);
}

function bumpRound(roundStr, by) {
  const n = parseInt((roundStr || "R0").replace("R", ""), 10) || 0;
  return "R" + (n + by);
}
function roundNum(roundStr) {
  return parseInt((roundStr || "R0").replace("R", ""), 10) || 0;
}

// ── 拉取「該複習」「該新學」名單 ───────────────────────────
function dueForReview(currentRound) {
  const state = loadState();
  const cur = roundNum(currentRound);
  return Object.values(state.words)
    .filter(w => w.nextDue && roundNum(w.nextDue) <= cur)
    .sort((a, b) => roundNum(a.nextDue) - roundNum(b.nextDue));
}

function l4Count() {
  const state = loadState();
  return Object.values(state.words).filter(w => w.level === "L4" || w.level === "L5").length;
}
function totalLearned() {
  const state = loadState();
  return Object.keys(state.words).length;
}
function l4Ratio() {
  const total = totalLearned();
  return total === 0 ? 0 : l4Count() / total;
}

// ── 設定 ─────────────────────────────────────────────────────
function getSettings() { return loadState().settings; }
function setSetting(key, value) {
  const state = loadState();
  state.settings[key] = value;
  saveState(state);
}

// ── 輪次紀錄 ─────────────────────────────────────────────────
function recordLesson(roundStr, mode, wordIds, evalEmoji) {
  const state = loadState();
  state.stats.totalLessons += 1;
  state.stats.lastLesson = roundStr;
  if (!state.stats.startedAt) state.stats.startedAt = new Date().toISOString();
  state.history.push({
    round: roundStr,
    date: new Date().toISOString(),
    mode, wordIds, evalEmoji
  });
  // 每字 first / lastSeen 在此輪初次見到的設定
  const curN = roundNumber(roundStr);
  for (const w of wordIds) {
    const word = state.words[w];
    if (word) {
      if (!word.first) word.first = roundStr;
      word.lastSeen = roundStr;
      if (!word.nextDue) {
        // 首次見到:預設下輪複習
        word.nextDue = bumpRound(roundStr, 1);
      } else {
        // 已有 nextDue 的字,本輪沒被 ✅/❌ 主動標 → 算「中性看過」,
        // 把 nextDue 推到 max(interval, 2) 輪後,避免下輪又被抽到同一批
        const dueN = roundNumber(word.nextDue);
        if (dueN <= curN) {
          // 此輪被當 review 抽到但沒主動標
          // (有主動標的情況 knewIt/forgotIt 已先把 nextDue 改到未來)
          const push = Math.max(word.interval || 1, 2);
          word.nextDue = bumpRound(roundStr, push);
        }
      }
    }
  }
  saveState(state);
}
function roundNumber(s) { const m = /^R?(\d+)/.exec(s||""); return m ? parseInt(m[1],10) : 0; }

function getCurrentRound() {
  const state = loadState();
  const last = state.stats.lastLesson;
  if (!last) return "R1";
  return bumpRound(last, 1);
}

// ── Export / Import 同步用 ──────────────────────────────────
function exportState() {
  return JSON.stringify(loadState(), null, 2);
}
function importState(json) {
  try {
    const parsed = JSON.parse(json);
    saveState(parsed);
    return true;
  } catch (e) { return false; }
}

// ── 暴露給頁面 ──────────────────────────────────────────────
window.SRS = {
  loadState, saveState, resetState,
  ensureWordState,
  logWordPlay, logChunkPlay,
  knewIt, forgotIt,
  dueForReview, l4Count, totalLearned, l4Ratio,
  getSettings, setSetting,
  recordLesson, getCurrentRound,
  exportState, importState,
  bumpRound, roundNum,
  LEVELS,
};
