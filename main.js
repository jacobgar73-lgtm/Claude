/* Love Thy Neighbor: small behaviours. The site works fully without this file. */
(function () {
  'use strict';

  /* Mobile menu */
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.toggleAttribute('data-open', !open);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        toggle.setAttribute('aria-expanded', 'false');
        nav.removeAttribute('data-open');
        toggle.focus();
      }
    });
  }

  /* Chart marks grow from their baseline the first time a chart is seen. */
  var charts = document.querySelectorAll('[data-animate]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window) || reduce) {
    charts.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          seen.unobserve(entry.target);
        }
      });
    }, { threshold: 0.25 });
    charts.forEach(function (el) { seen.observe(el); });
  }

  /* Tooltip on chart marks. Every value is also printed beside its mark. */
  var tip = null;
  function showTip(target, x, y) {
    if (!tip) {
      tip = document.createElement('div');
      tip.className = 'tip';
      tip.setAttribute('role', 'tooltip');
      document.body.appendChild(tip);
    }
    var parts = String(target.getAttribute('data-tip')).split('|');
    tip.textContent = '';
    var strong = document.createElement('strong');
    strong.textContent = parts[0].trim();
    tip.appendChild(strong);
    if (parts[1]) tip.appendChild(document.createTextNode(parts[1].trim()));
    tip.hidden = false;
    var half = tip.offsetWidth / 2 + 8;
    var left = Math.min(Math.max(x, half), document.documentElement.clientWidth - half);
    tip.style.left = left + window.scrollX + 'px';
    tip.style.top = y + window.scrollY + 'px';
  }
  function hideTip() { if (tip) tip.hidden = true; }
  document.querySelectorAll('[data-tip]').forEach(function (el) {
    el.addEventListener('pointermove', function (event) { showTip(el, event.clientX, event.clientY); });
    el.addEventListener('pointerleave', hideTip);
    el.addEventListener('focus', function () {
      var box = el.getBoundingClientRect();
      showTip(el, box.left + box.width / 2, box.top);
    });
    el.addEventListener('blur', hideTip);
  });

  /* Forms: there is no server yet, so a form opens the visitor's email app with
     the answers filled in. Replace data-mailto with a real form service before launch. */
  document.querySelectorAll('form[data-mailto]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (typeof form.reportValidity === 'function' && !form.reportValidity()) return;
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || !el.value) return;
        if ((el.type === 'radio' || el.type === 'checkbox') && !el.checked) return;
        var label = el.getAttribute('data-label') || el.name;
        lines.push(label + ': ' + el.value);
      });
      var href = 'mailto:' + form.getAttribute('data-mailto') +
        '?subject=' + encodeURIComponent(form.getAttribute('data-subject') || 'Message from the website') +
        '&body=' + encodeURIComponent(lines.join('\n'));
      var status = form.querySelector('.form__status');
      if (status) {
        status.hidden = false;
        status.textContent = 'Your email app should open with this message ready to send. If it does not, call (956) 320-3378 or write to Info@LtnTexas.org.';
      }
      window.location.href = href;
    });
  });

  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
