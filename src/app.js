const box = document.getElementById("box");
const file = document.getElementById("file");

file.addEventListener("change", async e => {
  const f = e.target.files[0]; if (!f) return;
  const data = JSON.parse(await f.text());
  await fetch("/load", { method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify(data) });
  let i = 0; render();

  async function render() {
    const res = await fetch(`/question?idx=${i}`); const q = await res.json();
    if (q.done) { box.innerHTML = "<h3>All done 🎉</h3>"; return; }
    box.innerHTML = `
      <h3>${q.q}</h3>
      <div class="opts">
        ${q.options.map(o => `<button data-opt="${o}">${o}</button>`).join("")}
      </div>
      ${q.hint ? `<p><em>Hint: ${q.hint}</em></p>` : ""}
      <p>Topic: ${q.topic || "-"}</p>
    `;
    box.querySelectorAll(".opts button").forEach(btn => {
      btn.onclick = async () => {
        const guess = btn.getAttribute("data-opt");
        const r = await fetch(`/answer?idx=${i}&guess=${encodeURIComponent(guess)}`, { method:"POST" });
        const a = await r.json();
        alert(a.correct ? `✅ Correct! Next in ${a.interval}d` : `❌ Correct: ${a.answer}`);
        i++; render();
      };
    });
  }
});
