(() => {
  const saved = localStorage.getItem('homepage-language');
  let language = new URLSearchParams(location.search).get('lang') || saved || 'en';
  const apply = next => {
    language = next === 'zh' ? 'zh' : 'en';
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-en][data-zh]').forEach(el => { el.textContent = el.dataset[language]; });
    document.querySelectorAll('[data-language]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.language === language)));
    document.querySelectorAll('[data-cv]').forEach(link => { link.href = language === 'zh' ? 'assets/郭浩然简历.pdf' : 'assets/Haoran_Guo_CV.pdf'; });
    localStorage.setItem('homepage-language', language);
    window.homepageLanguage = language;
    document.dispatchEvent(new CustomEvent('languagechange', { detail: language }));
  };
  document.querySelectorAll('[data-language]').forEach(button => button.addEventListener('click', () => apply(button.dataset.language)));
  apply(language);
})();
