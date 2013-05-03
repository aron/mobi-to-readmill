if (window.FormData && document.querySelector) {
  var form = document.querySelector('form');
  var input = form.querySelector('input');
  var fallback = document.getElementById('fallback');

  if (fallback) {
    fallback.parentNode.removeChild(fallback);
  }

  function upload(options) {
    var data = new FormData();
    data.append(options.field || 'file', options.file, options.file.name);

    var xhr = new XMLHttpRequest();
    xhr.open('post', options.url, true);

    xhr.setRequestHeader('X-Requested-With', 'xmlhttprequest')
    xhr.addEventListener('load', function (event) {
      if (xhr.readyState === 4) {
        if (xhr.status >= 200 && xhr.status < 300) {
          options.onSuccess();
        } else {
          options.onError();
        }
        options.onComplete();
      }
    }, false);

    xhr.addEventListener('progress', function (event) {
      if (typeof options.onProgress === 'function' && event.lengthComputable) {
        options.onProgress(event.loaded / event.total);
      }
    });

    xhr.send(data);
  }

  function stop(cb) {
    return function (event) {
      event.stopPropagation();
      event.preventDefault();

      if (typeof cb === 'function') {
        return cb(event);
      }
    }
  }

  var timer;
  var quotes = [
      "This is the beginning of a great journey...",
      "People don't read any more",
      "Life is like a grapefruit",
      "We apologies for the inconvenience",
      "I come in peace, take me to your Lizard",
      "Anything that happens, happens",
      "Why are we surrounded by squirrels, and what do they want?",
      "Don't give any money to the unicorns, it only encourages them",
      "My cat. I call him \"the lord\". I am kind to him",
      "Humans are not proud of their ancestors...",
      "... and rarely invite them round to dinner"
  ];
  var progress = document.createElement('span');
  progress.className = 'progress';
  progress.innerHTML = quotes[0];
  document.body.appendChild(progress);

  var dropbox = document.body;
  dropbox.addEventListener('dragenter', stop(function (event) {
    dropbox.classList.add('active');
  }), false);

  dropbox.addEventListener('dragleave', function (event) {
    dropbox.classList.remove('active');
  }, false);

  dropbox.addEventListener('dragover', stop(), false);

  dropbox.addEventListener("drop", stop(function (event) {
    dropbox.classList.add('loading');
    dropbox.classList.remove('active');

    timer = setInterval(function () {
      progress.innerHTML = quotes.pop();
    }, 3000);

    upload({
      url: form.action,
      file: event.dataTransfer.files[0],
      field: input.name,
      onSuccess: function () {
        dropbox.classList.add('success');
      },
      onComplete: function () {
        clearTimeout(timer);
        dropbox.classList.remove('loading');
      },
      onError: function () {
        dropbox.classList.add('error');
      },
      onProgress: function (progress) {
        console.log(progress * 100);
      }
    });
  }), false);
}
