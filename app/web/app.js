const form = document.querySelector("#chatForm");
const input = document.querySelector("#messageInput");
const sendButton = document.querySelector("#sendButton");
const messages = document.querySelector("#messages");
const statusValue = document.querySelector("#statusValue");
const providerValue = document.querySelector("#providerValue");

function setStatus(value) {
  statusValue.textContent = value;
}

function addMessage(role, text) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const avatar = document.createElement("span");
  avatar.className = "avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = role === "user" ? "You" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  bubble.append(paragraph);

  article.append(avatar, bubble);
  messages.append(article);
  messages.scrollTop = messages.scrollHeight;

  return paragraph;
}

async function sendMessage(message) {
  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = payload.detail || "Request failed";
    throw new Error(detail);
  }

  return payload;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message) {
    return;
  }

  addMessage("user", message);
  input.value = "";
  input.focus();
  sendButton.disabled = true;
  setStatus("Думает");
  const assistantMessage = addMessage("assistant", "...");

  try {
    const result = await sendMessage(message);
    assistantMessage.textContent = result.answer;
    providerValue.textContent = `${result.provider} / ${result.model}`;
    setStatus("Готов");
  } catch (error) {
    assistantMessage.textContent = `Ошибка: ${error.message}`;
    setStatus("Ошибка");
  } finally {
    sendButton.disabled = false;
  }
});

input.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    form.requestSubmit();
  }
});
