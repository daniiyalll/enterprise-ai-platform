// Add a class to the <html> element indicating WebP support so CSS can prefer .webp backgrounds.
(function(){
  function addClass(s){
    try{document.documentElement.classList.add(s);}catch(e){}
  }

  // Modern test using createImageBitmap
  if (self.createImageBitmap) {
    fetch('data:image/webp;base64,UklGRiIAAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=')
      .then(r => r.blob())
      .then(blob => createImageBitmap(blob))
      .then(() => addClass('webp'))
      .catch(() => addClass('no-webp'));
  } else {
    // Fallback test via canvas
    var img = new Image();
    img.onload = function(){
      var result = (img.width > 0) && (img.height > 0);
      addClass(result ? 'webp' : 'no-webp');
    };
    img.onerror = function(){ addClass('no-webp'); };
    img.src = 'data:image/webp;base64,UklGRiIAAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=';
  }
})();
