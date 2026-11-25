(() => {
  const container = document.querySelector("[data-product-comments]");
  if (!container) return;

  const form = container.querySelector("[data-comment-form]");
  const list = container.querySelector("[data-comment-list]");
  const status = container.querySelector("[data-comments-status]");
  const language = () => document.documentElement.lang === "hi" ? "hi" : "en";
  const messages = {
    en: { empty: "No comments yet. Be the first to share your experience.", loaded: "Comments are up to date. New comments will appear here automatically.", sent: "Your comment was shared.", error: "Could not submit your comment. Please try again.", invalid: "Enter your name and a comment of up to 500 characters." },
    hi: { empty: "अभी कोई टिप्पणी नहीं है। अपने अनुभव को साझा करने वाले पहले व्यक्ति बनें।", loaded: "टिप्पणियाँ अपडेट हैं। नई टिप्पणियाँ यहाँ अपने आप दिखाई देंगी।", sent: "आपकी टिप्पणी साझा कर दी गई है।", error: "टिप्पणी भेजी नहीं जा सकी। कृपया फिर से कोशिश करें।", invalid: "अपना नाम और 500 अक्षरों तक की टिप्पणी लिखें।" }
  };
  const text = (key) => messages[language()][key];
  const formatDate = (date) => new Intl.DateTimeFormat(language() === "hi" ? "hi-IN" : "en-IN", { dateStyle: "medium", timeStyle: "short" }).format(new Date(date));
  const addComment = (comment) => {
    if (!comment?.id || list.querySelector(`[data-comment-id="${CSS.escape(comment.id)}"]`)) return;
    const item = document.createElement("li");
    item.className = "product-comment";
    item.dataset.commentId = comment.id;
    const heading = document.createElement("div");
    heading.className = "product-comment-heading";
    const name = document.createElement("strong");
    name.textContent = comment.customerName;
    const date = document.createElement("time");
    date.dateTime = comment.createdAt;
    date.textContent = formatDate(comment.createdAt);
    const body = document.createElement("p");
    body.textContent = comment.text;
    heading.append(name, date);
    item.append(heading, body);
    list.append(item);
  };

  const loadComments = async () => {
    try {
      const response = await fetch(container.dataset.listUrl, { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error("Comment history request failed.");
      const comments = await response.json();
      comments.forEach(addComment);
      status.textContent = comments.length ? text("loaded") : text("empty");
    } catch {
      status.textContent = text("error");
    }
  };

  const stream = new EventSource(container.dataset.liveUrl);
  stream.onmessage = (event) => {
    try {
      addComment(JSON.parse(event.data));
      status.textContent = text("loaded");
    } catch {
      status.textContent = text("error");
    }
  };
  stream.onerror = () => {
    if (stream.readyState === EventSource.CLOSED) status.textContent = text("error");
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submit = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);
    const customerName = String(formData.get("customerName") || "").trim();
    const commentText = String(formData.get("text") || "").trim();
    if (!customerName || customerName.length > 60 || !commentText || commentText.length > 500) {
      status.textContent = text("invalid");
      return;
    }

    submit.disabled = true;
    try {
      const response = await fetch(container.dataset.listUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ customerName, text: commentText })
      });
      if (!response.ok) throw new Error("Comment submission failed.");
      const comment = await response.json();
      addComment(comment);
      form.reset();
      status.textContent = text("sent");
    } catch {
      status.textContent = text("error");
    } finally {
      submit.disabled = false;
    }
  });

  loadComments();
})();
