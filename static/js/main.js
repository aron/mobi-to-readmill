if (Dropzone && Dropzone.isBrowserSupported() && document.querySelector) {
  var fallback = document.getElementById('fallback');
  if (fallback) {
    fallback.parentNode.removeChild(fallback);
  }
}
