/* =========================================================
   DRB 网站优化 · 滚动揭示动画
   轻量、无依赖：IntersectionObserver 触发元素淡入；
   不支持时优雅降级，内容始终可见。
   ========================================================= */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js-anim');

  // 需要揭示动画的元素
  var selector = '.card-widget, .recent-post-item, article, .note, .flink, section';
  var targets = document.querySelectorAll(selector);

  // 先给元素打上 reveal 标记（此时因 html.js-anim 才隐藏）
  for (var i = 0; i < targets.length; i++) {
    targets[i].classList.add('reveal');
  }

  function showAll() {
    for (var i = 0; i < targets.length; i++) {
      targets[i].classList.add('in-view');
    }
  }

  if (!('IntersectionObserver' in window)) {
    showAll();
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  for (var j = 0; j < targets.length; j++) {
    io.observe(targets[j]);
  }

  // 兜底：3 秒后强制显示，防止极端情况下元素残留隐藏
  setTimeout(showAll, 3000);
})();

/* =========================================================
   移动端侧栏菜单：关闭按钮 + 触摸友好增强
   - 点击 / 键盘（Enter/Space）关闭抽屉
   - 与已有 main.js 的 sidebarFn 解耦，独立健壮
   ========================================================= */
(function () {
  'use strict';

  function closeSidebar() {
    var sb = document.getElementById('sidebar-menus');
    var mask = document.getElementById('menu-mask');
    if (sb) sb.classList.remove('open');
    if (mask) mask.style.display = 'none';
  }

  function bind() {
    var btn = document.getElementById('sidebar-close');
    if (!btn) return;
    btn.addEventListener('click', closeSidebar);
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        closeSidebar();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
})();
