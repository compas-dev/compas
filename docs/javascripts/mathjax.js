window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: "\\btex2jax_ignore\\b",
    processHtmlClass: "\\btex2jax_process\\b",
  },
};

document$.subscribe(() => {
  MathJax.typesetPromise();
});
