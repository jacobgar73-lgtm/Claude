/* Love Thy Neighbor: menu, counting numbers, before/after slider, giving picker, referral form. */
(function () {
  'use strict';

  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Numbers that count up once, when they scroll into view.
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var counters = document.querySelectorAll('[data-count]');
  function show(el, n) {
    el.textContent = (el.dataset.prefix || '') + Math.round(n).toLocaleString('en-US') + (el.dataset.suffix || '');
  }
  if (counters.length && !reduced && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var end = Number(el.dataset.count);
        var start = null;
        io.unobserve(el);
        function step(ts) {
          if (start === null) start = ts;
          var p = Math.min((ts - start) / 1200, 1);
          show(el, end * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { io.observe(el); });
  }

  // Before and after slider
  document.querySelectorAll('[data-ba]').forEach(function (ba) {
    var frame = ba.querySelector('.ba__frame');
    var range = ba.querySelector('.ba__range');
    range.addEventListener('input', function () {
      frame.style.setProperty('--pos', range.value + '%');
    });
  });

  // Giving picker: frequency and amount update the button label and link.
  document.querySelectorAll('[data-give]').forEach(function (box) {
    var label = box.querySelector('[data-give-label]');
    var button = box.querySelector('[data-give-button]');
    var base = button.getAttribute('href');
    var monthly = document.documentElement.lang === 'es' ? 'al mes' : 'monthly';
    var once = document.documentElement.lang === 'es' ? 'una vez' : 'one time';
    function update() {
      var freq = box.querySelector('[data-frequency].is-active').dataset.frequency;
      var amount = box.querySelector('[data-amount].is-active').dataset.amount;
      label.textContent = '$' + amount + ' ' + (freq === 'monthly' ? monthly : once);
      if (base.indexOf('mailto:') === 0) {
        button.href = base.split('?')[0] + '?subject=' + encodeURIComponent('I would like to give $' + amount + ' ' + freq);
      } else {
        button.href = base + (base.indexOf('?') > -1 ? '&' : '?') + 'amount=' + amount + '&frequency=' + freq;
      }
    }
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-frequency], [data-amount]');
      if (!b) return;
      var group = b.hasAttribute('data-frequency') ? '[data-frequency]' : '[data-amount]';
      box.querySelectorAll(group).forEach(function (x) {
        x.classList.toggle('is-active', x === b);
        if (x.hasAttribute('aria-pressed')) x.setAttribute('aria-pressed', String(x === b));
      });
      update();
    });
    update();
  });

  // Referral form. Posts to the form service set in content/site.json (form_endpoint).
  // Until one is set, it opens the visitor's email app with the answers filled in.
  document.querySelectorAll('[data-form]').forEach(function (form) {
    var status = form.querySelector('.form__status');
    function say(key, isError) {
      status.textContent = status.dataset[key];
      status.classList.toggle('is-error', !!isError);
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      form.querySelectorAll('[required]').forEach(function (f) {
        var bad = !f.value.trim();
        f.setAttribute('aria-invalid', String(bad));
        if (bad && !firstBad) firstBad = f;
      });
      if (firstBad) { say('error', true); firstBad.focus(); return; }
      if (form.elements._gotcha && form.elements._gotcha.value) return; // spam trap

      var data = new FormData(form);
      data.delete('_gotcha');
      var endpoint = form.dataset.endpoint;
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(); form.reset(); say('success'); })
          .catch(function () { openMail(data); });
      } else {
        openMail(data);
      }
    });
    function openMail(data) {
      var lines = [];
      data.forEach(function (value, key) { lines.push(key + ': ' + value); });
      window.location.href = 'mailto:' + form.dataset.mailto +
        '?subject=' + encodeURIComponent(form.dataset.subject) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      say('fallback');
    }
  });
})();
