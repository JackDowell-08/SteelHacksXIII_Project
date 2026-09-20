async function sendText() {
  const text = document.getElementById("userInput").value;
  const responseArea = document.getElementById("responseArea");

  responseArea.innerText = "Loading...";

  const response = await fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text })
  });

  const data = await response.json();
  document.getElementById("responseArea").innerText = data.result;
}