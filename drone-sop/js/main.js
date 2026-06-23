// 高雄機場無人機 SOP - interaction helpers
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
      a.setAttribute('aria-label', '點擊撥打電話 ' + a.textContent.trim());
    });
    document.querySelectorAll('a[target="_blank"]').forEach(function (a) {
      a.setAttribute('rel', 'noopener');
    });
  });
})();
