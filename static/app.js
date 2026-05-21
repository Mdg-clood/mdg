/**
 * AskGL : chat avec mémoire (historique envoyé à l'API) et conversations persistées (localStorage).
 */
(function () {
  var STORAGE_KEY = "askgl_threads_v1";

  var TUTOR_NAME = "AskGL";
  var OFF_TOPIC = "⚠️ Question hors département détectée.";

  try {
    var bootEl = document.getElementById("app-boot");
    if (bootEl && bootEl.textContent) {
      var boot = JSON.parse(bootEl.textContent);
      if (boot.tutorName) TUTOR_NAME = String(boot.tutorName);
      if (boot.offTopic) OFF_TOPIC = String(boot.offTopic);
    }
  } catch (e) {
    console.error("app-boot JSON:", e);
  }

  function introText() {
    return (
      "Bonjour, je suis " +
      TUTOR_NAME +
      ", votre tuteur pour les matières couvertes par la formation (voir la liste à droite). " +
      "Décrivez votre problème ou votre notion à clarifier : je peux expliquer, résumer ou proposer un exemple simple."
    );
  }

  function newId() {
    if (typeof crypto !== "undefined" && crypto.randomUUID) return crypto.randomUUID();
    return "t_" + Date.now() + "_" + Math.floor(Math.random() * 1e9);
  }

  function truncateTitle(text) {
    var t = (text || "").replace(/\s+/g, " ").trim();
    if (t.length <= 52) return t || "Nouvelle conversation";
    return t.slice(0, 49) + "…";
  }

  function formatWhen(iso) {
    try {
      var d = new Date(iso);
      if (isNaN(d.getTime())) return "";
      var now = new Date();
      var sameDay =
        d.getFullYear() === now.getFullYear() &&
        d.getMonth() === now.getMonth() &&
        d.getDate() === now.getDate();
      if (sameDay) {
        return d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
      }
      return d.toLocaleDateString(undefined, { day: "numeric", month: "short" });
    } catch (_) {
      return "";
    }
  }

  var state = {
    threads: [],
    activeId: null,
  };

  function saveState() {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          version: 1,
          threads: state.threads,
          activeId: state.activeId,
        })
      );
    } catch (e) {
      console.warn("Impossible d'enregistrer les conversations (quota ou mode privé).", e);
    }
  }

  function loadState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;
      var data = JSON.parse(raw);
      if (!data || data.version !== 1 || !Array.isArray(data.threads)) return false;
      state.threads = data.threads.filter(function (t) {
        return t && typeof t.id === "string" && Array.isArray(t.messages);
      });
      state.activeId = typeof data.activeId === "string" ? data.activeId : null;
      if (!state.threads.length) return false;
      if (!state.threads.some(function (t) { return t.id === state.activeId; })) {
        state.activeId = state.threads[0].id;
      }
      return true;
    } catch (_) {
      return false;
    }
  }

  function ensureInitialThread() {
    if (loadState()) return;
    var id = newId();
    state.threads = [
      {
        id: id,
        title: "Nouvelle conversation",
        updatedAt: new Date().toISOString(),
        messages: [],
      },
    ];
    state.activeId = id;
    saveState();
  }

  function getActiveThread() {
    return state.threads.find(function (t) { return t.id === state.activeId; }) || null;
  }

  var form = document.getElementById("chatForm");
  var input = document.getElementById("questionInput");
  var chatLog = document.getElementById("chatLog");
  var sendBtn = document.getElementById("sendBtn");
  var spinner = document.getElementById("sendSpinner");
  var statusHint = document.getElementById("statusHint");
  var clearBtn = document.getElementById("clearBtn");
  var tabChat = document.getElementById("tabChat");
  var tabHistory = document.getElementById("tabHistory");
  var panelChat = document.getElementById("panelChat");
  var panelHistory = document.getElementById("panelHistory");
  var threadList = document.getElementById("threadList");
  var newThreadBtn = document.getElementById("newThreadBtn");

  if (!form || !input || !chatLog || !sendBtn || !clearBtn) {
    console.error("Éléments du chat introuvables dans le DOM.");
    return;
  }

  function setLoading(loading) {
    sendBtn.disabled = loading;
    input.disabled = loading;
    if (spinner) spinner.hidden = !loading;
    if (statusHint) statusHint.textContent = loading ? "Réponse en cours…" : "Prêt";
  }

  function appendMessage(role, text, extraClass) {
    var row = document.createElement("div");
    row.className = "msg msg--" + role + (extraClass ? " " + extraClass : "");

    var avatar = document.createElement("div");
    avatar.className = "msg__avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = role === "user" ? "Vous" : TUTOR_NAME;

    var bubble = document.createElement("div");
    bubble.className = "msg__bubble";
    var p = document.createElement("p");
    p.textContent = text;
    bubble.appendChild(p);

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatLog.appendChild(row);
    chatLog.scrollTop = chatLog.scrollHeight;
    return row;
  }

  function showError(message) {
    appendMessage("bot", message, "msg--error");
  }

  function renderChat() {
    var thread = getActiveThread();
    chatLog.innerHTML = "";
    if (!thread) return;
    if (thread.messages.length === 0) {
      appendMessage("bot", introText(), "msg--intro");
    } else {
      thread.messages.forEach(function (m) {
        var uiRole = m.role === "user" ? "user" : "bot";
        var cls =
          m.role === "assistant" && (m.content || "").indexOf(OFF_TOPIC) !== -1 ? "msg--warn" : "";
        appendMessage(uiRole, m.content, cls);
      });
    }
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  function renderThreadList() {
    if (!threadList) return;
    threadList.innerHTML = "";
    var sorted = state.threads
      .slice()
      .sort(function (a, b) {
        return new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0);
      });
    sorted.forEach(function (t) {
      var li = document.createElement("li");
      li.className = "thread-list__item" + (t.id === state.activeId ? " thread-list__item--active" : "");
      li.setAttribute("data-id", t.id);

      var main = document.createElement("button");
      main.type = "button";
      main.className = "thread-list__main";
      var title = document.createElement("span");
      title.className = "thread-list__title";
      title.textContent = t.title || "Conversation";
      var when = document.createElement("span");
      when.className = "thread-list__when";
      when.textContent = formatWhen(t.updatedAt);
      main.appendChild(title);
      main.appendChild(when);
      main.addEventListener("click", function () {
        state.activeId = t.id;
        saveState();
        renderThreadList();
        renderChat();
        activateTab("chat");
      });

      var del = document.createElement("button");
      del.type = "button";
      del.className = "thread-list__del";
      del.setAttribute("aria-label", "Supprimer cette conversation");
      del.textContent = "×";
      del.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (!confirm("Supprimer cette conversation de l'historique local ?")) return;
        state.threads = state.threads.filter(function (x) { return x.id !== t.id; });
        if (!state.threads.length) {
          var id = newId();
          state.threads.push({
            id: id,
            title: "Nouvelle conversation",
            updatedAt: new Date().toISOString(),
            messages: [],
          });
          state.activeId = id;
        } else if (state.activeId === t.id) {
          state.activeId = state.threads[0].id;
        }
        saveState();
        renderThreadList();
        renderChat();
      });

      li.appendChild(main);
      li.appendChild(del);
      threadList.appendChild(li);
    });
  }

  function activateTab(which) {
    var isChat = which === "chat";
    if (tabChat) {
      tabChat.classList.toggle("chat-tabs__btn--active", isChat);
      tabChat.setAttribute("aria-selected", isChat ? "true" : "false");
    }
    if (tabHistory) {
      tabHistory.classList.toggle("chat-tabs__btn--active", !isChat);
      tabHistory.setAttribute("aria-selected", isChat ? "false" : "true");
    }
    if (panelChat) {
      panelChat.classList.toggle("chat-panel--active", isChat);
    }
    if (panelHistory) {
      panelHistory.classList.toggle("chat-panel--active", !isChat);
    }
  }

  if (tabChat && tabHistory && panelChat && panelHistory) {
    tabChat.addEventListener("click", function () {
      activateTab("chat");
    });
    tabHistory.addEventListener("click", function () {
      activateTab("history");
      renderThreadList();
    });
  }

  if (newThreadBtn) {
    newThreadBtn.addEventListener("click", function () {
      var id = newId();
      state.threads.unshift({
        id: id,
        title: "Nouvelle conversation",
        updatedAt: new Date().toISOString(),
        messages: [],
      });
      state.activeId = id;
      saveState();
      renderThreadList();
      renderChat();
      activateTab("chat");
      input.focus();
    });
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    var thread = getActiveThread();
    if (!thread) return;

    var question = input.value.trim();
    if (!question) return;

    if (thread.messages.length === 0) {
      var introEl = chatLog.querySelector(".msg--intro");
      if (introEl && introEl.parentNode) introEl.parentNode.removeChild(introEl);
    }

    appendMessage("user", question);
    var pendingRow = chatLog.lastElementChild;
    input.value = "";
    setLoading(true);

    var historyPayload = thread.messages.map(function (m) {
      return { role: m.role, content: m.content };
    });

    try {
      var res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ question: question, history: historyPayload }),
      });

      var data = await res.json().catch(function () {
        return {};
      });

      if (!res.ok) {
        if (pendingRow && pendingRow.parentNode) pendingRow.parentNode.removeChild(pendingRow);
        var detail = data.detail;
        var msg = "Erreur serveur (" + res.status + ").";
        if (typeof detail === "string") msg = detail;
        else if (Array.isArray(detail) && detail[0] && detail[0].msg) msg = detail[0].msg;
        else if (data.message) msg = data.message;
        showError(msg);
        return;
      }

      var answer = data.answer || "";
      var wasEmpty = thread.messages.length === 0;
      thread.messages.push({ role: "user", content: question });
      thread.messages.push({ role: "assistant", content: answer });
      if (wasEmpty) thread.title = truncateTitle(question);
      thread.updatedAt = new Date().toISOString();
      saveState();

      var isOff = answer.indexOf(OFF_TOPIC) !== -1;
      appendMessage("bot", answer, isOff ? "msg--warn" : "");
      renderThreadList();
    } catch (err) {
      if (pendingRow && pendingRow.parentNode) pendingRow.parentNode.removeChild(pendingRow);
      showError("Impossible de contacter le serveur. Vérifiez votre connexion et que l'API tourne.");
    } finally {
      setLoading(false);
      input.focus();
    }
  });

  clearBtn.addEventListener("click", function () {
    var thread = getActiveThread();
    if (!thread) return;
    thread.messages = [];
    thread.title = "Nouvelle conversation";
    thread.updatedAt = new Date().toISOString();
    saveState();
    renderChat();
    renderThreadList();
  });

  ensureInitialThread();
  renderChat();
  renderThreadList();
  activateTab("chat");
})();
