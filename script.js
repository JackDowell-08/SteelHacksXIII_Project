async function sendText() {
  const text = document.getElementById("userInput").value;

  const response = await fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text })
  });

  const data = await response.json();
  document.getElementById("responseArea").innerText = data.result;
}