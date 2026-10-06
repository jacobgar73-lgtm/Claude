(function () {
  document.documentElement.classList.remove("no-js");

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && links.classList.contains("open")) {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // Hero video: respect reduced motion, offer pause/play
  var video = document.querySelector(".hero-media video");
  var vbtn = document.querySelector(".video-toggle");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (video) {
    if (reduce) video.pause();
    var sync = function () {
      if (!vbtn) return;
      var paused = video.paused;
      vbtn.setAttribute("aria-label", paused ? "Play video" : "Pause video");
      vbtn.innerHTML = paused
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.5"/><rect x="14" y="5" width="4" height="14" rx="1.5"/></svg>';
    };
    video.addEventListener("play", sync);
    video.addEventListener("pause", sync);
    if (vbtn) vbtn.addEventListener("click", function () { video.paused ? video.play() : video.pause(); });
    sync();
  }

  // Reveal on scroll
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    document.documentElement.classList.add("js-motion");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // Footer year
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Forms: no backend yet, so compose an email to LTN with the answers.
  // Swap data-mailto for a real form endpoint (e.g. Formspree, Wix, Jotform) when ready.
  document.querySelectorAll("form[data-mailto]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || !el.value) return;
        var label = form.querySelector('label[for="' + el.id + '"]');
        lines.push((label ? label.textContent.replace(/\s*\*$/, "") : el.name) + ": " + el.value);
      });
      var subject = form.getAttribute("data-subject") || "Website message";
      window.location.href = "mailto:" + form.getAttribute("data-mailto") +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      var status = form.querySelector(".form-status");
      if (status) {
        status.textContent = "Thank you! Your email app should open with your message ready to send. If it doesn't, email us at Info@LtnTexas.org or call (956) 320-3378.";
        status.classList.add("show");
      }
    });
  });
})();
