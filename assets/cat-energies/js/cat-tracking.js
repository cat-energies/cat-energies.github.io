(function(){
  var cfg = window.CAT_CONFIG && window.CAT_CONFIG.goatCounter;
  if(!cfg || !cfg.endpoint || !cfg.script) return;
  if(document.querySelector('script[data-cat-goatcounter]')) return;

  var script = document.createElement('script');
  script.async = true;
  script.src = cfg.script;
  script.setAttribute('data-goatcounter', cfg.endpoint);
  script.setAttribute('data-cat-goatcounter', cfg.slug || 'cat-energies-cattenom');
  document.head.appendChild(script);
})();
